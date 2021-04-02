import sqlite3


def get_entry_id(post, temp):
    """
    はてなブログAPI から特定記事のentry_idを取得
    :param post: 記事内容
    :param temp: localPATH
    """
    conn = sqlite3.connect('ファイル名')
    curs = conn.cursor()
    curs.execute("select entry_id from post where blog_id = ?", (post[0]['blog_id'],))
    dic = (curs.fetchall())[0][0]
    conn.close()
    return dic
