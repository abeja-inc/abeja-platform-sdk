# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ABEJA Platform SDK is a Python SDK for interacting with the ABEJA Platform services (Datalake, Dataset, Training, Deployment, etc.). The SDK is distributed via PyPI as `abeja-sdk`.

## Key Architecture

### Service Modules
Each ABEJA Platform service has its own module under `abeja/`:
- `datalake/` - Data lake service for file storage
- `datasets/` - Dataset management
- `training/` - Model training operations
- `deployments/` - Model deployment
- `endpoints/` - API endpoint management
- `models/` - Model registry
- `notebook/` - Jupyter notebook integration
- `secret/` and `secret_version/` - Secret management
- `opsbeellm/` - LLM operations service
- `tracking/` - Experiment tracking

### Core Components
- `abeja/common/connection.py` - HTTP connection management with retry logic
- `abeja/common/auth.py` - Authentication handling
- `abeja/base_client.py` - Base client class
- `abeja/common/api_client.py` - Base API client class

Each service typically has:
- `api/client.py` - Low-level API client
- `client.py` - High-level client interface
- Model classes for request/response objects

## Development Commands

### Running Tests
```bash
# Run all tests with linting and type checking
make test

# Run specific test file or directory
poetry run pytest tests/path/to/test.py

# Run tests with coverage
poetry run pytest tests/ --cov=abeja

# Run integration tests (requires environment setup)
make integration_test
```

### Code Quality
```bash
# Run linting
make lint
# or
poetry run flake8 abeja tests

# Run type checking
make mypy

# Format code
make format
# or
poetry run autopep8 -r --in-place --aggressive --aggressive abeja tests
```

### Building & Documentation
```bash
# Build wheel package
make dist

# Generate documentation
poetry install -E docs
make docs
```

### Development Setup
```bash
# Install dependencies with Poetry
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Create local wheel for testing
make dist
```

## Environment Variables

The SDK uses these key environment variables:
- `ABEJA_API_URL` - API endpoint (default: https://api.abeja.io)
- `ABEJA_ORGANIZATION_ID` - Organization identifier
- `ABEJA_PLATFORM_USER_ID` - User ID for authentication
- `ABEJA_PLATFORM_DATASOURCE_ID` - Datasource ID
- `ABEJA_PLATFORM_DATASOURCE_SECRET` - Datasource secret
- `ABEJA_SDK_CONNECTION_TIMEOUT` - Connection timeout (default: 30)
- `ABEJA_SDK_MAX_RETRY_COUNT` - Max retry attempts (default: 5)
- `ABEJA_STORAGE_DIR_PATH` - Local storage path for downloads
- `ABEJA_TRAINING_RESULT_DIR` - Training result directory

## Testing Approach

Tests are organized to mirror the SDK structure under `tests/`:
- Unit tests for each service module
- `tests/conftest.py` contains pytest fixtures
- `integration_tests/` for end-to-end testing (requires live environment)

Use `parameterized` and `mock` for test variations and mocking external services.

## Release Process

The SDK uses a PR-based release flow:
- `develop` - Development branch
- `staging` - Release-candidate packages
- `master` - Production packages

Merge `develop` into `staging` to publish the next automatically numbered RC.
Merge `staging` into `master` to publish the final version. GitHub Actions runs
unit and integration tests before publishing to PyPI, then dispatches the exact
published version to `platform-system-test`. See `.github/CICD.md` for required
GitHub Environments, secrets, branch protection, and the decommission checklist.
