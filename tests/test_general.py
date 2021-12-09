import pathlib

import pytest_codeblocks


def test_basic(testdir):
    string1 = """
    Lorem ipsum
    ```python
    1 + 2 + 3
    ```
    dolor sit amet
    """
    testdir.makefile(".md", string1)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(passed=1)


def test_skip(testdir):
    string1 = """
    Lorem ipsum
    <!--pytest-codeblocks:skip-->
    ```python
    1 + 2 + 3
    ```
    dolor sit amet

    Some newlines:

    <!--pytest-codeblocks:skip-->

    ```python
    1 + 2 + 3
    ```
    """
    testdir.makefile(".md", string1)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(skipped=2)


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
        pytest_codeblocks.CodeBlock("foobar\n", 16, "ruby"),
        pytest_codeblocks.CodeBlock("echo abc\n", 20, "sh"),
        pytest_codeblocks.CodeBlock("bar\n", 25, "python", skip=True),
        pytest_codeblocks.CodeBlock("# ```import math```\n", 30, "python"),
        pytest_codeblocks.CodeBlock("1 + 1 == 2\n", 35, "python"),
        pytest_codeblocks.CodeBlock("1 + 1 == 2\n", 40, "python"),
    ]
    this_dir = pathlib.Path(__file__).resolve().parent
    lst = pytest_codeblocks.extract_from_file(this_dir / "example.md")
    print(lst)
    for r, obj in zip(ref, lst):
        print("\n\nr  ", r)
        print("\nobj", obj)
        assert r == obj
