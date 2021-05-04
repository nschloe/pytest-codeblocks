import io
import pathlib

import exdown


def test_extract_from_buffer():
    inp = io.StringIO(
        """
    Lorem ipsum
    ```python
    1 + 2 + 3
    ```
    dolor sit amet
    """
    )
    out = exdown.extract_from_buffer(inp)
    assert out == [("1 + 2 + 3\n", 3, "python", None)]


# example.md against reference strings test against
def test_reference():
    ref = [
        ("1 + 1\n", 1, "python", None),
        ("1 + 2 + 3\n2 + 5\n", 5, "python", None),
        ("import exdown\n\nexdown.extract_from_buffer\n", 10, "python", None),
        ("foobar\n", 16, "bash", None),
        ("# ```import math```\n", 26, "python", None),
        ("1 + 1 == 2\n", 31, "python", None),
        ("1 + 1 == 2\n", 36, "python", None),
    ]
    this_dir = pathlib.Path(__file__).resolve().parent
    lst = exdown.extract(this_dir / "example.md")
    print(lst)
    for r, obj in zip(ref, lst):
        assert r == obj
