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


def extract(f, filter=None):
    code_blocks = []
    while True:
        try:
            line = next(islice(f, 1))
        except StopIteration:  # EOF
            break

        out = re.match('[^`]*```(.*)$', line)
        if out:
            if filter and filter.strip() != out.group(1).strip():
                continue
            code_block = [next(islice(f, 1))]
            while re.search('```', code_block[-1]) is None:
                code_block.append(next(islice(f, 1)))
            code_blocks.append(''.join(code_block[:-1]))
    return code_blocks


def write(f, code_blocks, prefix='test'):
    # We'd like to put all code blocks in one file, each in separate test*()
    # functions (for them to be picked up by pytest, for example), but
    # asterisk imports are forbidden in subfunctions. Hence, parse for those
    # imports and put them at the beginning of the output file.
    asterisk_imports = []
    clean_code_blocks = []
    for code_block in code_blocks:
        clean_code_block = []
        for line in code_block.split('\n'):
            if re.match('\s*from\s+[^\s]+\s+import\s+\*', line):
                asterisk_imports.append(line)
            else:
                clean_code_block.append(line)
        clean_code_blocks.append('\n'.join(clean_code_block))
    # make list unique
    asterisk_imports = list(set(asterisk_imports))

    f.write('\n'.join(asterisk_imports))
    for k, code_block in enumerate(clean_code_blocks):
        f.write('\n\n\ndef %s%d():\n' % (prefix, k))
        f.write(indent(code_block, 4))
        f.write('    return')
    return
