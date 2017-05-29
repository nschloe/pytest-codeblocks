# code_extract

[![Build Status](https://travis-ci.org/nschloe/code_extract.svg?branch=master)](https://travis-ci.org/nschloe/code_extract)
[![codecov](https://codecov.io/gh/nschloe/code_extract/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/code_extract)
[![PyPi Version](https://img.shields.io/pypi/v/code_extract.svg)](https://pypi.python.org/pypi/code_extract)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/code_extract.svg?style=social&label=Star&maxAge=2592000)](https://github.com/nschloe/code_extract)

This is code_extract, a Python tool for extracting code blocks markdown files.

For example, the command
```
code_extract input.md test
```
turns
extracts `some_code = 1` from
````
Lorem ipsum
```python
some_code = 1
```
````
and places it in `test0.py`.

This can be used, for example, for automatically turning snippets from
a `README.md` into unit tests.

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

code_extract is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
