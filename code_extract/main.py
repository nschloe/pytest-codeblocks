# -*- coding: utf-8 -*-
#
from itertools import islice
import re


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


def write(code_blocks, file_prefix):
    for k, code_block in enumerate(code_blocks):
        filename = file_prefix + str(k) + '.py'
        with open(filename, 'w') as f:
            f.write(code_block)
    return
