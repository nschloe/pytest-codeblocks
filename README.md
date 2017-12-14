# excode

[![Build Status](https://travis-ci.org/nschloe/excode.svg?branch=master)](https://travis-ci.org/nschloe/excode)
[![codecov](https://codecov.io/gh/nschloe/excode/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/excode)
[![PyPi Version](https://img.shields.io/pypi/v/excode.svg)](https://pypi.python.org/pypi/excode)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/excode.svg?style=social&label=Stars)](https://github.com/nschloe/excode)

This is excode, a tool for extracting code blocks from markdown files.

For example, the command
```
excode input.md test.py
```
takes `input.md`,
````
Lorem ipsum
```python
some_code = 1
```
dolor sit amet.
````
and creates `test.py`,
```python
def test0():
    some_code = 1
    return
```
This can be used for automatically turning snippets from
a `README.md` into unit tests.

### Installation

excode is [available from the Python Package
Index](https://pypi.python.org/pypi/excode/), so simply
```
pip install -U excode
```
to install or upgrade.

### Testing

To run the unit tests, check out this repository and type
```
pytest
```

### Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:
    ```
    $ make publish
    ```

### License

excode is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
