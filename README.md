**exdown is deprecated. Use
[pytest-codeblocks](https://pypi.org/project/pytest-codeblocks) instead.**

---

# exdown

[![PyPi Version](https://img.shields.io/pypi/v/exdown.svg?style=flat-square)](https://pypi.org/project/exdown/)
[![Anaconda Cloud](https://anaconda.org/conda-forge/exdown/badges/version.svg?=style=flat-square)](https://anaconda.org/conda-forge/exdown/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/exdown.svg?style=flat-square)](https://pypi.org/project/exdown/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/exdown.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/exdown)
[![PyPi downloads](https://img.shields.io/pypi/dm/exdown.svg?style=flat-square)](https://pypistats.org/packages/exdown)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/exdown/ci?style=flat-square)](https://github.com/nschloe/exdown/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/exdown.svg?style=flat-square)](https://app.codecov.io/gh/nschloe/exdown)
[![LGTM](https://img.shields.io/lgtm/grade/python/github/nschloe/exdown.svg?style=flat-square)](https://lgtm.com/projects/g/nschloe/exdown)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

This is exdown, a tool for extracting code blocks from Markdown files and to create
tests from them.

Install with
```
pip install exdown
```
and create tests for [pytest](https://docs.pytest.org/en/stable/) with
```python
import exdown

test_readme = exdown.pytests_from_file("README.md")
```
The `test_readme` variable is really a decorated function that pytest will pick up and
turn into tests.
```
tests/test_readme.py .............                    [100%]
```


#### Skipping code blocks
If you don't want all code blocks to be extracted, you can **filter by syntax**
```python
exdown.pytests_from_file("README.md", syntax_filter="python")
```
or prefix your code block in the Markdown file with an `exdown-skip` comment
````markdown
Lorem ipsum
<!--exdown-skip-->
```python
foo + bar  # not working
```
dolor sit amet.
````


#### Merging code blocks
Broken-up code blocks can be merged into one with the `exdown-cont` prefix
````markdown
Lorem ipsum
```
a = 1
```
dolor sit amet
<!--exdown-cont-->
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
<!--exdown-expected-output-->
```
5
```
````


#### Expected errors
Some code blocks are expected to give errors. You can verify this with
````markdown
The following gives an error:
<!--exdown-expect-exception-->
```python
1 / 0
```
````


### License
This software is published under the [MIT
license](https://en.wikipedia.org/wiki/MIT_License).
