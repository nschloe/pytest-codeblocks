import re


def from_file(f, *args, **kwargs):
    with open(f, "r") as handle:
        return from_string(handle, *args, **kwargs)


def from_string(f, filter=None):
    code_blocks = []
    while True:
        line = f.readline()
        if not line:
            # EOF
            break

        out = re.match("[^`]*```(.*)$", line)
        if out:
            if filter and filter.strip() != out.group(1).strip():
                continue
            code_block = [f.readline()]
            while re.search("```", code_block[-1]) is None:
                code_block.append(f.readline())
            code_blocks.append("".join(code_block[:-1]))

    return code_blocks
