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

        if line[:3] == "```":
            syntax = line[3:]
            lineno = k - 1
            # read the block
            line = f.readline()
            code_block = [line]
            k += 1
            while code_block[-1][:3] != "```":
                line = f.readline()
                code_block.append(line)
                k += 1
                if k > max_num_lines:
                    raise RuntimeError(
                        f"File too large (> {max_num_lines} lines). Set max_num_lines."
                    )

            if syntax_filter and syntax_filter.strip() != syntax.strip():
                continue
            if previous_line.strip() == "<!--exdown-skip-->":
                continue

            out.append(("".join(code_block[:-1]), lineno))

        previous_line = line

    return out
