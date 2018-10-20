import os
from gitsecret.utils import _command_and_parse


def test_run_command():
    (output, _) = _command_and_parse("ls -l")

    assert output.returncode == 0
    assert "total" in output.stdout.decode("utf-8")


def test_run_command_with_regex():
    regex = "\d+:\d+"
    (output, search_results) = _command_and_parse("ls -l", regex)

    assert output.returncode == 0
    assert len(search_results) >= 1


def test_run_command_with_location():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    (output, search_results) = _command_and_parse("ls -l", location=dir_path)

    assert output.returncode == 0
    assert "test_utils.py" in output.stdout.decode("utf-8")
