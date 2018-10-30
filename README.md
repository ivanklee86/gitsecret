# GitSecret

[![CircleCI](https://circleci.com/gh/ivanklee86/gitsecret.svg?style=svg)](https://circleci.com/gh/ivanklee86/gitsecret) [![Coverage Status](https://coveralls.io/repos/github/ivanklee86/gitsecret/badge.svg)](https://coveralls.io/github/ivanklee86/gitsecret) [![Maintainability](https://api.codeclimate.com/v1/badges/7c39fafac8a7c66f3d13/maintainability)](https://codeclimate.com/github/ivanklee86/gitsecret/maintainability) [![PyPI version](https://badge.fury.io/py/gitsecret.svg)](https://badge.fury.io/py/gitsecret)

Python wrapper for [git-secret](http://git-secret.io/). 🔐🔐🔐

Check out the [documentation](https://ivanklee86.github.io/gitsecret/).

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