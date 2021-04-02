import re

def get_md_contents(image_uploads, markdown):
    """
    追加・修正したマークダウンファイルから記事内容を読み取り、記事内容を返す
    マークダウン内で指定した画像の中にGCSにアップした画像ファイルがあれば置換する
    :param image_uploads: GithubのイメージPATHとGCSのイメージPATH
    :param markdown: 記事のタイトル
    """
    md_contents = []
    # Markdownファイル読み取り
    for md in markdown:
        file_open = open(md['path'], "r+")
        read_fp = file_open.read()

        # GithubのPATHをGCSのPATHに変換
        for image_trade in image_uploads:
            read_fp = read_fp.replace(image_trade['local_path'], image_trade['remote_path'])
        title = re.findall(r'title: (.*)', read_fp)[0]
        change_type = md['change_type']
        file = md['path'].split('docs/')[1]
        category = re.findall(r'category: (.*)', read_fp)[0]
        blog_id = re.findall(r'blog_id: (.*)', read_fp)[0]
        md_contents.append(
            {
                "blog_id": blog_id,
                "file": file,
                "change_type": change_type,
                "title": title,
                "category": category,
                "text": re.split(r'---', read_fp)[2:]

            }
        )
    return md_contents
