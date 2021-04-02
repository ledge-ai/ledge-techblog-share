import html
import re
import xml.etree.ElementTree as ET
import requests
import os
import yaml
from packages.get_entry_id import get_entry_id

def post_hatena(post, temp):
    """
    はてなブログのAPIフォーマットに従い、引数の内容をはてなブログへPOSTし、記事URLを取得する。
    投稿に際しての認証情報、投稿先は設定値を参照する
    postのchange_typeの値で次のように動作する
        Aの場合、APIで記事内容を新規で追加し、取得したURLと記事IDを返す
        Mの場合、APIで記事を修正し、取得したURLと記事IDを返す
        Dの場合、APIで記事を削除し、urlはnullを返す
        Rの場合、APIに投稿せず、urlはnullを返す
    :param post: 記事内容
    """
    HATENA_BLOG_ID = os.environ['HATENA_BLOG_ID']
    API_KEY = os.environ['API_KEY']
    BLOG_ID = os.environ['BLOG_ID']

    with open("blog_format.txt", 'r') as data_file:
        data = data_file.read()
    summary = []
    col_url = "https://blog.hatena.ne.jp/{}/{}/atom/entry".format(HATENA_BLOG_ID, BLOG_ID)
    for value in post:
        # 追加
        if value['change_type'] == "A":
            post = requests.post(url=col_url, auth=(HATENA_BLOG_ID, API_KEY), data=data.format(value["title"], html.escape(value["text"]), value["category"]).encode('utf-8'))
            root = ET.fromstring(post.text)
            summary.append(
                {
                    "blog_id": value['blog_id'],
                    "file": value['file'],
                    "change_type": value['change_type'],
                    "title": value['title'],
                    "category": value['category'],
                    "text": value['text'],
                    "url": root.findall("{http://www.w3.org/2005/Atom}link/[@rel='alternate']")[0].get('href'),
                    "entry_id": re.sub(r"https:.+entry/", "", root.findall("{http://www.w3.org/2005/Atom}link/[@rel='edit']")[0].get('href'))
                }
            )
        # 修正
        elif value['change_type'] == "M":
            entry_id = repr(get_entry_id(post, temp))
            collection_url = "https://blog.hatena.ne.jp/{}/{}/atom/entry/{}".format(HATENA_BLOG_ID, BLOG_ID, entry_id)
            # data = data.format(value["title"], html.escape(value["text"]), value["category"]).encode('utf-8')
            edit = requests.put(url=collection_url, auth=(HATENA_BLOG_ID, API_KEY), data=data.format(value["title"], html.escape(value["text"]), value["category"]).encode('utf-8'))
            root = ET.fromstring(edit.text)
            summary.append(
                {
                    "blog_id": value['blog_id'],
                    "file": value['file'],
                    "change_type": value['change_type'],
                    "title": value['title'],
                    "category": value['category'],
                    "text": value['text'],
                    "url": root.findall("{http://www.w3.org/2005/Atom}link/[@rel='alternate']")[0].get('href'),
                    "entry_id": entry_id
                }
            )
        # 削除
        elif value['change_type'] == "D":
            entry_id = repr(get_entry_id(post, temp))
            collection_url = "https://blog.hatena.ne.jp/{}/{}/atom/entry/{}".format(HATENA_BLOG_ID, BLOG_ID, entry_id)
            # data = data.format(value["title"], html.escape(value["text"]), value["category"]).encode('utf-8')
            delete = requests.delete(url=collection_url, auth=(HATENA_BLOG_ID, API_KEY), data=data.format(value["title"], html.escape(value["text"]), value["category"]).encode('utf-8'))
            summary.append(
                {
                    "blog_id": value['blog_id'],
                    "file": value['file'],
                    "change_type": value['change_type'],
                    "title": value['title'],
                    "category": value['category'],
                    "text": value['text'],
                    "url": "NULL",
                    "entry_id": entry_id
                }
            )
        # Rename
        elif value['change_type'] == "R":
            entry_id = repr(get_entry_id(post, temp))
            summary.append(
                {
                    "blog_id": value['blog_id'],
                    "file": value['file'],
                    "change_type": value['change_type'],
                    "title": value['title'],
                    "category": value['category'],
                    "text": value['text'],
                    "url": "NULL",
                    "entry_id": entry_id
                }
            )
        else:
            pass
    return summary

