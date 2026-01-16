# Contributing to Sisense MCP Server

We welcome contributions to the Sisense MCP server! This document provides guidelines for contributing.

## Getting Started

1. **Fork the repository** and clone your fork
2. **Install development dependencies:**
   ```bash
   uv sync --extra dev
   ```

## Development Workflow

### Code Style

We use the following tools for code quality:

- **Black** - Code formatting
- **Ruff** - Linting and import sorting
- **Pytest** - Testing

### Running Tests

```bash
# Run all tests
make test

# Or directly with pytest
uv run pytest tests/ -v
```

### Code Formatting

```bash
# Format code
make fmt

# Check formatting
make lint
```

### Before Submitting

1. **Run tests** - Ensure all tests pass:
   ```bash
   make test
   ```

2. **Format code** - Ensure code is properly formatted:
   ```bash
   make fmt
   ```

3. **Check linting** - Ensure linting passes:
   ```bash
   make lint
   ```

## Submitting Changes

### Pull Request Process

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit them:
   ```bash
   git commit -m "Add feature: description"
   ```

3. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open a Pull Request** on GitHub

### Pull Request Guidelines

- **Keep PRs focused** - One feature or bug fix per PR
- **Write tests** - New features should include tests
- **Update documentation** - Update README.md if needed
- **Follow code style** - Run `make fmt` and `make lint` before submitting

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Use mocks for external API calls
- Test both success and error paths
- Aim for >80% code coverage

### Test Structure

Tests are located in the `tests/` directory:
- `test_sisense_client.py` - HTTP client tests
- `test_elasticube_service.py` - ElastiCube service tests
- `test_dashboard_service.py` - Dashboard service tests
- `test_elasticube_tools.py` - ElastiCube tool tests
- `test_dashboard_tools.py` - Dashboard tool tests
- `test_server.py` - Integration tests

## Code Structure

The codebase is organized as follows:

```
src/
  client/          # HTTP client (pure API calls)
  services/       # Business logic layer
  tools/          # MCP tool definitions and handlers
  server.py       # MCP server setup
  config.py       # Configuration
```

**Key principles:**
- **Separation of concerns** - Client handles HTTP, services handle business logic, tools handle MCP protocol
- **Reusability** - Services can be used independently of MCP tools
- **Testability** - Each layer can be tested independently with mocks

## Reporting Issues

When reporting issues, please include:

- **Description** - What happened?
- **Expected behavior** - What should have happened?
- **Steps to reproduce** - How can we reproduce this?
- **Environment** - Python version, OS, Sisense version
- **Error messages** - Any error messages or logs

## Questions?

If you have questions, please open an issue on GitHub.

Thank you for contributing! 🎉
