# import pathlib
#
# import pytest_codeblocks
#
# this_dir = pathlib.Path(__file__).resolve().parent
#
# test_example = pytest_codeblocks.pytests_from_file(
#     this_dir / "example.md", syntax_filter="python"
# )

# Doesn't work from every folder, e.g., fails for `cd test && pytest`
# test_readme = pytest_codeblocks.pytests_from_file(this_dir / ".." / "README.md", syntax_filter="python")
