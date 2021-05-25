def test_cont(testdir):
    string = """
    Lorem ipsum
    ```python
    a = 1
    ```
    dolor sit amet
    <!--pytest-codeblocks:cont-->
    ```
    a + 1
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_hidden_cont(testdir):
    string = """
    Lorem ipsum
    <!--
    ```python
    a = 1
    ```
    -->
    dolor sit amet
    <!--pytest-codeblocks:cont-->
    ```
    a + 1
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_nocont(testdir):
    string = """
    <!--pytest-codeblocks:cont-->
    ```python
    1 + 2 + 3
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(errors=1)
