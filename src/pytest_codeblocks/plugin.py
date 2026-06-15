import subprocess
import re
import sys

import pytest

from .main import extract_from_file, stdout_io


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        "--codeblocks",
        action="store_true",
        help="enable testing of code blocks",
    )


def pytest_collect_file(file_path, parent):
    config = parent.config
    if config.option.codeblocks and file_path.suffix == ".md":
        return MarkdownFile.from_parent(parent, path=file_path)


class MarkdownFile(pytest.File):
    def collect(self):
        for block in extract_from_file(self.path):
            if block.syntax not in ["python", "sh", "bash"]:
                continue
            # https://docs.pytest.org/en/stable/deprecations.html#node-construction-changed-to-node-from-parent
            # The name makes sure that tests appear as
            # ```
            # README.md::line 56
            # ```
            out = TestBlock.from_parent(parent=self, name=f"line {block.lineno}")
            out.obj = block

            for mark in block.marks:
                out.add_marker(eval(mark, {"sys": sys, "pytest": pytest}))

            yield out


class TestBlock(pytest.Item):
    def __init__(self, name, parent, obj=None):
        super().__init__(name, parent=parent)
        self.obj = obj

    def runtest(self):
        output = None

        if self.obj.importorskip is not None:
            try:
                __import__(self.obj.importorskip)
            except ImportError:
                pytest.skip()

        if self.obj.syntax == "python":
            with stdout_io() as s:
                try:
                    # https://stackoverflow.com/a/62851176/353337
                    exec(self.obj.code, {"__MODULE__": "__main__"})
                except Exception as e:
                    raise RuntimeError(
                        f"{self.name}, line {self.obj.lineno}:\n```\n"
                        + self.obj.code
                        + "```\n\n"
                        + f"{e}"
                    )
            output = s.getvalue()
        else:
            executable = {
                "sh": None,
                "bash": "/bin/bash",
                "zsh": "/bin/zsh",
            }[self.obj.syntax]

            ret = subprocess.run(
                self.obj.code,
                shell=True,
                check=True,
                capture_output=True,
                executable=executable,
            )
            output = ret.stdout.decode()

        if output is not None and self.obj.expected_output is not None:
            str0 = self.obj.expected_output
            str1 = output

            if self.obj.expected_output_ignore_whitespace:
                str0 = re.sub(r"\s+", "", str0)
                str1 = re.sub(r"\s+", "", str1)

            if str0 != str1:
                raise RuntimeError(
                    f"{self.name}, line {self.obj.lineno}:\n```\n"
                    + f"Expected output\n```\n{self.obj.expected_output}```\n"
                    + f"but got\n```\n{output}```"
                )

    def repr_failure(self, excinfo):
        return excinfo.value.args[0]

    def reportinfo(self):
        return (self.path, -1, "code block check")
