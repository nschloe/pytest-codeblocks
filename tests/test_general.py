import io
import pathlib

import pytest_codeblocks


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
    out = pytest_codeblocks.extract_from_buffer(inp)
    assert out == [pytest_codeblocks.CodeBlock("1 + 2 + 3\n", 3, "python")]


# example.md against reference strings test against
def test_reference():
    ref = [
        pytest_codeblocks.CodeBlock("1 + 1\n", 1, "python"),
        pytest_codeblocks.CodeBlock("1 + 2 + 3\n2 + 5\n", 5, "python"),
        pytest_codeblocks.CodeBlock(
            "import pytest_codeblocks\n\npytest_codeblocks.extract_from_buffer\n",
            10,
            "python",
        ),
        pytest_codeblocks.CodeBlock("foobar\n", 16, "bash"),
        pytest_codeblocks.CodeBlock("# ```import math```\n", 26, "python"),
        pytest_codeblocks.CodeBlock("1 + 1 == 2\n", 31, "python"),
        pytest_codeblocks.CodeBlock("1 + 1 == 2\n", 36, "python"),
    ]
    this_dir = pathlib.Path(__file__).resolve().parent
    lst = pytest_codeblocks.extract_from_file(this_dir / "example.md")
    print(lst)
    for r, obj in zip(ref, lst):
        print("r  ", r)
        print("obj", obj)
        assert r == obj
