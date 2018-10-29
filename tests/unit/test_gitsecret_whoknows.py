import pytest
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_whoknows(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "test1@gmail.com\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    assert gen_gitsecret.whoknows() == ["test1@gmail.com"]


def test_gitsecret_whoknows_multi(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "test1@gmail.com\ntest2@gmail.com",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    assert gen_gitsecret.whoknows() == ["test1@gmail.com", "test2@gmail.com"]


def test_gitsecret_whoknows_exception(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "Not a repo",
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    with pytest.raises(GitSecretException):
        gen_gitsecret.whoknows()
