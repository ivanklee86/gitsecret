import pytest
import gitsecret
from gitsecret import GitSecretException
from tests.utilities.factories import FakeCompletedProcess
from tests.utilities.fixtures import gen_gitsecret  # noqa: F401


def test_gitsecret_changes(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "\nchanges in /Users/ivanlee/repos/sandbox/integration/hello.txt:\n--- /dev/fd/63	2018-10-30 03:12:54.000000000 -0400\n+++ /Users/ivanlee/repos/sandbox/integration/hello.txt	2018-10-30 03:12:54.000000000 -0400\n@@ -1 +1 @@-Hello!\n+Hello!Hello again!\n\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    assert "Hello again!" in gen_gitsecret.changes("test")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "changes", "-p", "test"]


def test_gitsecret_changes_path(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "\nchanges in /Users/ivanlee/repos/sandbox/integration/hello.txt:\n--- /dev/fd/63	2018-10-30 03:12:54.000000000 -0400\n+++ /Users/ivanlee/repos/sandbox/integration/hello.txt	2018-10-30 03:12:54.000000000 -0400\n@@ -1 +1 @@-Hello!\n+Hello!Hello again!\n\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    assert "Hello again!" in gen_gitsecret.changes(password="test",
                                                   file_path="/path/to/file")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "changes", "-p", "test", "/path/to/file"]


def test_gitsecret_changes_gpgpath(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "\nchanges in /Users/ivanlee/repos/sandbox/integration/hello.txt:\n--- /dev/fd/63	2018-10-30 03:12:54.000000000 -0400\n+++ /Users/ivanlee/repos/sandbox/integration/hello.txt	2018-10-30 03:12:54.000000000 -0400\n@@ -1 +1 @@-Hello!\n+Hello!Hello again!\n\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    assert "Hello again!" in gen_gitsecret.changes(password="test",
                                                   gpg_path="/path/to/key")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "changes", "-d", "/path/to/key", "-p", "test"]


def test_gitsecret_changes_all(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "\nchanges in /Users/ivanlee/repos/sandbox/integration/hello.txt:\n--- /dev/fd/63	2018-10-30 03:12:54.000000000 -0400\n+++ /Users/ivanlee/repos/sandbox/integration/hello.txt	2018-10-30 03:12:54.000000000 -0400\n@@ -1 +1 @@-Hello!\n+Hello!Hello again!\n\n",
        'returncode': 0
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    assert "Hello again!" in gen_gitsecret.changes(password="test",
                                                   gpg_path="/path/to/key",
                                                   file_path="/path/to/file")

    assert gitsecret.subprocess.run.assert_called_once
    assert gitsecret.subprocess.run.call_args[1]['args'] == ["git", "secret", "changes", "-d", "/path/to/key", "-p", "test", "/path/to/file"]


def test_gitsecret_changes_exception(gen_gitsecret, mocker):  # noqa: F811
    shell_command = FakeCompletedProcess(**{
        'stdout': "None",
        'stderr': "git-secret: abort: /Users/ivanlee/repos/sandbox/box5/.gitsecret/paths/mapping.cfg is missing",
        'returncode': 1
    })

    mocker.patch('gitsecret.subprocess.run', return_value=shell_command)

    with pytest.raises(GitSecretException):
        gen_gitsecret.changes("test")
