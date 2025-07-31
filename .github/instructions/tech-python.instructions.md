---
description: Python development standards and best practices
applyTo: "**/*.py,**/*.pyi"
---

# Python Development Standards

## 🏗️ Architecture & Navigation
- **Root Standards**: [General Coding Standards](./tech-general-coding.instructions.md)
- **Security Guidelines**: [Security & OWASP](./security-owasp.instructions.md)
- **Performance Guidelines**: [Performance Optimization](./tech-performance-optimization.instructions.md)
- **Framework Extensions**: No Python-specific frameworks currently defined

---

## 🐍 Python-Specific Context

- **Python Version**: 3.9+ (prefer 3.11+ for performance)
- **Code Style**: PEP 8, PEP 257 (docstrings), PEP 484 (type hints)
- **Common Frameworks**: FastAPI, Flask, Django, Pandas, Pydantic
- **Architecture Patterns**: MVC, Clean Architecture, Event-Driven, Microservices
- **Package Management**: Poetry (preferred), pip, conda

## 🔧 Python Language Standards

### Type Safety & Code Quality
- **Type Hints**: Use type hints for all function parameters, return values, and class attributes
- **Static Analysis**: Use mypy for type checking, black for formatting, isort for imports
- **Docstrings**: Follow PEP 257 with comprehensive docstrings for all public APIs
- **Code Style**: Strict adherence to PEP 8 with line length 88-100 characters

### Python-Specific Patterns
- **Pythonic Code**: Embrace Python idioms (list comprehensions, context managers, decorators)
- **Class Design**: Use dataclasses or Pydantic for data containers, prefer composition
- **Error Handling**: Use specific exception types, implement proper exception hierarchies
- **Resource Management**: Always use context managers for file I/O, database connections
- **Async Programming**: Use asyncio patterns for I/O-bound operations

### Data Handling & Validation
- **Input Validation**: Use Pydantic models for complex data validation
- **Data Processing**: Leverage pandas for data manipulation, NumPy for numerical operations
- **Database Operations**: Use SQLAlchemy for ORM, prefer async drivers when possible
- **API Development**: FastAPI for modern APIs, Flask for simpler applications

## 📁 Project Structure

```
src/
├── __init__.py
├── main.py                 # Application entry point
├── config/
│   ├── __init__.py
│   ├── settings.py         # Pydantic settings management
│   └── database.py         # Database configuration
├── core/
│   ├── __init__.py
│   ├── dependencies.py     # Dependency injection
│   ├── exceptions.py       # Custom exception classes
│   └── middleware.py       # Custom middleware
├── models/
│   ├── __init__.py
│   ├── base.py            # Base model classes
│   └── domain/            # Domain-specific models
├── repositories/
│   ├── __init__.py
│   ├── base.py            # Base repository pattern
│   └── implementations/   # Concrete repositories
├── services/
│   ├── __init__.py
│   ├── base.py            # Base service classes
│   └── implementations/   # Business logic services
├── api/                   # FastAPI/Flask routes
│   ├── __init__.py
│   ├── dependencies.py
│   └── v1/
│       ├── __init__.py
│       └── endpoints/
└── utils/
    ├── __init__.py
    ├── logging.py         # Logging configuration
    └── helpers.py         # Utility functions

tests/
├── __init__.py
├── conftest.py            # Pytest configuration
├── unit/                  # Unit tests
├── integration/           # Integration tests
└── fixtures/              # Test data fixtures
```

## 🧪 Python Testing Standards

### Testing Framework & Tools
- **Primary Framework**: pytest with pytest-asyncio for async tests
- **Coverage**: pytest-cov with minimum 90% coverage requirement
- **Mocking**: unittest.mock, pytest-mock for external dependencies
- **Database Testing**: Use test databases or in-memory SQLite for tests
- **API Testing**: httpx for async HTTP testing, requests for synchronous

### Test Organization
- **Test Structure**: Mirror source structure in tests directory
- **Test Naming**: `test_<functionality>_<scenario>_<expected_result>`
- **Fixtures**: Use pytest fixtures for test data and setup/teardown
- **Parametrized Tests**: Use pytest.mark.parametrize for multiple test cases
- **Test Categories**: Unit tests, integration tests, end-to-end tests

## 🚫 Python Anti-Patterns

### Code Smells to Avoid
- **Import Issues**: Wildcard imports (`from module import *`), circular imports
- **Global State**: Mutable global variables, global configuration without proper management
- **Performance**: Premature optimization, inefficient string concatenation
- **Error Handling**: Bare except clauses, swallowing exceptions without logging
- **Security**: Using eval(), pickle for untrusted data, hardcoded secrets

### Common Mistakes
- **Mutable Default Arguments**: `def func(items=[]):` - use `None` and initialize inside
- **Late Binding Closures**: Be aware of variable capture in loops
- **Missing Virtual Environments**: Always use virtual environments for project isolation
- **Blocking Operations**: Using synchronous operations in async contexts

## 🎯 Python Best Practices

### Development Workflow
- **Environment Management**: Use Poetry or pipenv for dependency management
- **Code Quality Gates**: Pre-commit hooks with black, isort, mypy, flake8
- **Documentation**: Sphinx for documentation generation from docstrings
- **Dependency Updates**: Regular security scans with safety, dependabot
- **Version Management**: Semantic versioning with proper changelog maintenance

### Production Considerations
- **Logging**: Structured logging with JSON format for production systems
- **Monitoring**: Integrate with APM tools (DataDog, New Relic) for performance monitoring
- **Configuration**: Use environment-based configuration with validation
- **Security**: Regular dependency scanning, secure coding practices
- **Performance**: Profile with cProfile, optimize bottlenecks identified through monitoring

## � Reference Links

### Official Documentation
- [Python Documentation](https://docs.python.org/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [PEP 257 Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 484 Type Hints](https://peps.python.org/pep-0484/)

### Essential Tools & Libraries
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Poetry Package Manager](https://python-poetry.org/)

```text
src/
  controllers/
  services/
  repositories/
  schemas/
  utils/
  config/
tests/
  unit/
  integration/
```

## 🧶 Patterns

### ✅ Patterns to Follow

Python-specific patterns:
- Use the Repository Pattern and Dependency Injection (e.g., via `Depends` in FastAPI)
- Validate data using Pydantic models
- Use environment variables via `dotenv` or `os.environ`
- Write modular, reusable code organized by concerns (e.g., controller, service, data layer)
- Favor async endpoints for I/O-bound services (FastAPI, aiohttp)
- Document functions and classes with docstrings

### 🚫 Patterns to Avoid

Python-specific anti-patterns:
- Don't use wildcard imports (`from module import *`)
- Avoid business logic inside views/routes

## 🧪 Testing Guidelines

**Follow universal testing standards in [tech-general-coding.instructions.md](./tech-general-coding.instructions.md).**

Python-specific testing:
- Use `pytest` or `unittest` for unit and integration tests
- Mock external services with `unittest.mock` or `pytest-mock`
- Use fixtures to set up and tear down test data

## 🧩 Example Prompts

- `Copilot, create a FastAPI endpoint that returns all users from the database.`
- `Copilot, write a Pydantic model for a product with id, name, and optional price.`
- `Copilot, implement a CLI command that uploads a CSV file and logs a summary.`
- `Copilot, write a pytest test for the transform_data function using a mock input.`

## 🔁 Iteration & Review

- Review Copilot output before committing
- Add comments to clarify intent if Copilot generates incorrect or unclear suggestions
- Use linters (flake8, pylint) and formatters (black, isort) as part of the review pipeline
- Refactor output to follow project conventions

## 📚 References

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Logging Best Practices](https://docs.python.org/3/howto/logging.html)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Poetry](https://python-poetry.org/docs/)ription: Project coding standards for Python
app### 🚫 Patterns to Avoid

Python-specific anti-patterns:
- Don't use wildcard imports (`from module import *`)
- Avoid business logic inside views/routes**/*.py,**/*.pyi"
---

# GitHub Copilot Instructions

These instructions define how GitHub Copilot should assist with this project. The goal is to ensure consistent, high-quality code generation aligned with our conventions, stack, and best practices.

## 🧠 Context

- **Project Type**: Web API / Data Pipeline / CLI Tool / ML App
- **Language**: Python
- **Framework / Libraries**: FastAPI / Flask / Django / Pandas / Pydantic / Poetry
- **Architecture**: MVC / Clean Architecture / Event-Driven / Microservices

## 🔧 General Guidelines

**Follow universal coding standards in [tech-general-coding.instructions.md](./tech-general-coding.instructions.md) for naming conventions, error handling, logging, testing, and code organization.**

Python-specific guidelines:
- Use Pythonic patterns (PEP8, PEP257)
- Prefer named functions and class-based structures over inline lambdas
- Use type hints where applicable (`typing` module)
- Follow black or isort for formatting and import order
- Emphasize simplicity, readability, and DRY principles

## 📁 File Structure

Use this structure as a guide when creating or updating files:

```text
src/
  controllers/
  services/
  repositories/
  schemas/
  utils/
  config/
tests/
  unit/
  integration/
```

## 🧶 Patterns

### ✅ Patterns to Follow

Python-specific patterns:
- Use the Repository Pattern and Dependency Injection (e.g., via `Depends` in FastAPI)
- Validate data using Pydantic models
- Use environment variables via `dotenv` or `os.environ`
- Write modular, reusable code organized by concerns (e.g., controller, service, data layer)
- Favor async endpoints for I/O-bound services (FastAPI, aiohttp)
- Document functions and classes with docstrings

### 🚫 Patterns to Avoid

- Don’t use wildcard imports (`from module import *`).
- Avoid global state unless encapsulated in a singleton or config manager.
- Don’t hardcode secrets or config values—use `.env`.
- Don’t expose internal stack traces in production environments.
- Avoid business logic inside views/routes.

## 🧪 Testing Guidelines

- Use `pytest` or `unittest` for unit and integration tests.
- Mock external services with `unittest.mock` or `pytest-mock`.
- Use fixtures to set up and tear down test data.
- Aim for high coverage on core logic and low-level utilities.
- Test both happy paths and edge cases.

## 🧩 Example Prompts

- `Copilot, create a FastAPI endpoint that returns all users from the database.`
- `Copilot, write a Pydantic model for a product with id, name, and optional price.`
- `Copilot, implement a CLI command that uploads a CSV file and logs a summary.`
- `Copilot, write a pytest test for the transform_data function using a mock input.`

## 🔁 Iteration & Review

- Review Copilot output before committing.
- Add comments to clarify intent if Copilot generates incorrect or unclear suggestions.
- Use linters (flake8, pylint) and formatters (black, isort) as part of the review pipeline.
- Refactor output to follow project conventions.

## 📚 References

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Logging Best Practices](https://docs.python.org/3/howto/logging.html)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Poetry](https://python-poetry.org/docs/)