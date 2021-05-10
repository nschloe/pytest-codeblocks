import io

import pytest_codeblocks

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


def test_cont():
    lst = pytest_codeblocks.extract_from_buffer(io.StringIO(string))
    print(lst)
    assert lst == [
        pytest_codeblocks.CodeBlock(
            "print(1 + 3)\nprint(1 - 3)\nprint(1 * 3)\n", 3, "python", "4\n-2\n3\n"
        )
    ]
