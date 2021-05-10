<p align="center">
  <a href="https://github.com/nschloe/meshio"><img alt="meshio" src="https://nschloe.github.io/pytest-codeblocks/logo.svg" width="60%"></a>
  <p align="center">Test code blocks in your READMEs.</p>
</p>

[![PyPi Version](https://img.shields.io/pypi/v/pytest-codeblocks.svg?style=flat-square)](https://pypi.org/project/pytest-codeblocks/)
[![Anaconda Cloud](https://anaconda.org/conda-forge/pytest-codeblocks/badges/version.svg?=style=flat-square)](https://anaconda.org/conda-forge/pytest-codeblocks/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-codeblocks.svg?style=flat-square)](https://pypi.org/project/pytest-codeblocks/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pytest-codeblocks.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/pytest-codeblocks)
[![PyPi downloads](https://img.shields.io/pypi/dm/pytest-codeblocks.svg?style=flat-square)](https://pypistats.org/packages/pytest-codeblocks)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/pytest-codeblocks/ci?style=flat-square)](https://github.com/nschloe/pytest-codeblocks/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/pytest-codeblocks.svg?style=flat-square)](https://app.codecov.io/gh/nschloe/pytest-codeblocks)
[![LGTM](https://img.shields.io/lgtm/grade/python/github/nschloe/pytest-codeblocks.svg?style=flat-square)](https://lgtm.com/projects/g/nschloe/pytest-codeblocks)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

This is pytest-codeblocks, a [pytest](https://pytest.org/) plugin for testing code
blocks from README files.

Install with
```
pip install pytest-codeblocks
```
and run pytest with
```
pytest --codeblocks
```
```
================================= test session starts =================================
platform linux -- Python 3.9.4, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /path/to/directory
plugins: codeblocks-0.10.4
collected 56 items

example.md .......................                                              [ 50%]
README.md .......................                                               [100%]

================================= 56 passed in 0.08s ==================================
```
By default, pytest-codeblocks will only pick up code blocks with `python` syntax
highlighting.


#### Skipping code blocks

Prefix your code block with a `pytest-codeblocks:skip` comment to skip
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
```python
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
4
```
````


#### Expected errors
Some code blocks are expected to give errors. You can verify this with
````markdown
The following gives an error:
<!--pytest-codeblocks:expect-error-->
```python
1 / 0
```
````
The keyword `expect-exception` is also possible.


### License
This software is published under the [MIT
license](https://en.wikipedia.org/wiki/MIT_License).
