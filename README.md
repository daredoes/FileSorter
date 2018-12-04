# GitReviewing

A rumps tool to keep up to date with Pull Requests.

---

## Getting An Access Token

[Generate a personal access token](https://github.com/settings/tokens)  with all permissions for repo to for all repos, or just `public_repo` for public repos, and `read:user`.

This token can be input into GitReviewing through the Menubar

---

## Making a cipher

For "Security" (aka not plain-text), GitReviewing uses a cipher key stored as a compiled pyc file.

If you have a better solution, fork and submit a pull request.

To generate a cipher, open a python shell and execute the following:
```python
from cryptography.fernet import Fernet
Fernet.generate_key()
```
which will generate a key such as: `b's7TbWhTLwscwOa02cEZD0IgTKzWil6Wo2yz54hDaAEo='` (Don't use this one!)

To save the cipher, create a file at the root called `cipher.py` with the contents
```python
cipher = b's7TbWhTLwscwOa02cEZD0IgTKzWil6Wo2yz54hDaAEo='
```

Then compile it to a `.pyc` file with the command 
```
python -m py_compile cipher.py
```  

This will put the file in a folder called `__pycache__`, move the file from there to the root of the repository, and change the name to `cipher.pyc`.

Then delete `cipher.py`
