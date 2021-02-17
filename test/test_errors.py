import io

import pytest

import exdown


def test_unclosed():
    unclosed = io.StringIO(
        """
    ```python
    1 + 2 + 3
    """
    )
    with pytest.raises(RuntimeError):
        exdown.from_buffer(unclosed)


def test_maxlines():
    unclosed = io.StringIO(
        """
    ```python
    1 + 2 + 3
    ```
    """
    )
    with pytest.raises(RuntimeError):
        exdown.from_buffer(unclosed, max_num_lines=1)
