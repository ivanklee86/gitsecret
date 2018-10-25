from git import InvalidGitRepositoryError
from git.repo import Repo
import pytest
import tempfile
from gitsecret import GitSecret


@pytest.fixture()
def gen_gitsecret():
    with tempfile.TemporaryDirectory() as tempdir:
        Repo.init(tempdir)
        yield GitSecret(tempdir)


def test_gitsecret_invalid_repo(gen_gitsecret):
    with pytest.raises(InvalidGitRepositoryError):
        with tempfile.TemporaryDirectory() as tempdir:
            GitSecret(tempdir)


def test_gitsecret(gen_gitsecret):
    gitsecret = gen_gitsecret
    gitsecret.create()
    gitsecret.tell()
    print("Hello!")
