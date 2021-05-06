import io

import exdown

string1 = """
Lorem ipsum
<!--exdown-expect-exception-->
```python
raise RuntimeError()
```
"""
test_frombuffer1 = exdown.pytests_from_buffer(io.StringIO(string1))


# string2 = """
# ```
# <!--exdown-expect-error-->
# ```python
# raise RuntimeError()
# ```
# """
# test_frombuffer2 = exdown.pytests_from_buffer(io.StringIO(string2))
