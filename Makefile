.PHONY: format test clean build publish

TARGET = $(if $(t),$(t),.)

format:
	@echo "Formatting in $(TARGET)"
	@black $(TARGET)
	@isort $(TARGET)
	@echo "Done!"

test:
	@pytest

clean:
	@echo "Cleaning up..."
	@rm -rf dist/ build/
	@find . -name "*.egg-info" -type d -exec rm -r {} +
	@find . -name "__pycache__" -type d -exec rm -r {} +
	@echo "Done!"

build: clean
	@python3 -m build

publish: build
	@python3 -m twine upload dist/*
