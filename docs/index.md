# GitSecret

Python wrapper for [git-secret](http://git-secret.io/). 🔐🔐🔐

## Pre-requisites

### Install git secret
Install _git secret_ using your favorite [installation method](http://git-secret.io/installation).

### Generate a gpg key
Generate a gpg and passphrase using your e-mail of choice.

```bash
gpg --full-generate-key
```

## Using Git Secret

### Initialization
```python
from gitsecret import GitSecret

secret_repo = GitSecret("/path/to/repo")
secret_repo.create()

```

### Adding & removing users
```python
secret_repo.tell("my_email@email.com")
secret_repo.killperson("my_email@email.com")

# After removing a person, you need to hide the repo again. 
secret_repo.hide()
```

### Adding, encrpyting, and decrypting files
```python
PASSWORD = "mysecretpassword"

secret_repo.add("hello.txt")
secret_repo.hide()
secret_repo.reveal(PASSWORD)
```