import contextlib
import re
import sys
import warnings

# namedtuple with default arguments
# <https://stackoverflow.com/a/18348004/353337>
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Optional, Union

import pytest


@dataclass
class CodeBlock:
    code: str
    lineno: int
    syntax: Optional[str] = None
    expected_output: Optional[str] = None
    expect_exception: bool = False


def extract(*args, **kwargs):
    warnings.warn("extract() -> extract_from_file()", DeprecationWarning)
    return extract_from_file(*args, **kwargs)


def extract_from_file(
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
                out.append(CodeBlock("".join(code_block), lineno, syntax))
                continue

            # check for keywords
            m = re.match("<!--exdown-(.*)-->", previous_line.strip())
            if m is None:
                out.append(CodeBlock("".join(code_block), lineno, syntax))
                continue

            keyword = m.group(1)

            # handle special tags
            if keyword == "skip":
                continue
            elif keyword == "expected-output":
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
            elif keyword == "cont":
                if len(out) == 0:
                    raise RuntimeError(
                        "Found <!--exdown-cont--> but no previous code block."
                    )
                out[-1] = CodeBlock(
                    out[-1].code + "".join(code_block),
                    out[-1].lineno,
                    out[-1].syntax,
                    out[-1].expected_output,
                    out[-1].expect_exception,
                )
            elif keyword in ["expect-exception", "expect-error"]:
                out.append(
                    CodeBlock(
                        "".join(code_block), lineno, syntax, expect_exception=True
                    )
                )
            else:
                raise RuntimeError('Unknown exdown keyword "{keyword}."')

        previous_line = line

    return out


def pytests(*args, **kwargs):
    warnings.warn("pytests() -> pytests_from_file()", DeprecationWarning)
    return pytests_from_file(*args, **kwargs)


def pytests_from_file(
    f: Union[str, bytes, Path], encoding: Optional[str] = None, *args, **kwargs
):
    with open(f, "r", encoding=encoding) as handle:
        return pytests_from_buffer(handle, *args, **kwargs)


def pytests_from_buffer(buf, syntax_filter: Optional[str] = None):
    code_blocks = extract_from_buffer(buf)

    if syntax_filter is not None:
        code_blocks = filter(lambda cb: cb.syntax == syntax_filter, code_blocks)

    @pytest.mark.parametrize("code_block", code_blocks)
    def exec_raise(code_block):
        if code_block.expect_exception:
            with pytest.raises(Exception):
                exec(code_block.code, {"__MODULE__": "__main__"})
        else:
            with stdoutIO() as s:
                try:
                    # https://stackoverflow.com/a/62851176/353337
                    exec(code_block.code, {"__MODULE__": "__main__"})
                except Exception:
                    if hasattr(buf, "name"):
                        print(f"{buf.name} (line {code_block.lineno}):\n```")
                    else:
                        print(f"line {code_block.lineno}:\n```")
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
