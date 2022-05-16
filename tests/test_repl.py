import pathlib

from pytest import skip

import pytest_codeblocks


def test_repr(testdir):
    string1 = """
    ```python
    >>> print("Hello World!")
    Hello World!
    ```
    """
    testdir.makefile(".md", string1)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_cont(testdir):
    string1 = """
    ```python
    >>> def add(a, b):
    ...     return a + b
    ```

    <!--pytest-codeblocks:cont-->
    ```python
    >>> add(2,7)
    9
    ```
    """
    testdir.makefile(".md", string1)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_exception(testdir):
    string1 = """
    Handle the exception by doctest:
    ```python
    >>> raise Exception("This should fail")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    Exception: This should fail
    ```

    Handle the exception by pytest:
    <!--pytest-codeblocks:expect-exception-->
    ```python
    >>> raise Exception("This should fail")
    ```
    """
    testdir.makefile(".md", string1)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=2)
