import pathlib

import exdown

this_dir = pathlib.Path(__file__).resolve().parent

test_example = exdown.pytests_from_file(this_dir / "example.md", syntax_filter="python")

# Doesn't work from every folder, e.g., fails for `cd test && pytest`
# test_readme = exdown.pytests_from_file(this_dir / ".." / "README.md", syntax_filter="python")
