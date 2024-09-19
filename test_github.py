import shutil
from pathlib import Path

import git
import pytest

from basic_commands import BasicCommands as _BCmd, content_generator
from data_feed import get_data_feed


class TestGithub:
    """A class holding git commands and tests."""

    HOME_DIR, TEST_DATA = get_data_feed()

    @pytest.fixture
    def cleanup(self):
        repo_path = self.HOME_DIR
        yield repo_path
        try:
            if Path(repo_path).exists():
                shutil.rmtree(repo_path)
                print(f"Cleanup after test performed. Removed {repo_path}")
        except OSError:
            print(f"Cleanup failed, failed to remove {repo_path}")

    @pytest.mark.smoke
    @pytest.mark.CI
    def test_repo_init(
        self,
        cleanup,
        action="test_repo_init",
        repo_path_local=TEST_DATA["test_repo_init"]["repo_path_local"],
    ):
        self.run_gh_test_flow_template(action=action, repo_path_local=repo_path_local)

    @pytest.mark.CI
    def test_open_existing_repo(
        self,
        cleanup,
        action="test_open_existing_repo",
        remote_repo_url=TEST_DATA["test_open_existing_repo"]["remote_repo_url"],
        repo_path_local=TEST_DATA["test_open_existing_repo"]["repo_path_local"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            remote_repo_url=remote_repo_url,
            repo_path_local=repo_path_local,
        )

    @pytest.mark.CI
    def test_clone_remote_repo_https(
        self,
        cleanup,
        action="test_clone_remote_repo_https",
        remote_repo_url=TEST_DATA["test_clone_remote_repo_https"]["remote_repo_url"],
        repo_path_local=TEST_DATA["test_clone_remote_repo_https"]["repo_path_local"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            remote_repo_url=remote_repo_url,
            repo_path_local=repo_path_local,
        )

    def test_clone_remote_repo_ssh(
        self,
        cleanup,
        action="test_clone_remote_repo_ssh",
        remote_repo_url=TEST_DATA["test_clone_remote_repo_ssh"]["remote_repo_url"],
        repo_path_local=TEST_DATA["test_clone_remote_repo_ssh"]["repo_path_local"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            remote_repo_url=remote_repo_url,
            repo_path_local=repo_path_local,
        )

    @pytest.mark.CI
    def test_commit(
        self,
        cleanup,
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

    @pytest.mark.CI
    def test_create_new_branch(
        self,
        cleanup,
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

    @pytest.mark.CI
    def test_switch_branch(
        self,
        cleanup,
        action="test_switch_branch",
        remote_repo_url=TEST_DATA["test_switch_branch"]["remote_repo_url"],
        repo_path_local=TEST_DATA["test_switch_branch"]["repo_path_local"],
        existing_branch_name=TEST_DATA["test_switch_branch"]["existing_branch_name"],
        new_branch_name=TEST_DATA["test_switch_branch"]["new_branch_name"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            remote_repo_url=remote_repo_url,
            repo_path_local=repo_path_local,
            existing_branch_name=existing_branch_name,
            new_branch_name=new_branch_name,
        )

    @pytest.mark.CI
    def test_pull(
        self,
        cleanup,
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

    @pytest.mark.CI
    def test_push(
        self,
        cleanup,
        action="test_push",
        remote_repo_url=TEST_DATA["test_push"]["remote_repo_url"],
        repo_path_local=TEST_DATA["test_push"]["repo_path_local"],
        existing_branch_name=TEST_DATA["test_push"]["existing_branch_name"],
    ):
        self.run_gh_test_flow_template(
            action=action,
            remote_repo_url=remote_repo_url,
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
            assert (
                new_repo.working_dir == repo_path_local
            ), f"Repo {new_repo} initialization failed"
            print(
                f"New repo {new_repo.git_dir} initialized. Working dir {new_repo.working_dir}"
            )
        elif action == "test_open_existing_repo":
            print("Test open the existing local repo")
            repo = _BCmd.clone_remote_repo(remote_repo_url, repo_path_local)
            repo.close()
            assert (
                Path(repo_path_local).exists()
                and Path(repo_path_local + "/.git").exists()
            ), f"Repo {repo_path_local} does not exist or is not a git repository"
            existing_repo = _BCmd.open_existing_local_repo(repo_path_local)
            assert (
                existing_repo.working_dir == repo_path_local
            ), f"Failed to open {existing_repo.working_dir}"
            print(f"Existing repo {existing_repo.git_dir} opened")
        elif action == "test_clone_remote_repo_https":
            print("Test clone a remote repo via https")
            cloned_repo = _BCmd.clone_remote_repo(remote_repo_url, repo_path_local)
            assert (
                cloned_repo.working_dir == repo_path_local
            ), f"Failed to create {cloned_repo}, url: {remote_repo_url} at location: {repo_path_local}"
            print(
                f"Repository {cloned_repo}cloned via https, url: {remote_repo_url} to location: {repo_path_local}"
            )
        elif action == "test_clone_remote_repo_ssh":
            print("Test clone a remote repo via ssh")
            cloned_repo = _BCmd.clone_remote_repo_ssh(remote_repo_url, repo_path_local)
            assert (
                cloned_repo.working_dir == repo_path_local
            ), f"Failed to create {cloned_repo}, url: {remote_repo_url} at location: {repo_path_local}"
            print(
                f"Repository {cloned_repo} cloned via ssh, addr: {remote_repo_url} to location: {repo_path_local}"
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
                new_branch = _BCmd.create_new_branch(repo, new_branch_name)
                assert (
                    repo.active_branch != new_branch
                ), f"Branch {new_branch} already exists in repo {repo}"
                print(
                    f"New branch {new_branch} created. New branch is different from active branch: {repo.active_branch}"
                )
            except git.exc.GitError:
                print("Failed to create branch")
        elif action == "test_switch_branch":
            print("Test switch to a new branch")
            try:
                repo = _BCmd.clone_remote_repo(remote_repo_url, repo_path_local)
                first_branch_name = existing_branch_name
                second_branch_name = new_branch_name
                _BCmd.create_new_branch(repo, first_branch_name)
                _BCmd.create_new_branch(repo, second_branch_name)
                repo.close()

                repo = _BCmd.open_existing_local_repo(repo_path_local)
                first_branch = _BCmd.checkout_branch(repo, first_branch_name)
                print(f"Actual branch is: {first_branch}")

                print(f"Switching to a new branch: {second_branch_name}")
                second_branch = _BCmd.switch_branch(repo, second_branch_name)
                print(f"Actual branch is: {second_branch}")

                print(f"List of existing branches:")
                existing_branches = []
                for branch in repo.branches:
                    existing_branches.append(branch)
                    print(f"{branch}")

                assert (
                    first_branch != second_branch
                ), f"Failed to switch branch {first_branch} = {second_branch}"
            except git.exc.GitCommandError as ex:
                print(f"Failed to clone repo {ex}")
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
            repo = _BCmd.clone_remote_repo(remote_repo_url, repo_path_local)
            _BCmd.switch_branch(repo, existing_branch_name)

            print("Test adding files to stage and commit")
            data = (content_generator("file", 10, repo.working_dir),)
            _BCmd.add_files_to_stage(repo, [data[0]])
            commit_msg = content_generator("commit_msg", 10)
            _BCmd.commit(repo, commit_msg)

            print("Pushed changes to origin")

            _BCmd.push(repo)
