from pathlib import Path
from typing import Optional, Union


def extract(
    f: Union[str, bytes, Path], encoding: Optional[str] = None, *args, **kwargs
):
    with open(f, "r", encoding=encoding) as handle:
        return from_buffer(handle, *args, **kwargs)


def from_buffer(
    f,
    max_num_lines: int = 10000,
    syntax_filter: Optional[str] = None,
):
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
            syntax = line.lstrip()[3:]
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

            if syntax_filter and syntax_filter.strip() != syntax.strip():
                continue
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
                out[-1] = (out[-1][0] + "".join(code_block), out[-1][1])
            else:
                out.append(("".join(code_block), lineno))

        previous_line = line

    return out


def pytests(filename: Union[str, bytes, Path], syntax_filter: Optional[str] = None):
    import pytest

    @pytest.mark.parametrize(
        "string, lineno", extract(filename, syntax_filter=syntax_filter)
    )
    def exec_raise(string, lineno):
        try:
            # https://stackoverflow.com/a/62851176/353337
            exec(string, {"__MODULE__": "__main__"})
        except Exception:
            print(f"{filename} (line {lineno}):\n```")
            print(string, end="")
            print("```")
            raise

    return exec_raise
