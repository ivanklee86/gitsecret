import pytest
import gitsecret
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_reveal(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "done. all 10 files are revealed.\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    gen_gitsecret.reveal(password="test")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "reveal", "-p", "test"]


def test_gitsecret_reveal_overwrite(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "done. all 10 files are revealed.\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    gen_gitsecret.reveal(password="test",
                         overwrite=True)

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "reveal", "-p", "test", "-f"]


def test_gitsecret_reveal_gpg_path(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "done. all 10 files are revealed.\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    gen_gitsecret.reveal(password="test",
                         gpg_path="/path/to/key")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "reveal", "-p", "test", "-d", "/path/to/key"]


def test_gitsecret_reveal_all(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "done. all 10 files are revealed.\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    gen_gitsecret.reveal(password="test",
                         overwrite=True,
                         gpg_path="/path/to/key")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "reveal", "-p", "test", "-f", "-d", "/path/to/key"]


def test_gitsecret_reveal_exception(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "None",
        'stderr': "git-secret: abort: no public keys for users found. run 'git secret tell email@address'.\n",
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    with pytest.raises(GitSecretException):
        gen_gitsecret.reveal("test1")
