from git.repo import Repo
import pytest
import tempfile
import gitsecret
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess


@pytest.fixture()
def gen_gitsecret():
    with tempfile.TemporaryDirectory() as tempdir:
        Repo.init(tempdir)
        yield gitsecret.GitSecret(tempdir)


def test_gitsecret_create(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "'/Users/ivanlee/repos/sandbox/box2/.gitsecret/' created.\ncleaning up...\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)
    gen_gitsecret.create()

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "init"]


def test_gitsecret_create_alreadycreated(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "'git-secret: abort: already inited.\n'",
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)
    with pytest.raises(GitSecretException):
        gen_gitsecret.create()


def test_gitsecret_tell(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "gpg: keybox '/Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/pubring.kbx' created\ngpg: /Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/trustdb.gpg: trustdb created\ndone. ivanklee86@gmail.com added as someone who know(s) the secret.\ncleaning up...",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    gen_gitsecret.tell(email="test@test.com")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "tell", "test@test.com"]
