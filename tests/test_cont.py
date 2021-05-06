import io

import pytest

import exdown

string = """
Lorem ipsum
```python
a = 1
```
dolor sit amet
<!--exdown-cont-->
```
a + 1
```
"""


test_frombuffer = exdown.pytests_from_buffer(io.StringIO(string))


def test_cont():
    lst = exdown.extract_from_buffer(io.StringIO(string))
    assert lst == [exdown.CodeBlock("a = 1\na + 1\n", 3, "python")]


def test_nocont():
    code = io.StringIO(
        """
    <!--exdown-cont-->
    ```python
    1 + 2 + 3
    ```
    """
    )
    with pytest.raises(RuntimeError):
        exdown.extract_from_buffer(code)
