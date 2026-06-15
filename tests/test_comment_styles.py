import pytest


@pytest.mark.parametrize(
    "comment",
    [
        "<!--pytest-codeblocks:cont-->",
        "<!---pytest-codeblocks:cont--->",
        "<!-- pytest-codeblocks:cont -->",
        "<!--- pytest-codeblocks:cont --->",
    ],
)
def test_cont(pytester, comment):
    string = """
    Lorem ipsum
    ```python
    a = 1
    ```
    dolor sit amet
    {comment}
    ```
    a + 1
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)
