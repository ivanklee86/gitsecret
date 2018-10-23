
class FakeCompletedProcess:
    def __init__(self, stdout, returncode):
        self.stdout = bytes(stdout, 'utf-8')
        self.returncode = returncode
