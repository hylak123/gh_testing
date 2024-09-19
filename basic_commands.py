import logging
import os
import string
from pathlib import Path
from random import choices

from git import Repo


class BasicCommands:
    @staticmethod
    def init_repo(local_path: Path | str):
        """
        To Initialize a new repository
        :param local_path: a path on local filesystem
        :return: initialized repository obj
        """
        return Repo.init(local_path)

    @staticmethod
    def open_existing_local_repo(local_path: Path | str):
        """
        To Open the Existing local repository
        :param local_path: a path on local filesystem
        :return: repository obj
        """
        return Repo(local_path)

    @staticmethod
    def clone_remote_repo(repo_url: str, local_path: Path | str):
        """
        To create a local copy of the repository at the specified local_path directory via HTTPS,
        using the repository URL repo_url
        :param repo_url: URL of remote repository
        :param local_path: a path on local filesystem
        :return: repository obj
        """
        print(f"Cloning repository, url: {repo_url} at location: {local_path}")
        return Repo.clone_from(repo_url, local_path)

    @staticmethod
    def clone_remote_repo_ssh(repo_addr: str, local_path: Path | str):
        """
        To create a local copy of the repository at the specified local_path directory via SSH
        :param repo_addr: URL of remote repository
        :param local_path: a path on local filesystem
        :return: repository obj
        """
        logging.basicConfig(level=logging.INFO)
        os.environ["GIT_PYTHON_TRACE"] = "1"
        return Repo.clone_from(
            repo_addr, local_path, env={"GIT_SSH_COMMAND": "ssh -i /tmp/id_rsa"}
        )

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
        :return: repository obj
        """
        print(f"Created commit with message: {msg}")
        repo.index.commit(msg)

    @staticmethod
    def push(repo):
        """
        Push the local commits to the remote repo
        :param repo: repository obj
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
        # return repo.git.branch(branch_name)

    @staticmethod
    def checkout_branch(repo, branch_name: str):
        """
        To check out the new branch
        :param repo: repository obj
        :param branch_name: name of a branch
        """
        return repo.git.checkout(branch_name)

    @staticmethod
    def switch_branch(repo, branch_name: str):
        """
        To switch to an existing branch
        :param repo: repository obj
        :param branch_name: branch name
        """
        branch = repo.heads[branch_name]
        branch.checkout()
        return branch

    @staticmethod
    def pull_from_remote_repo(repo):
        """
        To update the local repository with the latest changes from the remote repo
        :param repo: repository obj
        """
        origin = repo.remote(name="origin")
        origin.pull()


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
