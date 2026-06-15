def test_expect_error(pytester):
    string = """
    <!--pytest.mark.xfail-->
    ```python
    raise RuntimeError()
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(xfailed=1)


def test_expect_error_runtimeerror(pytester):
    string = """
    <!--pytest.mark.xfail(raises=RuntimeError)-->
    ```python
    raise RuntimeError()
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(xfailed=1)


def test_expect_error_indexerror(pytester):
    string = """
    <!--pytest.mark.xfail(raises=IndexError)-->
    ```python
    raise RuntimeError()
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)


def test_expect_error_fail(pytester):
    string1 = """
    Lorem ipsum
    <!--pytest.mark.xfail-->
    ```python
    1 + 1
    ```
    """
    pytester.makefile(".md", string1)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(xpassed=1)
