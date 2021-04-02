import sqlite3
import os
from packages.post_hatena import post_hatena
from google.cloud import storage

def modify_metadata(post, temp):
    """
    追加・修正したマークダウンファイルから記事内容を読み取り、記事内容を返す
    マークダウン内で指定した画像の中にGCSにアップした画像ファイルがあれば置換する
    :param post:記事内容
    :param temp:localPATH
    :param api_key:apiキー
    """
    # GCSに接続するための環境変数設定
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sample.json"  # サービスアカウントのjsonファイル
    client = storage.Client()
    # dbが入っているバケットを指定
    bucket = client.bucket('bucket名')
    # GCSかDBファイルをダウンロード
    bucket.blob('DBファイル').download_to_filename('ファイル名')

    # はてなブログにポスティングする
    posts = post_hatena(post, temp)

    # SQLliteに接続する
    conn = sqlite3.connect(temp + '/repo' + '/techblog.db')
    curs = conn.cursor()

    # カラム追加または変更して、コミットする
    for value in posts:
        if value['change_type'] == 'A':
            curs.execute("INSERT INTO post VALUES (?, ?, ?, ?, date(CURRENT_TIMESTAMP), date(CURRENT_TIMESTAMP))",
                         (value['blog_id'], value['entry_id'], value['url'], value['file']))
        elif value['change_type'] == 'D':
            curs.execute("UPDATE post set hatena_url=?, update_at=date(CURRENT_TIMESTAMP) where entry_id=?",
                         ("NULL", value['entry_id']))
        elif value['change_type'] == 'M':
            curs.execute("UPDATE post set update_at=date(CURRENT_TIMESTAMP) where entry_id=?", (value['entry_id'],))
        else:
            pass
    conn.commit()
    conn.close()
    ## DBの更新終了後、アップロード
    blob = bucket.blob('DBファイル')
    blob.upload_from_filename('ファイル名')
