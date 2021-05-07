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
        print("HA")
        return MarkdownFile.from_parent(parent, fspath=path)


class MarkdownFile(pytest.File):
    def __init__(self, fspath, parent):
        super().__init__(fspath, parent)

    def collect(self):
        for block in extract_from_file(self.fspath):
            if block.syntax != "python":
                continue
            out = Codeblock.from_parent(parent=self, name=self.name)
            out.block = block
            yield out


class Codeblock(pytest.Item):
    def __init__(self, name, parent):
        super().__init__(name, parent=parent)
        self.block = None

    def runtest(self):
        if self.block.expect_exception:
            with pytest.raises(Exception):
                exec(self.block.code, {"__MODULE__": "__main__"})
        else:
            with stdout_io() as s:
                try:
                    # https://stackoverflow.com/a/62851176/353337
                    exec(self.block.code, {"__MODULE__": "__main__"})
                except Exception:
                    # if hasattr(buf, "name"):
                    #     print(f"{buf.name} (line {self.code_block.lineno}):\n```")
                    # else:
                    print(self.parent)
                    print(f"line {self.block.lineno}:\n```")
                    print(self.block.code, end="")
                    print("```")
                    raise

            output = s.getvalue()
            if self.block.expected_output is not None:
                if self.block.expected_output != output:
                    raise RuntimeError(
                        f"Expected \n```\n{self.block.expected_output}```\n"
                        + f"but got\n```\n{output}```"
                    )
