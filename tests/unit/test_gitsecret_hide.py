import pytest
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_hide(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "done. all 11 files are hidden.\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    gen_gitsecret.hide()


def test_gitsecret_add_exception(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "None",
        'stderr': "git-secret: abort: no public keys for users found. run 'git secret tell email@address'.\n",
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    with pytest.raises(GitSecretException):
        gen_gitsecret.hide()
