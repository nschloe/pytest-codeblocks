def test_skip(testdir):
    string = """
    Lorem ipsum

    <!--pytest.mark.skip-->

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

    <!--pytest.mark.skip-->

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

    <!--pytest.mark.skipif(1 < 3, reason="")-->

    ```python
    print(1 + 3)
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)


def test_skipif2(testdir):
    string = """
    Lorem ipsum

    <!--pytest.mark.skipif(1 > 3, reason="")-->

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

    <!--pytest.mark.skipif(1 < 3, reason="")-->

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


def test_skipif_expected_output2(testdir):
    string = """
    Lorem ipsum

    <!--pytest.mark.skipif(1 > 3, reason="")-->

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


def test_importorskip(testdir):
    string = """
    Lorem ipsum

    <!--pytest-codeblocks:importorskip(some_nonexistent_module)-->

    ```python
    print(1 + 3)
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)


def test_importorskip2(testdir):
    string = """
    Lorem ipsum

    <!--pytest-codeblocks:importorskip(sys)-->

    ```python
    print(1 + 3)
    ```
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)
