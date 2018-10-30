from git.repo import Repo
import pytest
import tempfile
import gitsecret


@pytest.fixture()
def gen_gitsecret():
    with tempfile.TemporaryDirectory() as tempdir:
        Repo.init(tempdir)
        yield gitsecret.GitSecret(tempdir)
