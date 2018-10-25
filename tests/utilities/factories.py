
class FakeCompletedProcess:
    def __init__(self, stdout, returncode, stderr="None"):
        self.stdout = bytes(stdout, 'utf-8')
        self.stderr = bytes(stderr, 'utf-8')
        self.returncode = returncode
