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


@pytest.mark.parametrize(
    "string, lineno", exdown.extract(this_dir / "example.md", syntax_filter="python"),
)
def test_file(string, lineno):
    exec(string)
