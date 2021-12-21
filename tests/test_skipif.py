def test_skip(testdir):
    string = """
    Lorem ipsum

    <!--pytest-codeblocks:skip-->

    ```python
    print(1 + 3)
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)


def test_skip_expected_output(testdir):
    string = """
    Lorem ipsum

    <!--pytest-codeblocks:skip-->

    ```python
    print(1 + 3)
    ```

    <!--pytest-codeblocks:expected-output-->

    ```
    25abc
    ```

    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)


def test_skipif(testdir):
    string = """
    Lorem ipsum

    <!--pytest-codeblocks:skipif(1 < 3)-->

    ```python
    print(1 + 3)
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)

    string = """
    Lorem ipsum

    <!--pytest-codeblocks:skipif(1 > 3)-->

    ```python
    print(1 + 3)
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_skipif_expected_output(testdir):
    string = """
    Lorem ipsum

    <!--pytest-codeblocks:skipif(1 < 3)-->

    ```python
    print(1 + 3)
    ```

    <!--pytest-codeblocks:expected-output-->

    ```
    25abc
    ```

    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)

    string = """
    Lorem ipsum

    <!--pytest-codeblocks:skipif(1 > 3)-->

    ```python
    print(1 + 3)
    ```

    <!--pytest-codeblocks:expected-output-->

    ```
    4
    ```

    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)
