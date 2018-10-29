import pytest
import gitsecret
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_killperson(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "removed keys.\nnow [ivanklee86@gmail.com] do not have an access to the repository.\nmake sure to hide the existing secrets again\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    gen_gitsecret.killperson(email="test@test.com")
    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "killperson", "test@test.com"]


def test_gitsecret_killperson_exception(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': "None",
        'stderr': 'gpg: key "ivanklee86@gmail.com" not found: Not found\ngpg: ivanklee86@gmail.com: delete key failed: Not found\n',
        'returncode': 2
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    with pytest.raises(GitSecretException):
        gen_gitsecret.killperson(email="test@test.com")
