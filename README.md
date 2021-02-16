<p align="center">
  <a href="https://github.com/nschloe/exdown"><img alt="exdown" src="https://nschloe.github.io/exdown/logo.svg" width="25%"></a>
  <p align="center">Extract code blocks from Markdown.</p>
</p>

[![PyPi Version](https://img.shields.io/pypi/v/exdown.svg?style=flat-square)](https://pypi.org/project/exdown)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/exdown.svg?style=flat-square)](https://pypi.org/pypi/exdown/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/exdown.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/exdown)
[![PyPi downloads](https://img.shields.io/pypi/dm/exdown.svg?style=flat-square)](https://pypistats.org/packages/exdown)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/exdown/ci?style=flat-square)](https://github.com/nschloe/exdown/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/exdown.svg?style=flat-square)](https://codecov.io/gh/nschloe/exdown)
[![LGTM](https://img.shields.io/lgtm/grade/python/github/nschloe/exdown.svg?style=flat-square)](https://lgtm.com/projects/g/nschloe/exdown)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

This is exdown, a tool for extracting code blocks from Markdown files and to create
tests from them.

Install with
```
pip install exdown
```
and use as
```python
import exdown

blocks = exdown.extract("README.md")
```
or, to create tests for [pytest](https://docs.pytest.org/en/stable/)
```python
import exdown

test_readme = exdown.pytests("README.md")
```

If you don't want all code blocks to be extracted, you can filter by syntax
<!--exdown-skip-->
```python
exdown.pytests("README.md", syntax_filter="python")
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

### License
exdown is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
