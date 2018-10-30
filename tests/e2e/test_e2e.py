import os
import shutil
from git import InvalidGitRepositoryError
from git.repo import Repo
import pytest
import tempfile
from gitsecret import GitSecret


PATH = "/Users/ivanlee/repos/sandbox/integration"


@pytest.fixture()
def gen_gitsecret():
    # Deletes and recreates PATH
    if os.path.isdir(PATH):
        shutil.rmtree(PATH)

    os.mkdir(PATH)

    Repo.init(PATH)
    yield GitSecret(PATH)

    # Clear files at end.
    shutil.rmtree(PATH)


def test_gitsecret_invalid_repo(gen_gitsecret):
    with pytest.raises(InvalidGitRepositoryError):
        with tempfile.TemporaryDirectory() as tempdir:
            GitSecret(tempdir)


def test_gitsecret_user_management(gen_gitsecret):
    gitsecret = gen_gitsecret
    gitsecret.create()
    gitsecret.tell()
    assert len(gitsecret.whoknows()) == 1
    gitsecret.killperson(gitsecret.whoknows()[0])


def test_gitsecret_files(gen_gitsecret):
    gitsecret = gen_gitsecret
    gitsecret.create()
    gitsecret.tell(email="test@test.com")
    assert len(gitsecret.whoknows()) == 1
    with open(os.path.join(PATH, "hello.txt"), "w+") as test_file:
        test_file.write("Hello!")
    with open(os.path.join(PATH, ".gitignore"), "a") as test_file:
        test_file.write("hello.txt")
    gitsecret.add("hello.txt")
    gitsecret.hide()
    gitsecret.reveal("test")
