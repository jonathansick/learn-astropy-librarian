.PHONY: init
init:
	pip install pre-commit tox
	pre-commit install
	rm -rf .tox
	pip install -e ".[dev]"
