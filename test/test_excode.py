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


@pytest.mark.parametrize("string", excode.from_string(inp))
def test_string(string):
    exec(string)


@pytest.mark.parametrize(
    "string", excode.from_file(this_dir / "example.md", filter="python")
)
def test_file(string):
    exec(string)


# def test_filter():
#     inp = io.StringIO(
#         """
# Lorem ipsum
# ```c
# a = 4 + 5 + 6;
# ```
# ```python
# 1 + 2 + 3
# ```
# dolor sit amet
# """
#     )
#     code_blocks = excode.extract(inp, filter="python")
#     assert len(code_blocks) == 1
#     assert code_blocks[0] == "1 + 2 + 3\n"
#     return
