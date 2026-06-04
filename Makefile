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
	@rm -rf dist/ build/
	@find . -name "*.egg-info" -type d -exec rm -r {} +
	@find . -name "__pycache__" -type d -exec rm -r {} +
