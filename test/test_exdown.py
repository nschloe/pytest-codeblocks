import io
import pathlib

import pytest

import exdown

this_dir = pathlib.Path(__file__).resolve().parent
inp = io.StringIO(
    """
Lorem ipsum
```python
1 + 2 + 3
```
dolor sit amet
"""
)


@pytest.mark.parametrize("string,lineno", exdown.from_buffer(inp))
def test_string(string, lineno):
    exec(string)


# example.md against reference strings test against
def test_reference():
    ref = [
        ("1 + 1\n", 1),
        ("1 + 2 + 3\n2 + 5\n", 5),
        ("import exdown\n\nexdown.from_buffer\n", 10),
        ("# ```import math```\n", 26),
        ("1 + 1 == 2\n", 31),
        ("1 + 1 == 2\n", 36),
    ]
    lst = exdown.extract(this_dir / "example.md", syntax_filter="python")
    for r, obj in zip(ref, lst):
        assert r == obj


@pytest.mark.parametrize(
    "string, lineno",
    exdown.extract(this_dir / "example.md", syntax_filter="python"),
)
def test_file(string, lineno):
    exec(string)


if __name__ == "__main__":
    blocks = exdown.extract(this_dir / "example.md", syntax_filter="python")
    for block in blocks:
        print(block)
        print()
