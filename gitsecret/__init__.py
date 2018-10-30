import re
import shlex
import subprocess
from typing import Optional, Tuple, List
import git


class GitSecretException(Exception):
    pass


class GitSecret():
    def __init__(self, path: str):
        """
        This initializes the GitSecret wrapper class.

        :param path: Path to git repo
        """
        # Class variables
        self.repo_path = path

        # Create gitpython.Repo object to ensure file is actually a repo.
        self.git_repo = git.Repo(self.repo_path)

    def _command_and_parse(self,
                           command: list,  # pylint: disable=E0601
                           regex: Optional[str] = None) -> Tuple[subprocess.CompletedProcess, list]:
        """
        A (inflexible, implementation-focused) centralized method to run a method and optionally applies a regex to the
        stdout.

        :param command: Command to run, use shlex.split() + add arguments
        :param regex: Optional, regex string
        :param location: Optional, location to run command
        :return: [CompletedProcess, list of results form regex]
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
        """
        A (inflexible, implementation-focused) centralized method to run a method and split result based on \n

        :param command: Command to run, use shlex.split() + add arguments
        :return: List parsed from stdout
        """
        output = subprocess.run(args=command, capture_output=True, cwd=self.repo_path)
        parsed_list: list = []

        if output.returncode == 0:
            parsed_list = [n for n in output.stdout.decode("utf-8").split("\n") if n]
        else:
            raise GitSecretException("Error running command.  stdout: %s; stderr: %s" %
                                     (output.stdout.decode("utf-8"), output.stderr.decode("utf-8")))

        return parsed_list

    def create(self) -> None:
        """
        Initializes git secret.

        :return: None
        """
        init_command = shlex.split("git secret init")
        init_regex = r" created.\ncleaning up...\n$"
        self._command_and_parse(init_command, init_regex)

    def tell(self, email: Optional[str] = None,
             gpg_path: Optional[str] = None) -> None:
        """
        Adds a user's gpg key to git secret.

        :param email: Email of user's gpg key
        :param gpg_path: Optional, path to gpg key if in custom location
        :return:
        """
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
        """
        Lists emails with access to secrets.

        :return: List of gpg emails
        """
        whoknows_command = shlex.split("git secret whoknows")

        return self._command_and_split(whoknows_command)

    def killperson(self, email: str) -> None:
        """
        Removes a person's ability to decrypt secrets.

        NOTE: This must be followed by a GitSecret.hide() call to re-encrypt secrets.

        :param email: Email associated with gpg key
        :return:
        """
        killperson_command = shlex.split("git secret killperson")
        killperson_command.append(email)
        killperson_regex = r"do not have an access to the repository."

        self._command_and_parse(killperson_command, killperson_regex)

    def add(self, file_path: str,
            autoadd: bool = False) -> None:
        """
        Adds a file to git secret's list of files to encrypt.

        NOTE:  THis file must be covered by your .gitignore file or this action will fail!  You can
        also turn on the 'autoadd' flag to let git secret do this for you.

        :param file_path: Path to file
        :param autoadd: Optional, whether git secret will automatically add file to .gitignore
        :return:
        """
        istracked_command = shlex.split("git ls-files")

        add_command = shlex.split("git secret add")
        add_regex = r" item(s) added."

        if not autoadd:
            files = self._command_and_split(istracked_command)
            file_check = [n for n in files if file_path in files]

            if file_check:
                raise GitSecretException("File isn't ignored via .gitignore and cannot be added to git secret!")
        else:
            add_command.append("-i")

        add_command.append(file_path)

        self._command_and_parse(add_command, add_regex)

    def hide(self, clean_encrypted: bool = False,
             clean_unencrypted: bool = False) -> None:
        """
        Creates encrypted version of files tracked in git secret's file list.

        :param clean_encrypted: Optional, deletes encrypted files before creating new ones.
        :param clean_unencrypted: Optional, deletes unencrypted files after encryption.
        :return:
        """
        hide_command = shlex.split("git secret hide")
        hide_regex = r"done. all [0-1]+ files are hidden."

        if clean_encrypted:
            hide_command.append("-c")

        if clean_unencrypted:
            hide_command.append("-d")

        self._command_and_parse(hide_command, hide_regex)

    def reveal(self, password: str,
               gpg_path: Optional[str] = None,
               overwrite: bool = False) -> None:
        """
        Decrypts all encrypted files using user's private gpg key.

        :param password: gpg key's passphrase
        :param gpg_path: Optional, path to gpg key if in custom location
        :param overwrite: Optional, forces overwrite of existing files
        :return:
        """
        reveal_command = shlex.split("git secret reveal")
        reveal_regex = r"done. all [0-1]+ files are revealed."

        reveal_command.extend(["-p", password])

        if overwrite:
            reveal_command.append("-f")

        if gpg_path:
            reveal_command.extend(["-d", gpg_path])

        self._command_and_parse(reveal_command, reveal_regex)

    def remove(self, file_path: str,
               delete_existing: bool = False):
        """
        Removes a file from git secret's file list.

        :param file_path: Path to file to remove
        :param delete_existing: Optional, deletes existing encrypted file
        :return:
        """
        remove_command = shlex.split("git secret remove")
        remove_regex = r"ensure that files: \[.+\] are now not ignored."

        if delete_existing:
            remove_command.append("-c")

        remove_command.append(file_path)

        self._command_and_parse(remove_command, remove_regex)

    def clean(self) -> Optional[List]:
        """
        Removes all encrypted files.

        :return: list of files removed
        """
        clean_command = shlex.split("git secret clean -v")

        return self._command_and_split(clean_command)[1:]

    def list(self) -> Optional[List]:
        """
        Prints all files git secret is tracking.

        :return: list of tracked files
        """
        list_command = shlex.split("git secret list")

        return self._command_and_split(list_command)[:]

    def changes(self, password: str, file_path: Optional[str] = None, gpg_path: Optional[str] = None) -> str:
        """
        Returns a diff of encrypted files.

        :param password: gpg key's passphrase
        :param file_path: Optional, path to file.  If not present, will return diff of all tracked files.
        :param gpg_path: Optional, path to gpg key if in custom location
        :return:
        """
        changes_command = shlex.split("git secret changes")

        if gpg_path:
            changes_command.extend(["-d", gpg_path])

        changes_command.extend(["-p", password])

        if file_path:
            changes_command.append(file_path)

        output = subprocess.run(args=changes_command, capture_output=True, cwd=self.repo_path)

        if output.returncode != 0:
            raise GitSecretException("Error running git secret command.  stdout: %s; stderr: %s" %
                                     (output.stdout.decode("utf-8"), output.stderr.decode("utf-8")))

        return str(output.stdout.decode("utf-8"))
