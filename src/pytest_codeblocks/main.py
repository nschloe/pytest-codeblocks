import contextlib
import re
import sys

# namedtuple with default arguments
# <https://stackoverflow.com/a/18348004/353337>
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Optional, Union


@dataclass
class CodeBlock:
    code: str
    lineno: int
    syntax: Optional[str] = None
    expected_output: Optional[str] = None
    expect_exception: bool = False


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
            m = re.match("<!--pytest-codeblocks:(.*)-->", previous_line.strip())
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
                        "Found <!--pytest-codeblocks-expected-output--> "
                        + "but no previous code block."
                    )
                if out[-1].expected_output is not None:
                    raise RuntimeError(
                        "Found <!--pytest-codeblocks-expected-output--> "
                        + "but block already has expected_output."
                    )
                expected_output = "".join(code_block)
                out[-1] = CodeBlock(
                    out[-1].code, out[-1].lineno, out[-1].syntax, expected_output
                )
            elif keyword == "cont":
                if len(out) == 0:
                    raise RuntimeError(
                        "Found <!--pytest-codeblocks-cont--> but no previous code block."
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
                raise RuntimeError('Unknown pytest-codeblocks keyword "{keyword}."')

        previous_line = line

    return out


# https://stackoverflow.com/a/3906390/353337
@contextlib.contextmanager
def stdout_io(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
