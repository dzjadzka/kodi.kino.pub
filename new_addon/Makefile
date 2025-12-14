.PHONY: help test lint format typecheck build install clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test:  ## Run tests
	pytest

test-watch:  ## Run tests in watch mode
	pytest-watch

coverage:  ## Generate coverage report
	pytest --cov --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:  ## Run all linters
	black --check new_addon/ tests/
	isort --check new_addon/ tests/
	flake8 new_addon/ tests/
	mypy new_addon/

format:  ## Auto-format code
	black new_addon/ tests/
	isort new_addon/ tests/

typecheck:  ## Run type checking
	mypy new_addon/

build:  ## Build addon zip
	@echo "Building addon package..."
	@mkdir -p dist
	@# TODO: Implement zip creation with addon.xml, fanart, icons, etc.
	@echo "Build not yet implemented"

install:  ## Install addon to Kodi
	@echo "Installing addon to Kodi..."
	@# TODO: Detect Kodi addons directory and copy files
	@echo "Install not yet implemented"

clean:  ## Remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

.DEFAULT_GOAL := help
