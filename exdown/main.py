import re


def extract(f, *args, **kwargs):
    with open(f, "r") as handle:
        return from_buffer(handle, *args, **kwargs)


def from_buffer(f, syntax_filter=None, skip=None):
    skip = [] if skip is None else skip
    code_blocks = []
    k = 0
    while True:
        line = f.readline()
        if not line:
            # EOF
            break

        out = re.match("[^`]*```(.*)$", line)
        if out:
            if syntax_filter and syntax_filter.strip() != out.group(1).strip():
                continue
            code_block = [f.readline()]
            while re.search("```", code_block[-1]) is None:
                code_block.append(f.readline())

            if k not in skip:
                code_blocks.append("".join(code_block[:-1]))
            k += 1

    return code_blocks
