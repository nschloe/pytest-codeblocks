# excode

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/excode/ci?style=flat-square)](https://github.com/nschloe/excode/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/excode.svg?style=flat-square)](https://codecov.io/gh/nschloe/excode)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/excode.svg?style=flat-square)](https://pypi.org/pypi/excode/)
[![PyPi Version](https://img.shields.io/pypi/v/excode.svg?style=flat-square)](https://pypi.org/project/excode)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/excode.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/excode)
[![PyPi downloads](https://img.shields.io/pypi/dm/excode.svg?style=flat-square)](https://pypistats.org/packages/excode)

This is excode, a tool for extracting code blocks from markdown files. This can be used
for testing code in your README files.

Install with
```
pip install excode
```
and use as
```
import excode
import pytest

@pytest.mark.parametrize("string", excode.extract("README.md"))
def test_readme(string):
    exec(string)
```

If you don't want all code blocks to be extracted, you can filter by syntax
```python
excode.extract("README.md", syntax_filter="python")
```
or
```python
excode.extract("README.md", skip=[2, 3, 5])
```
(or both).

### Testing

To run the unit tests, check out this repository and type
```
pytest
```

### License

excode is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
