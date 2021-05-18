import io

import pytest

import pytest_codeblocks


def test_unclosed(testdir):
    string = """
    ```python
    1 + 2 + 3
    """
    testdir.makefile(".md", string)
    result = testdir.runpytest("--codeblocks")
    result.assert_outcomes(errors=1)


def test_maxlines():
    unclosed = io.StringIO(
        """
    ```python
    1 + 2 + 3
    ```
    """
    )
    with pytest.raises(RuntimeError):
        pytest_codeblocks.extract_from_buffer(unclosed, max_num_lines=1)
