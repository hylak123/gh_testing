
import string
from pathlib import Path
from random import choices

import git

from basic_commands import BasicCommands as _BCmd

REPO_URL_HTTPS = "https://github.com/hylak123/gh_testing.git"


def content_generator(text_type: str, text_length: int, save_path=None) -> list | str:
    if text_type == "commit_msg":
        commit_msg = "Random commit message: " + "".join(
            choices(string.ascii_letters, k=text_length)
        )
        return str(commit_msg)
    elif text_type == "text":
        random_txt = "".join(choices(string.ascii_letters, k=text_length))
        return str(random_txt)
    elif text_type == "file":
        filename = str("".join(choices(string.ascii_letters, k=text_length)) + ".txt")
        random_content = []
        [
            random_content.append(
                str("".join(choices(string.ascii_letters, k=text_length))) + "\n"
            )
            for _ in range(text_length)
        ]
        filepath = save_path + "\\" + filename
        with open(filepath, "a") as file:
            file.writelines(random_content)
        return filepath


TEST_DATA = {
    "test_repo_init": {"repo_path_local": r"C:\work\gh_testing2"},
    "test_open_existing_repo": {"repo_path_local": r"C:\work\gh_testing2"},
    "test_clone_remote_repo_https": {
        "remote_repo_url": REPO_URL_HTTPS,
        "repo_path_local": r"C:\work\gh_testing3",
    },
    "test_commit": {
        "remote_repo_url": REPO_URL_HTTPS,
        "repo_path_local": r"C:\work\gh_testing5",
        "commit_msg": content_generator("commit_msg", 10),
    },
    "test_create_new_branch": {
        "remote_repo_url": REPO_URL_HTTPS,
        "repo_path_local": r"C:\work\gh_testing6",
        "new_branch_name": content_generator("text", 20),
    },
    "test_switch_branch": {
        # "remote_repo_url": REPO_URL_HTTPS,
        "repo_path_local": r"C:\work\gh_testing6",
        "existing_branch_name": content_generator("text", 20),
    },
    "test_pull": {
        "remote_repo_url": REPO_URL_HTTPS,
        "repo_path_local": r"C:\work\gh_testing7",
        "existing_branch_name": "main",
    },
    "test_push": {
        # "remote_repo_url": REPO_URL_HTTPS,
        "repo_path_local": r"C:\work\gh_testing7",
        "existing_branch_name": "main",
    },
}


class TestGithub:
    """A class holding git commands and tests."""

    def test_repo_init(
            self,
            action="test_repo_init",
            repo_path_local=TEST_DATA["test_repo_init"]["repo_path_local"],
    ):
        self.run_gh_test_flow_template(action=action, repo_path_local=repo_path_local)

    def test_open_existing_repo(
            self,
            action="test_open_existing_repo",
            repo_path_local=TEST_DATA["test_open_existing_repo"]["repo_path_local"],
    ):
        self.run_gh_test_flow_template(action=action, repo_path_local=repo_path_local)

    def test_clone_remote_repo_https(
            self,
            action="test_clone_remote_repo_https",
            remote_repo_url=TEST_DATA["test_clone_remote_repo_https"]["remote_repo_url"],
            repo_path_local=TEST_DATA["test_clone_remote_repo_https"]["repo_path_local"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            remote_repo_url=remote_repo_url,
            repo_path_local=repo_path_local,
        )

    def test_commit(
            self,
            action="test_commit",
            remote_repo_url=TEST_DATA["test_commit"]["remote_repo_url"],
            repo_path_local=TEST_DATA["test_commit"]["repo_path_local"],
            commit_msg=TEST_DATA["test_commit"]["commit_msg"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            remote_repo_url=remote_repo_url,
            repo_path_local=repo_path_local,
            commit_msg=commit_msg,
        )

    def test_create_new_branch(
            self,
            action="test_create_new_branch",
            remote_repo_url=TEST_DATA["test_create_new_branch"]["remote_repo_url"],
            repo_path_local=TEST_DATA["test_create_new_branch"]["repo_path_local"],
            new_branch_name=TEST_DATA["test_create_new_branch"]["new_branch_name"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            remote_repo_url=remote_repo_url,
            repo_path_local=repo_path_local,
            new_branch_name=new_branch_name,
        )

    def test_switch_branch(
            self,
            action="test_switch_branch",
            # remote_repo_url=TEST_DATA["test_switch_branch"]["remote_repo_url"],
            repo_path_local=TEST_DATA["test_switch_branch"]["repo_path_local"],
            existing_branch_name=TEST_DATA["test_switch_branch"]["existing_branch_name"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            # remote_repo_url=remote_repo_url,
            repo_path_local=repo_path_local,
            existing_branch_name=existing_branch_name,
        )

    def test_pull(
            self,
            action="test_pull",
            remote_repo_url=TEST_DATA["test_pull"]["remote_repo_url"],
            repo_path_local=TEST_DATA["test_pull"]["repo_path_local"],
            existing_branch_name=TEST_DATA["test_pull"]["existing_branch_name"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            remote_repo_url=remote_repo_url,
            repo_path_local=repo_path_local,
            existing_branch_name=existing_branch_name,
        )

    def test_push(
            self,
            action="test_push",
            # remote_repo_url=TEST_DATA["test_push"]["remote_repo_url"],
            repo_path_local=TEST_DATA["test_push"]["repo_path_local"],
            existing_branch_name=TEST_DATA["test_push"]["existing_branch_name"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            # remote_repo_url=remote_repo_url,
            repo_path_local=repo_path_local,
            existing_branch_name=existing_branch_name,
        )

    @staticmethod
    def run_gh_test_flow_template(
            action,
            repo_path_local=None,
            remote_repo_url=None,
            commit_msg="",
            new_branch_name="",
            existing_branch_name="",
    ):
        """
        Positive test flow template method
        :param action: test action to perform
        :param repo_path_local: local repository path
        :param remote_repo_url: url to remote repo
        :param commit_msg: message to commit
        :param new_branch_name: name of new branch to create
        :param existing_branch_name: name of a branch existing in repo

        """
        if action == "test_repo_init":
            print("Test repo init")
            new_repo = _BCmd.init_repo(repo_path_local)
            # assert (
            #         new_repo.working_dir == repo_path_local
            # ), f"Repo {new_repo} initialization failed"
            print(
                f"New repo {new_repo.git_dir} initialized. Working dir {new_repo.working_dir}"
            )
        elif action == "test_open_existing_repo":
            print("Test open the existing local repo")
            assert (
                    Path(repo_path_local).exists()
                    and Path(repo_path_local + "/.git").exists()
            ), f"Repo {repo_path_local} does not exist or is not a git repository"
            existing_repo = _BCmd.open_existing_local_repo(repo_path_local)
            assert (
                    existing_repo.working_dir == repo_path_local
            ), f"Failed to open {existing_repo.working_dir}"
            print(f"Existing repo {existing_repo.git_dir} opened")
        # parametrize
        elif action == "test_clone_remote_repo_https":
            print("Test clone a remote repo")
            cloned_repo = _BCmd.clone_remote_repo(remote_repo_url, repo_path_local)
            assert (
                    cloned_repo.working_dir == repo_path_local
            ), f"Failed to create {cloned_repo}, url: {remote_repo_url} at location: {repo_path_local}"
            print(
                f"Repository {cloned_repo}, url: {remote_repo_url} cloned at location: {repo_path_local}"
            )
        elif action == "test_commit":
            print("Test adding files to stage and commit")
            repo = _BCmd.clone_remote_repo(remote_repo_url, repo_path_local)
            data = (content_generator("file", 10, repo.working_dir),)
            _BCmd.add_files_to_stage(repo, [data[0]])
            _BCmd.commit(repo, commit_msg)

            head_commit = repo.head.commit
            assert (
                    head_commit.message == commit_msg
            ), f"Last commit message {commit_msg} differs from {head_commit.message}"
        elif action == "test_create_new_branch":
            print("Test creating a new branch")
            try:
                repo = _BCmd.clone_remote_repo(remote_repo_url, repo_path_local)
                # flow
            except git.exc.GitError:
                repo = _BCmd.open_existing_local_repo(repo_path_local)
                new_branch = _BCmd.create_new_branch(repo, new_branch_name)
                assert (
                        repo.active_branch != new_branch
                ), f"Branch {new_branch} already exists in repo {repo}"
                print(
                    f"New branch {new_branch} created. New branch is different from active branch: {repo.active_branch}"
                )
        elif action == "test_switch_branch":
            print("Test switch to a new branch")
            repo = _BCmd.open_existing_local_repo(repo_path_local)
            existing_branch = _BCmd.create_new_branch(repo, existing_branch_name)

            print(f"List of existing branches:")
            existing_branches = []
            for branch in repo.branches:
                existing_branches.append(branch)
                print(f"{branch}")

            _BCmd.switch_branch(repo, existing_branch_name)
            assert (
                    existing_branch in existing_branches
            ), f"Branch {existing_branch} does not exist in repo: {repo}"
            print(f"Switched to branch {existing_branch} existing in repo: {repo}")
        elif action == "test_pull":
            print("Test pull from remote repo")
            try:
                repo = _BCmd.clone_remote_repo(remote_repo_url, repo_path_local)
            except git.exc.GitCommandError:
                repo = _BCmd.open_existing_local_repo(repo_path_local)
            try:
                print("List of Remotes:")
                for remote in repo.remotes:
                    print(f"- {remote.name} {remote.url}")

                _BCmd.pull_from_remote_repo(repo)
            except ValueError:
                print("List of Remotes:")
                for remote in repo.remotes:
                    print(f"- {remote.name} {remote.url}")

                print("Creating a new remote")
                try:
                    remote = repo.create_remote(name="origin", url=remote_repo_url)
                except git.exc.GitCommandError as error:
                    print(f"Error creating remote: {error}")

                    # flow
                    print("Reference to remote branch")
                    print(f"Remote name: {repo.remotes.origin.name}")
                    print(f"Remote URL: {repo.remotes.origin.url}")

                    _BCmd.pull_from_remote_repo(repo)
                    # Pull from remote repo
                    print(repo.remotes.origin.pull())
                    # Push changes
                    print(repo.remotes.origin.push())
        elif action == "test_push":
            print("Test pushing local commits to remote repo")
            repo = _BCmd.open_existing_local_repo(repo_path_local)
            _BCmd.switch_branch(repo, existing_branch_name)

            print("Test adding files to stage and commit")
            data = (content_generator("file", 10, repo.working_dir),)
            _BCmd.add_files_to_stage(repo, [data[0]])
            commit_msg = content_generator("commit_msg", 10)
            _BCmd.commit(repo, commit_msg)

            print('Pushed changes to origin')

            _BCmd.push(repo)
