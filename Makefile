.PHONY: fmt lint test install clean

# Format code
fmt:
	uv run black src/ tests/
	uv run ruff check src/ tests/ --fix

# Lint code
lint:
	uv run black src/ tests/ --check
	uv run ruff check src/ tests/

# Run tests
test:
	uv run pytest tests/ -v

# Install dependencies
install:
	uv sync --extra dev

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".ruff_cache" -exec rm -r {} +
