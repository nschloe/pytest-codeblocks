def test_expect_error(testdir):
    string = """
    Lorem ipsum
    <!--pytest-codeblocks:expect-exception-->
    ```python
    raise RuntimeError()
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_expect_error_fail(testdir):
    string1 = """
    Lorem ipsum
    <!--pytest-codeblocks:expect-exception-->
    ```python
    1 + 1
    ```
    """
    testdir.makefile(".md", string1)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)
