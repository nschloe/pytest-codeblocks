import io

import pytest_codeblocks

string1 = """
Lorem ipsum
<!--pytest_codeblocks-expect-exception-->
```python
raise RuntimeError()
```
"""
test_frombuffer1 = pytest_codeblocks.pytests_from_buffer(io.StringIO(string1))


# string2 = """
# ```
# <!--pytest_codeblocks-expect-error-->
# ```python
# raise RuntimeError()
# ```
# """
# test_frombuffer2 = pytest_codeblocks.pytests_from_buffer(io.StringIO(string2))
