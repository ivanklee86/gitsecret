from git.repo import Repo
import pytest
import tempfile
from gitsecret import GitSecret
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess


@pytest.fixture()
def gen_gitsecret():
    with tempfile.TemporaryDirectory() as tempdir:
        Repo.init(tempdir)
        yield GitSecret(tempdir)


def test_gitsecret_create(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "'/Users/ivanlee/repos/sandbox/box2/.gitsecret/' created.\ncleaning up...\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.utils.subprocess.run', return_value=shell_cmd)
    gen_gitsecret.create()


def test_gitsecret_create_alreadycreated(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "'git-secret: abort: already inited.\n'",
        'returncode': 1
    })

    mocker.patch('gitsecret.utils.subprocess.run', return_value=shell_cmd)
    with pytest.raises(GitSecretException):
        gen_gitsecret.create()
