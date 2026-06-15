def test_expected_output(pytester):
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
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_expected_output_fail(pytester):
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
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)


def test_expected_output_ignore_whitespace(pytester):
    string = """
Lorem ipsum
```python
print(1 + 3)
print(1 - 3)
print(1 * 3)
```
dolor sit amet
<!--pytest-codeblocks:expected-output-ignore-whitespace-->
```
 4 -2

  3
```
"""
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_expected_output_ignore_whitespace_fail(pytester):
    string = """
Lorem ipsum
```python
print(1 + 3)
print(1 - 3)
print(1 * 3)
```
dolor sit amet
<!--pytest-codeblocks:expected-output-ignore-whitespace-->
```
 4 -2

  5
```
"""
    pytester.makefile(".md", string)
    result = pytester.runpytest("--codeblocks")
    result.assert_outcomes(failed=1)
