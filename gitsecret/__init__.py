import re
import shlex
import subprocess
from typing import Optional, Tuple
import git
from gitsecret import constants


class GitSecretException(Exception):
    pass


class GitSecret():
    def __init__(self, path: str):
        # Class variables
        self.repo_path = path

        # Create gitpython.Repo object to ensure file is actually a repo.
        self.git_repo = git.Repo(self.repo_path)

    def _command_and_parse(self,
                           command: str,
                           regex: Optional[str] = None) -> Tuple[subprocess.CompletedProcess, list]:
        """
        A (inflexible, implementation-focused) centralized method to run a method and optionally applies a regex to the
        stdout.

        :param command: Command to run (just like in the terminal, to be parsed in method)!
        :param regex: Regex string. Optional.
        :param location: Location to run command.  Optional
        :return:
        """

        # _Set up for method_
        parsed_command = shlex.split(command)
        search_result: list = []

        # _Run command and parse_
        output = subprocess.run(args=parsed_command, capture_output=True, cwd=self.repo_path)

        if regex and output.returncode == 0:
            search_result = re.findall(regex, output.stdout.decode("utf-8"))

        return output, search_result

    def create(self):
        (output, search_results) = self._command_and_parse(command=constants.GIT_SECRET_INIT_COMMAND,
                                                           regex=constants.GIT_SECRET_INIT_REGEX)

        if not search_results:
            raise GitSecretException("Error initializing gitsecret.  Error: %s" % output.stdout.decode("utf-8"))

    def tell(self, email: Optional[str] = None,
             gpg_path: Optional[str] = None):
        tell_command = constants.GIT_SECRET_TELL_COMMAND

        if email:
            tell_command = "{} {}".format(tell_command, email)
        else:
            tell_command = "{} {}".format(tell_command, "-m")

        if gpg_path:
            tell_command = "{} {} {}".format(tell_command, "-d", gpg_path)

        (output, search_results) = self._command_and_parse(command=tell_command,
                                                           regex=constants.GIT_SECRET_TELL_REGEX)

        if not search_results:
            raise GitSecretException("Error adding user to git secret.  Error: %s" % output.stdout.decode("utf-8"))
