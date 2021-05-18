```python
1 + 1
```
Lorem ipsum
```python
1 + 2 + 3
2 + 5
```
dolor sit amet.
```python
import pytest_codeblocks

pytest_codeblocks.extract_from_buffer
```
Something that should be skipped because of the language:
```ruby
foobar
```
A shell script should be exectuted:
```sh
echo abc
```
Again with an explicit skip:
<!--pytest-codeblocks:skip-->
```python
bar
```

Something that contains triple fences
```python
# ```import math```
```

Indented code blocks:
  ```python
  1 + 1 == 2
  ```

"Wrong" indentation:
```python
1 + 1 == 2
  ```
