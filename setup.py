import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

APP = ['FileSorter.py']
DATA_FILES = ['cipher.pyc']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'iconfile': 'profile_pic.icns',
    'packages': ['rumps', 'cryptography', 'cffi']
}
CLASSIFIERS = ["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent"]

setuptools.setup(
    name="FileSorter",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    version="0.0.1",
    author="Daniel Alexander Ross Evans",
    author_email="me@daredoes.work",
    description="A rumps tool for keeping folders organized.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daredoes/FileSorter",
    packages=setuptools.find_packages(),
    classifiers=CLASSIFIERS,
)