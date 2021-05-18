def test_bash(testdir):
    string = """
    Lorem ipsum
    ```bash
    ls
    ```
    dolor sit amet
    ```sh
    cd
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=2)


def test_bash_fail(testdir):
    string = """
    ```sh
    cdc
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)
