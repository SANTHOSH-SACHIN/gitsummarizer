# Contributing to GitSummarizer

Thank you for your interest in contributing to GitSummarizer! This document provides guidelines and instructions for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/gitsummarizer.git
   cd gitsummarizer
   ```

3. Set up a development environment:
   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install development dependencies
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and add tests for new functionality

3. Run tests to ensure your changes don't break existing functionality:
   ```bash
   pytest
   ```

4. Format your code:
   ```bash
   black gitsummarizer
   isort gitsummarizer
   ```

5. Run linting:
   ```bash
   flake8 gitsummarizer
   ```

6. Commit your changes with a descriptive commit message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```

7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. Open a Pull Request from your fork to the main repository

## Adding a New LLM Provider

1. Create a new file in `gitsummarizer/models/` (e.g., `your_provider.py`)
2. Implement the `LLMProvider` interface from `gitsummarizer/models/base.py`
3. Add your provider to the `PROVIDERS` dictionary in `gitsummarizer/models/__init__.py`
4. Add tests for your provider in `tests/models/test_your_provider.py`

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function arguments and return values
- Document functions, classes, and modules with docstrings
- Keep lines under 100 characters where possible

## Pull Request Guidelines

- Update documentation for significant changes
- Add tests for new features
- Keep PRs focused on a single change or feature
- Rebase your branch onto the latest main branch before submitting

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=gitsummarizer

# Run specific test
pytest tests/test_specific_file.py
```

## Reporting Issues

When reporting issues, please include:

- A clear, descriptive title
- A detailed description of the issue
- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- Environment information (OS, Python version, GitSummarizer version)

## License

By contributing to GitSummarizer, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).