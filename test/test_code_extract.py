# -*- coding: utf-8 -*-
#
import code_extract

try:
    import StringIO as io
except ImportError:
    import io


def test_plain():
    inp = io.StringIO('''
Lorem ipsum
```python
1 + 2 + 3
```
dolor sit amet
''')
    code_blocks = code_extract.extract(inp)
    assert len(code_blocks) == 1
    assert code_blocks[0] == '1 + 2 + 3\n'
    code_extract.write(code_blocks, 'test')
    with open('test0.py', 'r') as f:
        assert f.read() == '1 + 2 + 3\n'
    return


def test_filter():
    inp = io.StringIO('''
Lorem ipsum
```c
a = 4 + 5 + 6;
```
```python
1 + 2 + 3
```
dolor sit amet
''')
    code_blocks = code_extract.extract(inp, filter='python')
    assert len(code_blocks) == 1
    assert code_blocks[0] == '1 + 2 + 3\n'
    return
