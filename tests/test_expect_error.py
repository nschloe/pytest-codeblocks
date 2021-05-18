string1 = """
Lorem ipsum
<!--pytest-codeblocks:expect-exception-->
```python
raise RuntimeError()
```
dolor
<!--pytest-codeblocks:expect-exception-->
```python
1 + 1
```
"""

def test_expect_error(testdir):
    testdir.makefile(".md", string1)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1, failed=1)
