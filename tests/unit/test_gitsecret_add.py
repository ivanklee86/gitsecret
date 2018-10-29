import pytest
import gitsecret
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_add_nogitignore(gen_gitsecret, mocker):  # noqa: F811
    shell_cmd = FakeCompletedProcess(**{
        'stdout': ".gitignore\n.gitsecret/keys/mapping.cfg\n.gitsecret/keys/pubring.kbx\n.gitsecret/keys/trustdb.gpg\n.gitsecret/paths/mapping.cfg\n\nhello.txt",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_cmd)

    with pytest.raises(GitSecretException):
        gen_gitsecret.add("hello.txt")


def test_gitsecret_add(gen_gitsecret, mocker):  # noqa: F811
    file_check = FakeCompletedProcess(**{
        'stdout': ".gitignore\n.gitsecret/keys/mapping.cfg\n.gitsecret/keys/pubring.kbx\n.gitsecret/keys/trustdb.gpg\n.gitsecret/paths/mapping.cfg\n",
        'returncode': 0
    })

    git_secret_add_output = FakeCompletedProcess(**{
        'stdout': "1 item(s) added.\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=file_check)
    mocker.patch('gitsecret.subprocess.run', return_value=git_secret_add_output)

    gen_gitsecret.add("hello.txt")
    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "add", "hello.txt"]


def test_gitsecret_add_autoadd(gen_gitsecret, mocker):  # noqa: F811
    git_secret_add_output = FakeCompletedProcess(**{
        'stdout': "1 item(s) added.\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=git_secret_add_output)

    gen_gitsecret.add("hello.txt", autoadd=True)
    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "add", "-i", "hello.txt"]


def test_gitsecret_add_exception(gen_gitsecret, mocker):  # noqa: F811
    file_check = FakeCompletedProcess(**{
        'stdout': ".gitignore\n.gitsecret/keys/mapping.cfg\n.gitsecret/keys/pubring.kbx\n.gitsecret/keys/trustdb.gpg\n.gitsecret/paths/mapping.cfg\n",
        'returncode': 0
    })

    git_secret_add_output = FakeCompletedProcess(**{
        'stdout': "\n",
        "stderr": "git-secret: abort: file not found: hello.txt1",
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=file_check)
    mocker.patch('gitsecret.subprocess.run', return_value=git_secret_add_output)

    with pytest.raises(GitSecretException):
        gen_gitsecret.add("hello.txt1")
