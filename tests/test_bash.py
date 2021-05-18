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


def test_bash_expect_fail(testdir):
    string = """
    <!--pytest-codeblocks:expect-error-->
    ```sh
    cdc
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_bash_expect_fail_passed(testdir):
    string = """
    <!--pytest-codeblocks:expect-error-->
    ```sh
    cd
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)
