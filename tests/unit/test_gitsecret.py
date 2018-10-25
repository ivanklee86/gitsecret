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


def test_gitsecret_tell_noemail(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "gpg: keybox '/Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/pubring.kbx' created\ngpg: /Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/trustdb.gpg: trustdb created\ndone. ivanklee86@gmail.com added as someone who know(s) the secret.\ncleaning up...",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    gen_gitsecret.tell()

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "tell", "-m"]


def test_gitsecret_tell_path(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "gpg: keybox '/Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/pubring.kbx' created\ngpg: /Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/trustdb.gpg: trustdb created\ndone. ivanklee86@gmail.com added as someone who know(s) the secret.\ncleaning up...",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    gen_gitsecret.tell(gpg_path="/random/path")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "tell", "-m", "-d", "/random/path"]


def test_gitsecret_tell_exception(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "some",
        'stderr': 'error',
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    with pytest.raises(GitSecretException):
        gen_gitsecret.tell(gpg_path="/random/path")


def test_gitsecret_whoknows(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "test1@gmail.com\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    assert gen_gitsecret.whoknows() == ["test1@gmail.com"]


def test_gitsecret_whoknows_multi(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "test1@gmail.com\ntest2@gmail.com",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    assert gen_gitsecret.whoknows() == ["test1@gmail.com", "test2@gmail.com"]


def test_gitsecret_whoknows_exception(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "Not a repo",
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    with pytest.raises(GitSecretException):
        gen_gitsecret.whoknows()


def test_gitsecret_killperson(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "removed keys.\nnow [ivanklee86@gmail.com] do not have an access to the repository.\nmake sure to hide the existing secrets again\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    gen_gitsecret.killperson(email="test@test.com")
    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "killperson", "test@test.com"]


def test_gitsecret_killperson_exception(gen_gitsecret, mocker):
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "None",
        'stderr': 'gpg: key "ivanklee86@gmail.com" not found: Not found\ngpg: ivanklee86@gmail.com: delete key failed: Not found\n',
        'returncode': 2
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    with pytest.raises(GitSecretException):
        gen_gitsecret.killperson(email="test@test.com")
