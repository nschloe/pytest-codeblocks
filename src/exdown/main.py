import contextlib
import sys
from collections import namedtuple
from io import StringIO
from pathlib import Path
from typing import Optional, Union

CodeBlock = namedtuple("CodeBlock", ["code", "lineno", "syntax", "expected_output"])


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

            if previous_line is None:
                out.append(CodeBlock("".join(code_block), lineno, syntax, None))
                continue

            # handle special tags
            if previous_line.strip() == "<!--exdown-skip-->":
                continue
            elif previous_line.strip() == "<!--exdown-expected-output-->":
                if len(out) == 0:
                    raise RuntimeError(
                        "Found <!--exdown-expected-output--> "
                        + "but no previous code block."
                    )
                if out[-1].expected_output is not None:
                    raise RuntimeError(
                        "Found <!--exdown-expected-output--> "
                        + "but block already has expected_output."
                    )
                expected_output = "\n".join(code_block)
                out[-1] = CodeBlock(
                    out[-1].code, out[-1].lineno, out[-1].syntax, expected_output
                )
            elif previous_line.strip() == "<!--exdown-cont-->":
                if len(out) == 0:
                    raise RuntimeError(
                        "Found <!--exdown-cont--> but no previous code block."
                    )
                out[-1] = CodeBlock(
                    out[-1].code + "".join(code_block),
                    out[-1].lineno,
                    out[-1].syntax,
                    out[-1].expected_output,
                )
            else:
                out.append(CodeBlock("".join(code_block), lineno, syntax, None))

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
    if syntax_filter is not None:
        code_blocks = filter(lambda cb: cb.syntax == syntax_filter, code_blocks)

    @pytest.mark.parametrize("code_block", code_blocks)
    def exec_raise(code_block):
        with stdoutIO() as s:
            try:
                # https://stackoverflow.com/a/62851176/353337
                exec(code_block.code, {"__MODULE__": "__main__"})
            except Exception:
                print(f"{buf.name} (line {code_block.lineno}):\n```")
                print(code_block.code, end="")
                print("```")
                raise

        output = s.getvalue()
        if code_block.expected_output is not None:
            if code_block.expected_output != output:
                raise RuntimeError(
                    f"Expected \n```\n{code_block.expected_output}```\n"
                    + f"but got\n```\n{output}```"
                )

    return exec_raise


# https://stackoverflow.com/a/3906390/353337
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
