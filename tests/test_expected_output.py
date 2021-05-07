import io

import pytest_codeblocks

string = """
Lorem ipsum
```python
print(1 + 3)
```
dolor sit amet
<!--pytest-codeblocks:expected-output-->
```
4
```
"""


# test_frombuffer = pytest_codeblocks.pytests_from_buffer(io.StringIO(string))


def test_cont():
    lst = pytest_codeblocks.extract_from_buffer(io.StringIO(string))
    assert lst == [pytest_codeblocks.CodeBlock("print(1 + 3)\n", 3, "python", "4\n")]
