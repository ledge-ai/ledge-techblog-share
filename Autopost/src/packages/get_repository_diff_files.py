import os
from git import Repo


def get_repository_diff_files(repository_url, local_path, branch_name, github_private):

    """
    引数で指定したレポジトリをダウンロードし、指定したブランチの差分ファイルパスを出力する。
    :param repository_url: リポジトリのURL
    :param local_path: ローカルのファイルオブジェクト
    :param branch_name: ブランチ名
    :return: 差分サマリ型
    """
    _repo_path = os.path.join(local_path, "repo")
    repo = Repo.clone_from(repository_url, _repo_path,
                           branch=branch_name, env={"GIT_SSH_COMMAND": 'ssh -i {} -o {}'.format(github_private, "StrictHostKeyChecking=no")})
    draft_rev_num = None
    for commit in repo.iter_commits('origin/draft', max_count=1):
        draft_rev_num = commit.hexsha
    with repo.config_writer().set_value('core', 'quotepath', 'false'):
        diff = repo.head.commit.diff(draft_rev_num)

    # 差分情報の取得
    diff_summary = []
    for diff_file in diff:
        diff_summary.append(
            {
                "path": local_path + '/repo/' + diff_file.a_path,
                "change_type": diff_file.change_type,
                "rename_from": diff_file.a_path if diff_file.change_type == 'R' else None
            }
        )


    # ブランチをマージ
    commit_message = 'Merge draft into master from Autopost'
    if len(diff) > 0:
        repo.git.checkout('draft')
        repo.git.checkout(branch_name)
        master_branch = repo.branches[branch_name]
        draft_branch = repo.branches['draft']
        base = repo.merge_base(draft_branch, master_branch)
        repo.index.merge_tree(draft_branch, base=base)
        repo.index.commit('Merge draft into ' + branch_name + ' by Autopost',
                          parent_commits=(draft_branch.commit, master_branch.commit))
        repo.remote(name='origin').push(branch_name)
        repo.index.reset(index=True, working_tree=True)
    return diff_summary
