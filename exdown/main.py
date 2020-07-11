import re


def extract(f, *args, **kwargs):
    with open(f, "r") as handle:
        return from_buffer(handle, *args, **kwargs)


def from_buffer(f, max_num_lines=10000, syntax_filter=None):
    out = []
    previous_line = None
    k = 1
    while True:
        line = f.readline()
        k += 1
        if not line:
            # EOF
            break

        m = re.match("[^`]*```(.*)$", line)
        if m:
            lineno = k - 1
            # read the block
            code_block = [f.readline()]
            k += 1
            while re.search("```", code_block[-1]) is None:
                print("a", k)
                code_block.append(f.readline())
                k += 1
                if k > max_num_lines:
                    raise RuntimeError(
                        f"File too large (> {max_num_lines} lines). Set max_num_lines."
                    )

            if syntax_filter and syntax_filter.strip() != m.group(1).strip():
                continue
            if previous_line.strip() == "<!--exdown-skip-->":
                continue

            out.append(("".join(code_block[:-1]), lineno))

        previous_line = line

    return out
