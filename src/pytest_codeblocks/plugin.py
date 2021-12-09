#
# Take a look at the example
# https://docs.pytest.org/en/stable/example/nonpython.html
#
import subprocess

import pytest

from .main import extract_from_file, stdout_io


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        "--codeblocks", action="store_true", help="enable testing of codeblocks"
    )


def pytest_collect_file(path, parent):
    config = parent.config
    if config.option.codeblocks and path.ext == ".md":
        return MarkdownFile.from_parent(parent, fspath=path)


class MarkdownFile(pytest.File):
    def __init__(self, fspath, parent):
        super().__init__(fspath, parent)

    def collect(self):
        for block in extract_from_file(self.fspath):
            if block.syntax not in ["python", "sh", "bash"]:
                continue
            # https://docs.pytest.org/en/stable/deprecations.html#node-construction-changed-to-node-from-parent
            out = TestBlock.from_parent(parent=self, name=self.name)
            out.obj = block
            yield out


class TestBlock(pytest.Item):
    def __init__(self, name, parent, obj=None):
        super().__init__(name, parent=parent)
        self.obj = obj

    # TODO for python 3.7+, stdout=subprocess.PIPE can be replaced by
    #      capture_output=True
    def runtest(self):
        assert self.obj is not None
        output = None

        if self.obj.skip:
            pytest.skip()

        if self.obj.skipif is not None:
            # needed for sys.version_info in skipif eval():
            import sys

            if eval(self.obj.skipif):
                pytest.skip()

        if self.obj.syntax == "python":
            if self.obj.expect_exception:
                with pytest.raises(Exception):
                    exec(self.obj.code, {"__MODULE__": "__main__"})
            else:
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
            assert self.obj.syntax in ["sh", "bash"]
            executable = {
                "sh": None,
                "bash": "/bin/bash",
                "zsh": "/bin/zsh",
            }[self.obj.syntax]
            if self.obj.expect_exception:
                with pytest.raises(Exception):
                    subprocess.run(
                        self.obj.code, shell=True, check=True, executable=executable
                    )
            else:
                ret = subprocess.run(
                    self.obj.code,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    executable=executable,
                )
                output = ret.stdout.decode()

        if output is not None and self.obj.expected_output is not None:
            if self.obj.expected_output != output:
                raise RuntimeError(
                    f"{self.name}, line {self.obj.lineno}:\n```\n"
                    + f"Expected output\n```\n{self.obj.expected_output}```\n"
                    + f"but got\n```\n{output}```"
                )

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        # if isinstance(excinfo.value, CodeblockException):
        return excinfo.value.args[0]
        # if excinfo.errisinstance(RuntimeError):
        #     return excinfo.value.args[0].stdout
        # return super().repr_failure(excinfo)

    def reportinfo(self):
        return (self.fspath, -1, "code block check")
