import pytest
import gitsecret
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_list(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "\nhello.txt\nhello1.txt\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    assert gen_gitsecret.list() == ["hello.txt", "hello1.txt"]

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "list"]


def test_gitsecret_list_exception(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "None",
        'stderr': "git-secret: abort: /Users/ivanlee/repos/sandbox/box5/.gitsecret/paths/mapping.cfg is missing",
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    with pytest.raises(GitSecretException):
        gen_gitsecret.list()
