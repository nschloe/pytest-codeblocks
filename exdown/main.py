import re


def extract(f, *args, **kwargs):
    with open(f, "r") as handle:
        return from_buffer(handle, *args, **kwargs)


def from_buffer(f, syntax_filter=None):
    code_blocks = []
    previous_line = None
    while True:
        line = f.readline()
        if not line:
            # EOF
            break

        out = re.match("[^`]*```(.*)$", line)
        if out:
            # read the block
            code_block = [f.readline()]
            while re.search("```", code_block[-1]) is None:
                code_block.append(f.readline())

            if syntax_filter and syntax_filter.strip() != out.group(1).strip():
                continue
            if previous_line.strip() == "<!--exdown-skip-->":
                continue

            code_blocks.append("".join(code_block[:-1]))

        previous_line = line

    return code_blocks
