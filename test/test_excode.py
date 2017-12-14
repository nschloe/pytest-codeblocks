# -*- coding: utf-8 -*-
#
import excode

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
    code_blocks = excode.extract(inp)
    assert len(code_blocks) == 1
    assert code_blocks[0] == '1 + 2 + 3\n'
    out = io.StringIO()
    excode.write(out, code_blocks)
    assert out.getvalue() == '''

def test0():
    1 + 2 + 3
    return
'''
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
    code_blocks = excode.extract(inp, filter='python')
    assert len(code_blocks) == 1
    assert code_blocks[0] == '1 + 2 + 3\n'
    return
