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

    def create(self):
        init_command = shlex.split("git secret init")
        output = subprocess.run(args=init_command, capture_output=True, cwd=self.repo_path)
        search_result = None

        if output.returncode == 0:
            search_result = re.findall(r" created.\ncleaning up...\n$", output.stdout.decode("utf-8"))

        if not search_result or output.returncode > 0:
            raise GitSecretException("Error initializing gitsecret.  stdout: %s; stderr: %s" %
                                     (output.stdout.decode("utf-8"), output.stderr.decode("utf-8")))

    def tell(self, email: Optional[str] = None,
             gpg_path: Optional[str] = None):
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
        elif output.returncode == 2:
            search_result = re.findall(r"trustdb created", output.stderr.decode("utf-8"))

        if not search_result or output.returncode not in [0, 2]:
            raise GitSecretException("Error adding user.  stdout: %s; stderr: %s" %
                                     (output.stdout.decode("utf-8"), output.stderr.decode("utf-8")))
