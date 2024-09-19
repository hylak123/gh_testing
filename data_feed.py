from basic_commands import content_generator
import platform


REPO_URL_HTTPS = "https://github.com/hylak123/gh_testing.git"
REPO_SSH = "git@github.com:hylak123/gh_testing.git"


def get_data_feed():
    HOME = ""
    system = platform.system()
    if "Windows" in system:
        HOME = r"C:\work\gh_testing"
    elif "Linux" in system:
        HOME = r"/home/runner/work/gh_testing"

    TEST_DATA = {
        "test_repo_init": {"repo_path_local": r"C:\work\gh_testing2"},
        "test_open_existing_repo": {"repo_path_local": r"C:\work\gh_testing2"},
        "test_clone_remote_repo_https": {
            "remote_repo_url": REPO_URL_HTTPS,
            "repo_path_local": HOME,
        },
        "test_clone_remote_repo_ssh": {
            "remote_repo_url": REPO_SSH,
            "repo_path_local": HOME,
        },
        "test_commit": {
            "remote_repo_url": REPO_URL_HTTPS,
            "repo_path_local": HOME,
            "commit_msg": content_generator("commit_msg", 10),
        },
        "test_create_new_branch": {
            "remote_repo_url": REPO_URL_HTTPS,
            "repo_path_local": HOME,
            "new_branch_name": content_generator("text", 20),
        },
        "test_switch_branch": {
            # "remote_repo_url": REPO_URL_HTTPS,
            "repo_path_local": HOME,
            "existing_branch_name": content_generator("text", 20),
        },
        "test_pull": {
            "remote_repo_url": REPO_URL_HTTPS,
            "repo_path_local": HOME,
            "existing_branch_name": "main",
        },
        "test_push": {
            # "remote_repo_url": REPO_URL_HTTPS,
            "repo_path_local": HOME,
            "existing_branch_name": "main",
        },
    }
    return HOME, TEST_DATA
