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
def test_cont(testdir, comment):
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
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)
