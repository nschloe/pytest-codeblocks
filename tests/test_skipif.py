def test_skip(pytester):
    string = """
    Lorem ipsum

    <!--pytest.mark.skip-->

    ```python
    print(1 + 3)
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)


def test_skip_expected_output(pytester):
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
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)


def test_skipif(pytester):
    string = """
    Lorem ipsum

    <!--pytest.mark.skipif(1 < 3, reason="")-->

    ```python
    print(1 + 3)
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)


def test_skipif2(pytester):
    string = """
    Lorem ipsum

    <!--pytest.mark.skipif(1 > 3, reason="")-->

    ```python
    print(1 + 3)
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_skipif_expected_output(pytester):
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
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)


def test_skipif_expected_output2(pytester):
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
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_importorskip(pytester):
    string = """
    Lorem ipsum

    <!--pytest-codeblocks:importorskip(some_nonexistent_module)-->

    ```python
    print(1 + 3)
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(skipped=1)


def test_importorskip2(pytester):
    string = """
    Lorem ipsum

    <!--pytest-codeblocks:importorskip(sys)-->

    ```python
    print(1 + 3)
    ```
    """
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)
