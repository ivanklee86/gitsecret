import pytest
import gitsecret
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_tell(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "gpg: keybox '/Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/pubring.kbx' created\ngpg: /Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/trustdb.gpg: trustdb created\ndone. ivanklee86@gmail.com added as someone who know(s) the secret.\ncleaning up...",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    gen_gitsecret.tell(email="test@test.com")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "tell", "test@test.com"]


def test_gitsecret_tell_noemail(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "gpg: keybox '/Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/pubring.kbx' created\ngpg: /Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/trustdb.gpg: trustdb created\ndone. ivanklee86@gmail.com added as someone who know(s) the secret.\ncleaning up...",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    gen_gitsecret.tell()

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "tell", "-m"]


def test_gitsecret_tell_path(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "gpg: keybox '/Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/pubring.kbx' created\ngpg: /Users/ivanlee/repos/sandbox/box2/.gitsecret/keys/trustdb.gpg: trustdb created\ndone. ivanklee86@gmail.com added as someone who know(s) the secret.\ncleaning up...",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    gen_gitsecret.tell(gpg_path="/random/path")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "tell", "-m", "-d", "/random/path"]


def test_gitsecret_tell_exception(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "some",
        'stderr': 'error',
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    with pytest.raises(GitSecretException):
        gen_gitsecret.tell(gpg_path="/random/path")
