def test_custom_marks(testdir):
    string = """
    Lorem ipsum
    <!--pytest-codeblocks:custom-mark(pytest.mark.gpu)l-->
    ```python
    a = 1
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)