import io
import pathlib

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
    ref = [
        ("1 + 1\n", 1),
        ("1 + 2 + 3\n2 + 5\n", 5),
        ("import exdown\n\nexdown.from_buffer\n", 10),
        ("# ```import math```\n", 26),
        ("1 + 1 == 2\n", 31),
        ("1 + 1 == 2\n", 36),
    ]
    this_dir = pathlib.Path(__file__).resolve().parent
    lst = exdown.extract(this_dir / "example.md", syntax_filter="python")
    for r, obj in zip(ref, lst):
        assert r == obj
