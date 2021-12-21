from __future__ import annotations

import contextlib
import re
import sys

# namedtuple with default arguments
# <https://stackoverflow.com/a/18348004/353337>
from dataclasses import dataclass
from io import StringIO
from pathlib import Path


@dataclass
class CodeBlock:
    code: str
    lineno: int
    syntax: str | None = None
    expected_output: str | None = None
    expect_exception: bool = False
    skip: bool = False
    skipif: str | None = None


def extract_from_file(
    f: str | bytes | Path, encoding: str | None = "utf-8", *args, **kwargs
):
    with open(f, encoding=encoding) as handle:
        return extract_from_buffer(handle, *args, **kwargs)


def extract_from_buffer(f, max_num_lines: int = 10000) -> list[CodeBlock]:
    out = []
    previous_nonempty_line = None
    k = 1

    while True:
        line = f.readline()

        if k == 1 and line.strip() == "<!--pytest-codeblocks:skipfile-->":
            return []

        k += 1
        if not line:
            # EOF
            break

        if line.strip() == "":
            continue

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

            if previous_nonempty_line is None:
                out.append(CodeBlock("".join(code_block), lineno, syntax))
                continue

            # check for keywords
            m = re.match(
                r"<!--[-\s]*pytest-codeblocks:(.*)-->",
                previous_nonempty_line.strip(),
            )
            if m is None:
                out.append(CodeBlock("".join(code_block), lineno, syntax))
                continue

            keyword = m.group(1).strip("- ")

            # handle special tags
            if keyword == "expected-output":
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
                out[-1].expected_output = "".join(code_block)
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
            elif keyword == "skip":
                out.append(CodeBlock("".join(code_block), lineno, syntax, skip=True))
            elif keyword.startswith("skipif"):
                m = re.match(r"skipif\((.*)\)", keyword)
                if m is None:
                    raise RuntimeError(
                        "pytest-codeblocks: Expected skipif(some-condition)"
                    )
                out.append(
                    CodeBlock("".join(code_block), lineno, syntax, skipif=m.group(1))
                )
            elif keyword in ["expect-exception", "expect-error"]:
                out.append(
                    CodeBlock(
                        "".join(code_block), lineno, syntax, expect_exception=True
                    )
                )
            else:
                raise RuntimeError(f'Unknown pytest-codeblocks keyword "{keyword}."')

        previous_nonempty_line = line

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
