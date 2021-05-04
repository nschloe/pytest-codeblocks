import io

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
    lst = exdown.from_buffer(io.StringIO(string))
    assert lst == [("a = 1\na + 1\n", 3)]
