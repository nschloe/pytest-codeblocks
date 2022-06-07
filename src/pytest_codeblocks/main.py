from __future__ import annotations

import contextlib
import re
import sys
import warnings

# namedtuple with default arguments
# <https://stackoverflow.com/a/18348004/353337>
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path


@dataclass
class CodeBlock:
    code: str
    lineno: int
    syntax: str | None = None
    expected_output: str | None = None
    importorskip: str | None = None
    marks: list[str] = field(default_factory=lambda: [])


def extract_from_file(
    f: str | bytes | Path, encoding: str | None = "utf-8", *args, **kwargs
):
    with open(f, encoding=encoding) as handle:
        return extract_from_buffer(handle, *args, **kwargs)


def extract_from_buffer(f, max_num_lines: int = 10000) -> list[CodeBlock]:
    out = []
    marks = []
    continued_block = None
    expected_output_block = None
    importorskip = None
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

        m = re.match(
            r"<!--[-\s]*pytest-codeblocks:(.*)-->",
            line.strip(),
        )
        if m is not None:
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
                expected_output_block = out[-1]

            elif keyword == "cont":
                if len(out) == 0:
                    raise RuntimeError(
                        "Found <!--pytest-codeblocks-cont--> but no previous code block."
                    )
                continued_block = out[-1]

            elif keyword == "skip":
                warnings.warn(
                    "pytest-codeblocks:skip is deprecated. Use pytest.mark.skip",
                    DeprecationWarning,
                )
                marks.append("pytest.mark.skip")

            elif keyword.startswith("skipif"):
                warnings.warn(
                    "pytest-codeblocks:skipif is deprecated. Use pytest.mark.skipif",
                    DeprecationWarning,
                )
                m = re.match(r"skipif\((.*)\)", keyword)
                if m is None:
                    raise RuntimeError(
                        "pytest-codeblocks: Expected skipif(some-condition)"
                    )
                marks.append(f"pytest.mark.skipif({m.group(1)}, reason='')")

            elif keyword.startswith("importorskip"):
                m = re.match(r"importorskip\((.*)\)", keyword)
                if m is None:
                    raise RuntimeError(
                        "pytest-codeblocks: Expected importorskip(some-module)"
                    )
                importorskip = m.group(1)

            elif keyword in ["expect-exception", "expect-error"]:
                warnings.warn(
                    f"pytest-codeblocks:{keyword} is deprecated. Use pytest.mark.xfail",
                    DeprecationWarning,
                )
                marks.append("pytest.mark.xfail")

            else:
                raise RuntimeError(f'Unknown pytest-codeblocks keyword "{keyword}."')

            continue

        m = re.match(
            r"<!--[-\s]*(pytest\.mark\..*)-->",
            line.strip(),
        )
        if m is not None:
            marks.append(m.group(1))
            continue

        lsline = line.lstrip()
        if lsline.startswith("```"):
            # normally 3, but can be more:
            num_leading_backticks = len(lsline) - len(lsline.lstrip("`"))
            syntax = line.strip()[num_leading_backticks:]
            num_leading_spaces = len(line) - len(lsline)
            lineno = k - 1
            # read the block
            code_block = []
            while True:
                line = f.readline()
                lsline = line.lstrip()
                k += 1
                if not line:
                    raise RuntimeError("Hit end-of-file prematurely. Syntax error?")
                if k > max_num_lines:
                    raise RuntimeError(
                        f"File too large (> {max_num_lines} lines). Set max_num_lines."
                    )
                # check if end of block
                if lsline[:num_leading_backticks] == "`" * num_leading_backticks:
                    break
                # Cut (at most) num_leading_spaces leading spaces
                nls = min(num_leading_spaces, len(line) - len(lsline))
                line = line[nls:]
                code_block.append(line)

            code = "".join(code_block)

            if continued_block:
                continued_block.code += code
                continued_block = None

            elif expected_output_block:
                expected_output_block.expected_output = code
                expected_output_block = None

            else:
                out.append(
                    CodeBlock(
                        code,
                        lineno,
                        syntax,
                        marks=marks,
                        importorskip=importorskip,
                    )
                )
                marks = []
                importorskip = None

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
