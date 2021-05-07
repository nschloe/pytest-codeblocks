import io

import pytest

import pytest_codeblocks

string = """
Lorem ipsum
```python
a = 1
```
dolor sit amet
<!--pytest-codeblocks:cont-->
```
a + 1
```
"""

# test_frombuffer = pytest_codeblocks.pytests_from_buffer(io.StringIO(string))


def test_cont():
    lst = pytest_codeblocks.extract_from_buffer(io.StringIO(string))
    assert lst == [pytest_codeblocks.CodeBlock("a = 1\na + 1\n", 3, "python")]


def test_nocont():
    code = io.StringIO(
        """
    <!--pytest-codeblocks:cont-->
    ```python
    1 + 2 + 3
    ```
    """
    )
    with pytest.raises(RuntimeError):
        pytest_codeblocks.extract_from_buffer(code)
