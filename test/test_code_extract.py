# -*- coding: utf-8 -*-
#
import code_extract

try:
    import StringIO as io
except ImportError:
    import io


def test():
    inp = io.StringIO('''
Lorem ipsum
```python
1 + 2 + 3
```
dolor sit amet
''')
    code_blocks = code_extract.extract(inp)
    print(code_blocks)
    assert len(code_blocks) == 1
    assert code_blocks[0] == '1 + 2 + 3\n'
    out = io.StringIO()
    code_extract.write(out, code_blocks)
    print(out.getvalue())
    assert out.getvalue() == '''def test0():
    1 + 2 + 3
    return

'''
    return
