import io
import tempfile
from pathlib import Path

import exdown


def test_from_buffer():
    inp = io.StringIO(
        """
    Lorem ipsum
    ```python
    1 + 2 + 3
    ```
    dolor sit amet
    """
    )
    out = exdown.from_buffer(inp)
    assert out == [("1 + 2 + 3\n", 3)]


# example.md against reference strings test against
def test_reference():
    file_contents = """```python
1 + 1
```
Lorem ipsum
```python
1 + 2 + 3
2 + 5
```
dolor sit amet.
```python
import exdown

exdown.from_buffer
```
Something that should be skipped because of the language:
```bash
foobar
```
Again with an explicit skip:
<!--exdown-skip-->
```python
bar
```

Something that contains triple fences
```python
# ```import math```
```

Indented code blocks:
  ```python
  1 + 1 == 2
  ```

"Wrong" indentation:
```python
1 + 1 == 2
  ```
"""
    ref = [
        ("1 + 1\n", 1),
        ("1 + 2 + 3\n2 + 5\n", 5),
        ("import exdown\n\nexdown.from_buffer\n", 10),
        ("# ```import math```\n", 26),
        ("1 + 1 == 2\n", 31),
        ("1 + 1 == 2\n", 36),
    ]
    with tempfile.TemporaryDirectory() as tdir:
        filename = Path(tdir) / "test.md"
        with open(filename, "w") as f:
            f.write(file_contents)

        lst = exdown.extract(filename, syntax_filter="python")
        for r, obj in zip(ref, lst):
            assert r == obj
