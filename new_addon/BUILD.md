# Build and Development Guide

## Prerequisites

- Python 3.8 or newer
- pip (Python package manager)
- make (optional, for convenience)
- Kodi 19+ (for testing)

## Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Running Tests

```bash
# Run all tests
make test

# Or directly with pytest
pytest

# Run with coverage
pytest --cov=new_addon --cov-report=html

# Run specific test file
pytest tests/test_router.py

# Run specific test
pytest tests/test_router.py::test_route_registration
```

## Linting and Code Quality

```bash
# Run all linters
make lint

# Or individually
black new_addon/
isort new_addon/
flake8 new_addon/
mypy new_addon/
```

## Building Addon

```bash
# Create addon zip for installation
make build

# This creates: dist/plugin.video.kino.pub-<version>.zip
```

## Installing to Kodi

```bash
# Install addon to Kodi addons directory
make install

# Or manually copy to:
# Linux: ~/.kodi/addons/plugin.video.kino.pub/
# Windows: %APPDATA%\Kodi\addons\plugin.video.kino.pub\
# macOS: ~/Library/Application Support/Kodi/addons/plugin.video.kino.pub/
```

## Development Workflow

1. Create feature branch
2. Make changes
3. Run tests: `make test`
4. Run linters: `make lint`
5. Commit (pre-commit hooks will run automatically)
6. Push and create PR

## Makefile Targets

- `make test` - Run all tests
- `make lint` - Run all linters
- `make format` - Auto-format code (black + isort)
- `make typecheck` - Run mypy type checking
- `make build` - Build addon zip
- `make install` - Install to Kodi
- `make clean` - Remove build artifacts
- `make help` - Show all available targets

## Testing with Kodi

1. Enable Kodi debug logging: Settings → System → Logging
2. Set log level to "Debug"
3. Monitor logs: `tail -f ~/.kodi/temp/kodi.log`
4. Test addon functionality
5. Check for errors in logs

## Continuous Integration

GitHub Actions workflow runs on every push:
- Linting (black, isort, flake8, mypy)
- Tests (pytest with coverage)
- Build (addon zip creation)

See `.github/workflows/ci.yml` for details.

## Common Issues

### Import Errors
Ensure all dependencies are installed: `pip install -r requirements-dev.txt`

### Kodi Module Not Found
Mock Kodi modules are defined in `tests/mocks/` for testing without Kodi

### Type Checking Failures
Run `mypy new_addon/` to see detailed type errors

## Documentation

- Architecture: `.github/docs/new_architecture.md`
- API Contract: `.github/docs/api_contract.md`
- Routes: `.github/docs/routes.md`
- Playback Flow: `.github/docs/playback_flow.md`
