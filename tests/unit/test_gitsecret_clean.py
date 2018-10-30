import gitsecret
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_clean(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "\ncleaning:\n/Users/ivanlee/repos/sandbox/box5/hello.txt.secret\n\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    assert gen_gitsecret.clean()[0] == "/Users/ivanlee/repos/sandbox/box5/hello.txt.secret"

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "clean", "-v"]


def test_gitsecret_clean_noreturn(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "\ncleaning:\n\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    assert len(gen_gitsecret.clean()) == 0
