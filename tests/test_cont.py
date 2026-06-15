def test_cont(pytester):
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
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_hidden_cont(pytester):
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
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_nocont(pytester):
    string = """
    <!--pytest-codeblocks:cont-->
    ```python
    1 + 2 + 3
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(errors=1)
