version := `python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"`

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
	ruff format .
	ruff check --fix .
	blacken-docs README.md

lint:
	prek run --all-files
