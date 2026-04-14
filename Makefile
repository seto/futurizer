.PHONY: format test build publish clean

TARGET = $(if $(t),$(t),.)

format:
	@black $(TARGET)
	@isort $(TARGET)

test:
	@pytest

build:
	@rm -rf dist/ build/ *.egg-info
	@python3 -m build

publish: build
	@python3 -m twine upload dist/*

clean:
	@find . -name "__pycache__" -type d -exec rm -r {} +
