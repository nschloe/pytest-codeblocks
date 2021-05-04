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
import exdown

exdown.extract_from_buffer
```
Something that should be skipped because of the language:
```bash
foobar
```
Again with an explicit skip:
<!--exdown-skip-->
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
