import io

import exdown

string = """
Lorem ipsum
```python
print(1 + 3)
```
dolor sit amet
<!--exdown-expected-output-->
```
4
```
"""


test_frombuffer = exdown.pytests_from_buffer(io.StringIO(string))


def test_cont():
    lst = exdown.extract_from_buffer(io.StringIO(string))
    assert lst == [exdown.CodeBlock("print(1 + 3)\n", 3, "python", "4\n")]
