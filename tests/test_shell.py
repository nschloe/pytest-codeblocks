import sys

import pytest

if sys.platform.startswith("win"):
    pytest.skip("skipping shell tests", allow_module_level=True)


def test_shell(pytester):
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
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=2)


def test_shell_fail(pytester):
    string = """
    ```sh
    cdc
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)


def test_shell_expect_fail(pytester):
    string = """
    <!--pytest.mark.xfail-->
    ```sh
    cdc
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(xfailed=1)


def test_shell_expect_fail_passed(pytester):
    string = """
    <!--pytest.mark.xfail-->
    ```sh
    cd
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(xpassed=1)


def test_shell_expect_output(pytester):
    string = """
    ```sh
    echo abc
    ```
    <!--pytest-codeblocks:expected-output-->
    ```sh
    abc
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_shell_expect_output_fail(pytester):
    string = """
    ```sh
    echo abc
    ```
    <!--pytest-codeblocks:expected-output-->
    ```sh
    ac
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)


def test_bash(pytester):
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
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)
