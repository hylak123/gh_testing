from pathlib import Path

from git import Repo

REPO_URL_HTTPS = "https://github.com/hylak123/gh_testing.git"

TEST_DATA = {
    "test_repo_init": {"repo_path_local": r"C:\work\gh_testing2"},
    "test_open_existing_repo": {"repo_path_local": r"C:\work\gh_testing2"},
    "test_clone_remote_repo_https": {
        "remote_repo_url": REPO_URL_HTTPS,
        "repo_path_local": r"C:\work\gh_testing3",
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

    @staticmethod
    def run_gh_test_flow_template(
            action,
            repo_path_local=None,
            remote_repo_url=None,
            commit_data=None,
            commit_msg="",
            new_branch_name="",
            existing_branch_name="",
    ):
        """
        Positive test flow template method
        :param logger: class logger
        :param action: test action to perform
        :param repo_path_local: local repository path
        :param remote_repo_url: url to remote repo
        :param commit_data: data to commit
        :param commit_msg: message to commit
        :param new_branch_name: name of new branch to create
        :param existing_branch_name: name of a branch existing in repo

        """
        if action == "test_repo_init":
            print("Test repo init")
            new_repo = TestGithub.init_repo(repo_path_local)
            assert (
                    new_repo.working_dir == repo_path_local
            ), f"Repo {new_repo} initialization failed"
            print(
                f"New repo {new_repo.git_dir} initialized. Working dir {new_repo.working_dir}"
            )
        elif action == "test_open_existing_repo":
            print("Test open the existing local repo")
            assert (
                    Path(repo_path_local).exists()
                    and Path(repo_path_local + "/.git").exists()
            ), f"Repo {repo_path_local} does not exist or is not a git repository"
            existing_repo = TestGithub.open_existing_local_repo(repo_path_local)
            assert (
                    existing_repo.working_dir == repo_path_local
            ), f"Failed to open {existing_repo.working_dir}"
            print(f"Existing repo {existing_repo.git_dir} opened")
        elif action == "test_clone_remote_repo_https":
            print("Test clone a remote repo")
            cloned_repo = TestGithub.clone_remote_repo(remote_repo_url, repo_path_local)
            assert (
                    cloned_repo.working_dir == repo_path_local
            ), f"Failed to create {cloned_repo}, url: {remote_repo_url} at location: {repo_path_local}"
            print(
                f"Repository {cloned_repo}, url: {remote_repo_url} cloned at location: {repo_path_local}"
            )


    @staticmethod
    def init_repo(local_path: Path | str):
        """
        To Initialize a new repository
        :param local_path: a path on local filesystem
        :return: initialized repo
        """
        return Repo.init(local_path)

    @staticmethod
    def open_existing_local_repo(local_path: Path | str):
        """
        To Open the Existing local repository
        :param local_path: a path on local filesystem
        :return: cloned repo
        """
        return Repo(local_path)

    @staticmethod
    def clone_remote_repo(repo_url: str, local_path: Path | str):
        """
        To create a local copy of the repository at the specified local_path directory,
        using the repository URL repo_url
        :param repo_url: URL of remote repository
        :param local_path: a path on local filesystem
        :return: cloned repo
        """
        print(f"Cloning repository, url: {repo_url} at location: {local_path}")
        return Repo.clone_from(repo_url, local_path)

    @staticmethod
    def add_files_to_stage(repo, files: list | None):
        """
        Add specified files to staqe (index).
        :param repo: local repository obj
        :param files: files to be added to stage
        """
        print(f"Adding files {files} to repo {repo} stage")
        repo.index.add(files)

    @staticmethod
    def commit(repo, msg: str):
        """
        Create a new commit in the local repository with the specified commit message.
        :param repo: local repository obj
        :param msg: commit message
        :return: cloned repo
        """
        print(f"Created commit with message: {msg}")
        repo.index.commit(msg)

    @staticmethod
    def push(repo, upstream):
        """
        Push the local commits to the remote repo
        :param repo: repository obj
        :param upstream: upstream branch
        :return: cloned repo
        """
        origin = repo.remote(name="origin")
        origin.push()

    @staticmethod
    def create_new_branch(repo, branch_name: str):
        """
        Create new branch in local repo
        :param repo: repository obj
        :param branch_name: new branch name
        :return: new branch
        """
        return repo.create_head(branch_name)

    @staticmethod
    def checkout_branch(repo, branch_name: str):
        """
        To check out the new branch
        :param repo: repository obj
        :param branch_name: name of a branch
        """
        branch = repo.heads[branch_name]
        branch.checkout()

    @staticmethod
    def switch_branch(repo, existing_branch: str):
        """
        To switch to an existing branch
        :param repo: repository obj
        :param existing_branch: branch name
        """
        existing_branch = repo.heads[existing_branch]
        existing_branch.checkout()

    @staticmethod
    def pull_from_remote_repo(repo, upstream_branch):
        """
        To update the local repository with the latest changes from the remote repo
        :param repo: repository obj
        :param upstream_branch: upstream branch name
        :return: new branch
        """
        origin = repo.remote(name=rf"origin/{upstream_branch}")
        origin.pull()
