**pytest-codeblocks is deprecated. Use
[pytest-codeblocks](https://pypi.org/project/pytest-codeblocks) instead.**

---

# pytest-codeblocks

[![PyPi Version](https://img.shields.io/pypi/v/pytest-codeblocks.svg?style=flat-square)](https://pypi.org/project/pytest-codeblocks/)
[![Anaconda Cloud](https://anaconda.org/conda-forge/pytest-codeblocks/badges/version.svg?=style=flat-square)](https://anaconda.org/conda-forge/pytest-codeblocks/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-codeblocks.svg?style=flat-square)](https://pypi.org/project/pytest-codeblocks/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pytest-codeblocks.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/pytest-codeblocks)
[![PyPi downloads](https://img.shields.io/pypi/dm/pytest-codeblocks.svg?style=flat-square)](https://pypistats.org/packages/pytest-codeblocks)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/pytest-codeblocks/ci?style=flat-square)](https://github.com/nschloe/pytest-codeblocks/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/pytest-codeblocks.svg?style=flat-square)](https://app.codecov.io/gh/nschloe/pytest-codeblocks)
[![LGTM](https://img.shields.io/lgtm/grade/python/github/nschloe/pytest-codeblocks.svg?style=flat-square)](https://lgtm.com/projects/g/nschloe/pytest-codeblocks)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

This is pytest-codeblocks, a tool for extracting code blocks from Markdown files and to create
tests from them.

Install with
```
pip install pytest-codeblocks
```
and create tests for [pytest](https://docs.pytest.org/en/stable/) with
```python
import pytest_codeblocks

test_readme = pytest_codeblocks.pytests_from_file("README.md")
```
The `test_readme` variable is really a decorated function that pytest will pick up and
turn into tests.
```
tests/test_readme.py .............                    [100%]
```


#### Skipping code blocks
If you don't want all code blocks to be extracted, you can **filter by syntax**
```python
pytest - codeblocks.pytests_from_file("README.md", syntax_filter="python")
```
or prefix your code block in the Markdown file with a `pytest-codeblocks:skip` comment
````markdown
Lorem ipsum
<!--pytest-codeblocks:skip-->
```python
foo + bar  # not working
```
dolor sit amet.
````


#### Merging code blocks
Broken-up code blocks can be merged into one with the `pytest-codeblocks:cont` prefix
````markdown
Lorem ipsum
```
a = 1
```
dolor sit amet
<!--pytest-codeblocks:cont-->
```
# this would otherwise fail since `a` is not defined
a + 1
```
````


#### Expected output
You can also define the expected output of a code block:
````markdown
This
```
print(1 + 3)
```
gives
<!--pytest-codeblocks:expected-output-->
```
5
```
````


#### Expected errors
Some code blocks are expected to give errors. You can verify this with
````markdown
The following gives an error:
<!--pytest-codeblocks:expect-exception-->
```python
1 / 0
```
````


### License
This software is published under the [MIT
license](https://en.wikipedia.org/wiki/MIT_License).
