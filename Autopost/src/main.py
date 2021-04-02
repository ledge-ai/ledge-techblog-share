import tempfile

import os
from packages.get_repository_diff_files import get_repository_diff_files
from packages.get_md_contents import get_md_contents
from packages.image_upload import image_upload
from packages.modify_metadata import modify_metadata
from google.cloud import secretmanager
def main():
    # 環境変数を取得
    GIT_URL = os.environ['GIT_URL']
    GIT_BRANCH_NAME = os.environ['GIT_BRANCH_NAME']
    with tempfile.TemporaryDirectory() as temp:
        os.mkdir(temp + '/.ssh')
        github_private = temp + '/.ssh/id_github.txt'
        github = open(github_private, 'w+')
        os.chmod(github_private, 0o700)
        os.chmod(temp + '/.ssh', 0o700)
        # プライベートレポジトリをCloneするためのPrivateKeyをSecretManagerで読み取る
        client = secretmanager.SecretManagerServiceClient()
        name = f"{SecretManager}"
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        github.write('{}'.format(payload))
        github.close()
        f = open(github_private, 'r')
        words = f.read()
        f.close()
        diff = get_repository_diff_files(GIT_URL, temp, GIT_BRANCH_NAME, github_private)
        image = []
        markdown = []
        image_extension = ["jpg", "jpeg", "gif", "png", "svg"]
        docs_extension = ["md"]
        for value in diff:
            if value['path'].split(".")[-1] in image_extension:
                image.append(value)
            elif value['path'].split(".")[-1] in docs_extension:
                markdown.append(value)
            else:
                pass

        image_uploads = image_upload(image)

        post = get_md_contents(image_uploads, markdown)

        modify_metadata(post, temp)

        print("無事に完了しました。")


if __name__ == "__main__":
    main()
