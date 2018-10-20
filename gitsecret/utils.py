import re
import shlex
import subprocess
from typing import Optional, Tuple


def _command_and_parse(command: str,
                       regex: Optional[str] = None,
                       location: Optional[str] = None) -> Tuple[subprocess.CompletedProcess, list]:
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
    output = subprocess.run(args=parsed_command, capture_output=True, cwd=location)

    if regex and output.returncode == 0:
        search_result = re.findall(regex, output.stdout.decode("utf-8"))

    return output, search_result
