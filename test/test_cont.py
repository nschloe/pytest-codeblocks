import io

import exdown


def test_cont():
    inp = io.StringIO(
        """
    Lorem ipsum
    ```python
    a = 1
    ```
    dolor sit amet
    <!--exdown-cont-->
    ```
    a + 1
    ```
    """
    )
    lst = exdown.from_buffer(inp)
    assert lst == [("a = 1\na + 1\n", 3)]
