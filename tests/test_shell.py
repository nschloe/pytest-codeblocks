import sys

import pytest

if sys.platform.startswith("win"):
    pytest.skip("skipping shell tests", allow_module_level=True)


def test_shell(testdir):
    string = """
    Lorem ipsum
    ```sh
    ls
    ```
    dolor sit amet
    ```sh
    cd
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=2)


def test_shell_fail(testdir):
    string = """
    ```sh
    cdc
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)


def test_shell_expect_fail(testdir):
    string = """
    <!--pytest-codeblocks:expect-error-->
    ```sh
    cdc
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_shell_expect_fail_passed(testdir):
    string = """
    <!--pytest-codeblocks:expect-error-->
    ```sh
    cd
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)


def test_shell_expect_output(testdir):
    string = """
    ```sh
    echo abc
    ```
    <!--pytest-codeblocks:expected-output-->
    ```sh
    abc
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_shell_expect_output_fail(testdir):
    string = """
    ```sh
    echo abc
    ```
    <!--pytest-codeblocks:expected-output-->
    ```sh
    ac
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)


def test_bash(testdir):
    string = """
    ```bash
    foo=1
    if [[ $foo == 1 ]]; then
        echo abc
    fi
    ```
    <!--pytest-codeblocks:expected-output-->
    ```sh
    abc
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)
