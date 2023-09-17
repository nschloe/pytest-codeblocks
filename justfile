version := `python3 -c "from src.pytest_codeblocks.__about__ import __version__; print(__version__)"`

default:
	@echo "\"just publish\"?"

publish:
	@if [ "$(git rev-parse --abbrev-ref HEAD)" != "main" ]; then exit 1; fi
	gh release create "v{{version}}"
	flit publish

clean:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
	@rm -rf src/*.egg-info/ build/ dist/ .tox/

format:
	ruff src/ tests/ --fix
	black src/ tests/
	blacken-docs README.md

lint:
	pre-commit run --all
