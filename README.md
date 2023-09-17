<p align="center">
  <a href="https://github.com/nschloe/pytest-codeblocks"><img alt="pytest-codeblocks" src="https://nschloe.github.io/pytest-codeblocks/logo.svg" width="60%"></a>
  <p align="center">Test code blocks in your READMEs.</p>
</p>

[![PyPi Version](https://img.shields.io/pypi/v/pytest-codeblocks.svg?style=flat-square)](https://pypi.org/project/pytest_codeblocks/)
[![Anaconda Cloud](https://anaconda.org/conda-forge/pytest-codeblocks/badges/version.svg?=style=flat-square)](https://anaconda.org/conda-forge/pytest-codeblocks/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-codeblocks.svg?style=flat-square)](https://pypi.org/project/pytest_codeblocks/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pytest-codeblocks.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/pytest-codeblocks)
[![Downloads](https://static.pepy.tech/badge/pytest-codeblocks/month?style=flat-square)](https://www.pepy.tech/projects/pytest-codeblocks)

<!--[![PyPi downloads](https://img.shields.io/pypi/dm/pytest-codeblocks.svg?style=flat-square)](https://pypistats.org/packages/pytest-codeblocks)-->

[![gh-actions](https://img.shields.io/github/actions/workflow/status/nschloe/pytest-codeblocks/tests?style=flat-square)](https://github.com/nschloe/pytest-codeblocks/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/pytest-codeblocks.svg?style=flat-square)](https://app.codecov.io/gh/nschloe/pytest-codeblocks)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

This is pytest-codeblocks, a [pytest](https://pytest.org/) plugin for testing code
blocks from README files. It supports Python and shell code.

Install with

```sh
pip install pytest-codeblocks
```

and run pytest with

```sh
pytest --codeblocks
```

```sh
================================= test session starts =================================
platform linux -- Python 3.9.4, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /path/to/directory
plugins: codeblocks-0.11.0
collected 56 items

example.md .......................                                              [ 50%]
README.md .......................                                               [100%]

================================= 56 passed in 0.08s ==================================
```

pytest-codeblocks will only pick up code blocks with `python` and `sh`/`bash`/`zsh`
syntax highlighting.

#### Marking code blocks

It is possible to use `pytest.mark` for marking code blocks. For example,
to skip a code block use `pytest.mark.skip` or `pytest.mark.skipif`:

````markdown
Lorem ipsum

<!--pytest.mark.skip-->

```python
foo + bar  # not working
```

dolor sit amet.
````

```markdown
<!--pytest.mark.skipif(sys.version_info <= (3, 7), reason="Need at least Python 3.8")-->
```

You can skip code blocks on import errors with

```markdown
<!--pytest-codeblocks:importorskip(sympy)-->
```

Skip the entire file by putting

```markdown
<!--pytest-codeblocks:skipfile-->
```

in the first line.

For expected errors, use `pytest.mark.xfail`:

````markdown
The following gives an error:

<!--pytest.mark.xfail-->

```python
1 / 0
```
````

#### Merging code blocks

Broken-up code blocks can be merged into one with the `pytest-codeblocks:cont` prefix

````markdown
Lorem ipsum

```python
a = 1
```

dolor sit amet

<!--pytest-codeblocks:cont-->

```python
# this would otherwise fail since `a` is not defined
a + 1
```
````

If you'd like to prepend code that you don't want to show, you can just comment it out;
pytest-codeblocks will pick it up anyway:

````markdown
Lorem ipsum

<!--
```python
a = 1
```
-->

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

```sh
print(1 + 3)
```

gives

<!--pytest-codeblocks:expected-output-->

```
4
```
````

Use `expected-output-ignore-whitespace` if you'd like whitespace differences to
be ignored.

(Conditionally) Skipping the output verfication works by prepending the first
block with `skip`/`skipif` (see [above](#skipping-code-blocks)).
