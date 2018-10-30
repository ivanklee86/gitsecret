import pytest
import gitsecret
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_create(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "'/Users/ivanlee/repos/sandbox/box2/.gitsecret/' created.\ncleaning up...\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)
    gen_gitsecret.create()

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "init"]


def test_gitsecret_create_alreadycreated(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "'git-secret: abort: already inited.\n'",
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)
    with pytest.raises(GitSecretException):
        gen_gitsecret.create()
