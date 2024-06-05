# Workflow dependency & pre commit

## Workflow dependency

Create a new repo and add this workflow

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8.14
      uses: actions/setup-python@v2
      with:
        python-version: '3.8.14'
    - name: Install Black
      run: pip install black
    - name: Apply Black formatting
      run: black .
    - name: Commit formatting changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add -A
        git commit -m "Apply Black formatting" || echo "No changes to commit"

  lint:
    needs: format
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8.14
      uses: actions/setup-python@v2
      with:
        python-version: '3.8.14'
    - name: Install Ruff
      run: pip install ruff
    - name: Run Ruff linting
      run: ruff .

  typecheck:
    needs: format
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8.14
      uses: actions/setup-python@v2
      with:
        python-version: '3.8.14'
    - name: Install mypy
      run: pip install mypy
    - name: Run type checks
      run: mypy .
```

Add this python file and checkout the results of the action

```python
# test_ci.py

def greet(name: int) -> str:
    print("Hello, " + name + "!")
    return 42

greet("world")
```

- **Why**: Automating these checks ensures code quality and consistency without manual intervention. It catches errors early, making the development process more efficient.

- **Black**: Auto-formatter that makes code adhere to a consistent style. Useful for eliminating debates about code style in a project.

- **Ruff**: Linting tool that detects potential errors, bad practices, and style issues. Helps improve code readability and maintainability.

- **mypy**: Static type checker that catches type errors before runtime. Enhances code quality and can serve as documentation.

## Precommit

Allows you to run checks locally before each commit, catching issues earlier in the development cycle.

**Why Use It**:

1. Faster Feedback: Errors are caught on your local machine, not after pushing to the repository.
2. Consistency: Ensures every developer runs the same checks, making codebase more uniform.
3. Saves CI Time: By catching issues locally, it reduces the load on the CI pipeline, making it faster for everyone.

Using both pre-commit hooks and CI checks provides a more robust setup. Pre-commit catches issues earlier, while CI serves as the final gatekeeper before code gets merged.

Setup a file in the root name `pre-commit-config.yaml`

```yaml
repos:
  - repo: 'https://github.com/charliermarsh/ruff-pre-commit'
    rev: v0.0.265
    hooks:
      - id: ruff
        args:
          - '--ignore=E501,F821'
  - repo: 'https://github.com/pre-commit/pre-commit-hooks'
    rev: v2.3.0
    hooks:
      - id: check-json
      - id: check-merge-conflict
      - id: check-xml
      - id: check-yaml
      - id: debug-statements
      - id: detect-private-key
      - id: pretty-format-json
        args:
          - '--autofix'
          - '--indent=2'
          - '--no-sort-keys'
      - id: sort-simple-yaml
      - id: trailing-whitespace
      - id: end-of-file-fixer
  - repo: 'https://github.com/psf/black'
    rev: 23.3.0
    hooks:
      - id: black
        args:
          - '--line-length=88'
```

This is the one used at lewagon

To use it install pre-commit `pipx install precommit` and then `pre-commit install --install-hooks`

Then checkout what happens when you commit!
