# -*- coding: utf-8 -*-
#
from itertools import islice
import re
# https://stackoverflow.com/a/8348914/353337
try:
    import textwrap
    textwrap.indent
except AttributeError:  # undefined function (wasn't added until Python 3.3)
    def indent(text, amount, ch=' '):
        padding = amount * ch
        return ''.join(padding+line for line in text.splitlines(True))
else:
    def indent(text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)


def extract(filename, filter=None):
    code_blocks = []
    with open(filename, 'rb') as f:
        while True:
            try:
                line = next(islice(f, 1)).decode('utf-8')
            except StopIteration:  # EOF
                break

            out = re.match('[^`]*```(.*)$', line)
            if out:
                if filter and filter.strip() != out.group(1).strip():
                    continue
                code_block = [next(islice(f, 1)).decode('utf-8')]
                while re.search('```', code_block[-1]) is None:
                    code_block.append(next(islice(f, 1)).decode('utf-8'))
                code_blocks.append(''.join(code_block[:-1]))
    return code_blocks


def write(code_blocks, filename, prefix='test'):
    with open(filename, 'w') as f:
        for k, code_block in enumerate(code_blocks):
            f.write('def %s%d():\n' % (prefix, k))
            f.write(indent(code_block, 4))
            f.write('\n\n')
    return
