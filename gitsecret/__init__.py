import re
import shlex
import subprocess
from typing import Optional
import git


class GitSecretException(Exception):
    pass


class GitSecret():
    def __init__(self, path: str):
        # Class variables
        self.repo_path = path

        # Create gitpython.Repo object to ensure file is actually a repo.
        self.git_repo = git.Repo(self.repo_path)

    def create(self) -> None:
        init_command = shlex.split("git secret init")
        output = subprocess.run(args=init_command, capture_output=True, cwd=self.repo_path)
        search_result: list = None

        if output.returncode == 0:
            search_result = re.findall(r" created.\ncleaning up...\n$", output.stdout.decode("utf-8"))

        if not search_result or output.returncode > 0:
            raise GitSecretException("Error initializing gitsecret.  stdout: %s; stderr: %s" %
                                     (output.stdout.decode("utf-8"), output.stderr.decode("utf-8")))

    def tell(self, email: Optional[str] = None,
             gpg_path: Optional[str] = None) -> None:
        tell_command = shlex.split("git secret tell")
        search_result: list = None

        if email:
            tell_command.append(email)
        else:
            tell_command.append("-m")

        if gpg_path:
            tell_command.extend(["-d", gpg_path])

        output = subprocess.run(args=tell_command, capture_output=True, cwd=self.repo_path)

        if output.returncode == 0:
            search_result = re.findall(r" added as someone who know\(s\) the secret.", output.stdout.decode("utf-8"))

        if not search_result or output.returncode not in [0, 2]:
            raise GitSecretException("Error adding user.  stdout: %s; stderr: %s" %
                                     (output.stdout.decode("utf-8"), output.stderr.decode("utf-8")))

    def whoknows(self) -> list:
        whoknows_command = shlex.split("git secret whoknows")
        output = subprocess.run(args=whoknows_command, capture_output=True, cwd=self.repo_path)
        users: list = []

        if output.returncode == 0:
            users = [n for n in output.stdout.decode("utf-8").split("\n") if n]
        else:
            raise GitSecretException("Error getting list of user with access to secrets.  stdout: %s; stderr: %s" %
                                     (output.stdout.decode("utf-8"), output.stderr.decode("utf-8")))

        return users

    def killperson(self, email: str) -> None:
        killperson_command = shlex.split("git secret killperson")
        killperson_command.append(email)
        confirmation: list = []

        output = subprocess.run(args=killperson_command, capture_output=True, cwd=self.repo_path)

        if output.returncode == 0:
            confirmation = re.findall(r"do not have an access to the repository.", output.stdout.decode("utf-8"))

        if not confirmation or output.returncode > 0:
            raise GitSecretException("Error revoking user permissions.  stdout: %s; stderr: %s" %
                                     (output.stdout.decode("utf-8"), output.stderr.decode("utf-8")))

        # Add in re-hiding here.
