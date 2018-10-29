import re
import shlex
import subprocess
from typing import Optional, Tuple
import git


class GitSecretException(Exception):
    pass


class GitSecret():
    def __init__(self, path: str):
        # Class variables
        self.repo_path = path

        # Create gitpython.Repo object to ensure file is actually a repo.
        self.git_repo = git.Repo(self.repo_path)

    def _command_and_parse(self,
                           command: list,
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
        search_result: list = []

        # _Run command and parse_
        output = subprocess.run(args=command, capture_output=True, cwd=self.repo_path)

        if regex and output.returncode == 0:
            search_result = re.findall(regex, output.stdout.decode("utf-8"))

        if output.returncode != 0:
            raise GitSecretException("Error running git secret command.  stdout: %s; stderr: %s" %
                                     (output.stdout.decode("utf-8"), output.stderr.decode("utf-8")))

        return output, search_result

    def _command_and_split(self,
                           command: list):
        output = subprocess.run(args=command, capture_output=True, cwd=self.repo_path)
        parsed_list: list = []

        if output.returncode == 0:
            parsed_list = [n for n in output.stdout.decode("utf-8").split("\n") if n]
        else:
            raise GitSecretException("Error running command.  stdout: %s; stderr: %s" %
                                     (output.stdout.decode("utf-8"), output.stderr.decode("utf-8")))

        return parsed_list

    def create(self) -> None:
        init_command = shlex.split("git secret init")
        init_regex = r" created.\ncleaning up...\n$"
        self._command_and_parse(init_command, init_regex)

    def tell(self, email: Optional[str] = None,
             gpg_path: Optional[str] = None) -> None:
        tell_command = shlex.split("git secret tell")
        tell_regex = r" added as someone who know\(s\) the secret."

        if email:
            tell_command.append(email)
        else:
            tell_command.append("-m")

        if gpg_path:
            tell_command.extend(["-d", gpg_path])

        self._command_and_parse(tell_command, tell_regex)

    def whoknows(self) -> list:
        whoknows_command = shlex.split("git secret whoknows")

        return self._command_and_split(whoknows_command)

    def killperson(self, email: str) -> None:
        killperson_command = shlex.split("git secret killperson")
        killperson_command.append(email)
        killperson_regex = r"do not have an access to the repository."

        self._command_and_parse(killperson_command, killperson_regex)

        # Todo: Add in re-hiding here.

    def add(self, filename: str) -> None:
        istracked_command = shlex.split("git ls-files")
        files = self._command_and_split(istracked_command)
        file_check = [n for n in files if filename in files]

        if file_check:
            raise GitSecretException("File isn't ignored via .gitignore and cannot be added to git secret!")

        add_command = shlex.split("git secret add")
        add_command.append(filename)
        add_regex = r" item(s) added."
        self._command_and_parse(add_command, add_regex)

    def hide(self) -> None:
        hide_command = shlex.split("git secret hide")
        hide_regex = r"done. all [0-1]+ files are hidden."

        self._command_and_parse(hide_command, hide_regex)
