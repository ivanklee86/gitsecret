import pytest
import gitsecret
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_remove(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "hello.txt -> hello.txt -> /Users/ivanlee/repos/sandbox/box5/hello.txt\nremoved from index.\nensure that files: [hello.txt] are now not ignored.\ncleaning up...\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    gen_gitsecret.remove(filename="hello.txt")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "remove", "hello.txt"]


def test_gitsecret_reveal_overwrite(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "hello.txt -> hello.txt -> /Users/ivanlee/repos/sandbox/box5/hello.txt\nremoved from index.\nensure that files: [hello.txt] are now not ignored.\ncleaning up...\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    gen_gitsecret.remove(filename="hello.txt",
                         delete_existing=True)

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "remove", "-c", "hello.txt"]


def test_gitsecret_reveal_exception(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "None",
        'stderr': "hello.txt1 ->  -> /Users/ivanlee/repos/sandbox/box5/\ngit-secret: abort: file not found: hello.txt1",
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    with pytest.raises(GitSecretException):
        gen_gitsecret.remove(filename="hello.txt")
