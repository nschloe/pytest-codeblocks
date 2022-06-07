def test_expect_error(testdir):
    string = """
    <!--pytest.mark.xfail-->
    ```python
    raise RuntimeError()
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(xfailed=1)


def test_expect_error_runtimeerror(testdir):
    string = """
    <!--pytest.mark.xfail(raises=RuntimeError)-->
    ```python
    raise RuntimeError()
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(xfailed=1)


def test_expect_error_indexerror(testdir):
    string = """
    <!--pytest.mark.xfail(raises=IndexError)-->
    ```python
    raise RuntimeError()
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)


def test_expect_error_fail(testdir):
    string1 = """
    Lorem ipsum
    <!--pytest.mark.xfail-->
    ```python
    1 + 1
    ```
    """
    testdir.makefile(".md", string1)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(xpassed=1)
