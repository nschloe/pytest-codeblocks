from pathlib import Path
from typing import Optional, Union


def extract(
    f: Union[str, bytes, Path], encoding: Optional[str] = None, *args, **kwargs
):
    with open(f, "r", encoding=encoding) as handle:
        return extract_from_buffer(handle, *args, **kwargs)


def extract_from_buffer(f, max_num_lines: int = 10000):
    out = []
    previous_line = None
    k = 1

    while True:
        line = f.readline()
        k += 1
        if not line:
            # EOF
            break

        if line.lstrip()[:3] == "```":
            syntax = line.strip()[3:]
            num_leading_spaces = len(line) - len(line.lstrip())
            lineno = k - 1
            # read the block
            code_block = []
            while True:
                line = f.readline()
                k += 1
                if not line:
                    raise RuntimeError("Hit end-of-file prematurely. Syntax error?")
                if k > max_num_lines:
                    raise RuntimeError(
                        f"File too large (> {max_num_lines} lines). Set max_num_lines."
                    )
                # check if end of block
                if line.lstrip()[:3] == "```":
                    break
                # Cut (at most) num_leading_spaces leading spaces
                nls = min(num_leading_spaces, len(line) - len(line.lstrip()))
                line = line[nls:]
                code_block.append(line)

            if (
                previous_line is not None
                and previous_line.strip() == "<!--exdown-skip-->"
            ):
                continue

            if (
                previous_line is not None
                and previous_line.strip() == "<!--exdown-cont-->"
            ):
                if len(out) == 0:
                    raise RuntimeError(
                        "Found <!--exdown-cont--> but no previous code block."
                    )
                out[-1] = (out[-1][0] + "".join(code_block), *out[-1][1:])
            else:
                out.append(("".join(code_block), lineno, syntax))

        previous_line = line

    return out


def pytests(
    f: Union[str, bytes, Path], encoding: Optional[str] = None, *args, **kwargs
):
    with open(f, "r", encoding=encoding) as handle:
        return pytests_from_buffer(handle, *args, **kwargs)


def pytests_from_buffer(buf, syntax_filter: Optional[str] = None):
    import pytest

    code_blocks = extract_from_buffer(buf)
    print(code_blocks)
    if syntax_filter is None:
        code_blocks = [(string, lineno) for string, lineno, _ in code_blocks]
    else:
        code_blocks = [
            (string, lineno)
            for string, lineno, syntax in code_blocks
            if syntax == syntax_filter
        ]

    @pytest.mark.parametrize("string, lineno", code_blocks)
    def exec_raise(string, lineno):
        try:
            # https://stackoverflow.com/a/62851176/353337
            exec(string, {"__MODULE__": "__main__"})
        except Exception:
            print(f"{buf.name} (line {lineno}):\n```")
            print(string, end="")
            print("```")
            raise

    return exec_raise
