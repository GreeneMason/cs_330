# Contributing Guide

This guide outlines how to contribute to the UFC Fight Analysis project.

## Setting Up Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cs_330.git
   ```
3. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt
   pip install -e .
   ```

## Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Maximum line length: 88 characters
- Use docstrings for all functions and classes

### Documentation Style
- Use Markdown for documentation
- Include code examples
- Keep documentation up to date with code changes

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Reference issues when applicable

## Development Process

### 1. Creating New Features

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Write your code following these guidelines:
   - Write tests first (TDD approach)
   - Include docstrings
   - Add type hints
   - Follow code style guidelines

3. Add unit tests in `tests/` directory

4. Update documentation as needed

### 2. Testing

1. Run unit tests:
   ```bash
   python -m pytest tests/
   ```

2. Check code coverage:
   ```bash
   python -m pytest --cov=src tests/
   ```

3. Run style checks:
   ```bash
   flake8 src tests
   ```

### 3. Submitting Changes

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request from your fork to the main repository

## Project Structure

```
cs_330/
├── src/
│   └── ufc_analysis/       # Main package code
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── scripts/                # Utility scripts
└── notebooks/             # Jupyter notebooks
```

### Key Files and Directories

- `src/ufc_analysis/`: Main package code
- `tests/`: Unit tests
- `docs/`: Documentation
- `scripts/`: Utility scripts
- `notebooks/`: Example notebooks

## Documentation

### Adding New Documentation

1. Create new .md files in `docs/` directory
2. Update existing docs as needed
3. Include code examples
4. Add to table of contents

### Building Documentation

1. Install documentation tools:
   ```bash
   pip install mkdocs
   ```

2. Build docs:
   ```bash
   mkdocs build
   ```

3. Preview locally:
   ```bash
   mkdocs serve
   ```

## Issue Guidelines

### Reporting Bugs

Include:
1. Description of the bug
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. System information
6. Screenshots if applicable

### Feature Requests

Include:
1. Clear description of the feature
2. Use case(s)
3. Proposed implementation if possible
4. Any relevant examples

## Code Review Process

1. All code must be reviewed
2. Address all review comments
3. Tests must pass
4. Documentation must be updated
5. Code style must be consistent