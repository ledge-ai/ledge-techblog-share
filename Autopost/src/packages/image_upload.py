from google.cloud import storage
import urllib.parse

def image_upload(image):
    """
    差分ファイルの中から[画像ファイル](#画像ファイルの定義)をGCSにファイルをアップし、アップして公開される場合のURLを得る。
    :param image:imageファイルのPATH、change_type、rename_from
    """
    storage_client = storage.Client.from_service_account_json("sample.json")
    bucket = storage_client.get_bucket('techblog')
    diff_summary = []
    for image in image:
        local_image_path = image['path'].split('repo/')[1]
        blob = bucket.blob(local_image_path)
        blob.upload_from_filename(image['path'])
        # public設定, URL表示
        blob.make_public()
        url = blob.public_url
        diff_summary.append(
            {
                "local_path": "../" + local_image_path,
                "remote_path": urllib.parse.unquote(url)
            }
        )
    return diff_summary
