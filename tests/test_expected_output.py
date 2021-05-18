def test_expected_output(testdir):
    string = """
    Lorem ipsum
    ```python
    print(1 + 3)
    print(1 - 3)
    print(1 * 3)
    ```
    dolor sit amet
    <!--pytest-codeblocks:expected-output-->
    ```
    4
    -2
    3
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_expected_output_fail(testdir):
    string = """
    Lorem ipsum
    ```python
    print(1 + 3)
    ```
    dolor sit amet
    <!--pytest-codeblocks:expected-output-->
    ```
    5
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)
