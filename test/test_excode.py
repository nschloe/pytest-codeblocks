import io
import pathlib

import pytest

import excode

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


@pytest.mark.parametrize("string", excode.from_buffer(inp))
def test_string(string):
    exec(string)


@pytest.mark.parametrize(
    "string",
    excode.extract(this_dir / "example.md", syntax_filter="python", skip=[2]),
)
def test_file(string):
    exec(string)
