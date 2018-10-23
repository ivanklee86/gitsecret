import git
from gitsecret.utils import _command_and_parse
from gitsecret import constants


class GitSecretException(Exception):
    pass


class GitSecret():
    def __init__(self, path: str):
        # Class variables
        self.repo_path = path

        # Create gitpython.Repo object to ensure file is actually a repo.
        self.git_repo = git.Repo(self.repo_path)

    def create(self):
        (output, search_results) = _command_and_parse(command=constants.GIT_SECRET_INIT_COMMAND,
                                                      regex=constants.GIT_SECRET_INIT_REGEX,
                                                      location=self.repo_path)

        if not search_results:
            raise GitSecretException("Error initializing gitsecret.  Error: %s" % output.stdout.decode("utf-8"))
