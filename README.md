# excode

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/excode/ci?style=flat-square)](https://github.com/nschloe/excode/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/excode.svg?style=flat-square)](https://codecov.io/gh/nschloe/excode)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/excode.svg?style=flat-square)](https://pypi.org/pypi/excode/)
[![PyPi Version](https://img.shields.io/pypi/v/excode.svg?style=flat-square)](https://pypi.org/project/excode)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/excode.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/excode)
[![PyPi downloads](https://img.shields.io/pypi/dm/excode.svg?style=flat-square)](https://pypistats.org/packages/excode)

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

#### Filter code blocks

The command
```
excode -f "python,test" input.md test.py
```
only extracts code blocks with the header
````
```python,test
some_code()
```
````
(Appending anything to `<lang_name>` in the markdown header doesn't influence
the syntax highlighting.)

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

### License

excode is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
