def test_custom_mark(testdir):
    string = """
    Lorem ipsum
    <!--pytest-codeblocks:custom-marks(pytest.mark.gpu)-->
    ```python
    a = 1
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)

def test_multiple_custom_marks(testdir):
    string = """
    Lorem ipsum
    <!--pytest-codeblocks:custom-marks(pytest.mark.gpu;pytest.mark.fast)-->
    ```python
    a = 1
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)