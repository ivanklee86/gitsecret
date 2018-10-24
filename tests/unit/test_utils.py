from git import Repo
import pytest
import tempfile
import gitsecret


@pytest.fixture()
def gen_gitsecret():
    with tempfile.TemporaryDirectory() as tempdir:
        Repo.init(tempdir)
        yield gitsecret.GitSecret(tempdir)


def test_run_command(gen_gitsecret):
    (output, _) = gen_gitsecret._command_and_parse("ls -lrta")

    assert output.returncode == 0
    assert "total" in output.stdout.decode("utf-8")


def test_run_command_with_regex(gen_gitsecret):
    regex = "\d+:\d+"
    (output, search_results) = gen_gitsecret._command_and_parse("ls -lrta", regex)

    assert output.returncode == 0
    assert len(search_results) >= 1
