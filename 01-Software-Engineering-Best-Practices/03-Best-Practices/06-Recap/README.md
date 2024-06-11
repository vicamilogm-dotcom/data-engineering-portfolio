# 🎯 Workflow dependency & pre-commit hooks

Through this unit we have explored how automated Continuous Integration and Continuous Deployment actions can increase quality and consistency in our code. CI/CD actions catch errors early, making the development process more efficient and prevents broken or defective code being deployed to production.

But waiting and until you open a pull request to merge your feature back into the parent branch can result in a long feedback loop for you as the developer.

In this recap we'll look at pre-commit hooks and how they can shorten the feedback loop for development, and enforce linting and styling for a project when working collaboratively!

<br>

# 0️⃣ Setup

Create a new python project using poetry:

```bash
cd ~/code/<user.github_nickname>
poetry new pre-commit-test && cd $_
```

Let's initialise the project with git and make an initial commit.

```bash
# Initialize git repository
git init

# Create new Github repository
# and follow wizard to push current directory to Github
# Make sure it's a public repository!
gh repo create

# Add project skeleton files to staging and commit
git add .
git commit -m "inital commit"

# Push project to Github
git push origin main
```

<br>

# 1️⃣ Workflow dependency

With an empty project initialised and ready, lets start with a Github action for Continuous Integration that will:
- Format our python code with [black](https://github.com/psf/black)
- Lint our python code with [ruff](https://docs.astral.sh/ruff/)
- Typecheck out python functions with [mypy](https://mypy-lang.org/)

Create a new branch and add the below to `.github/workflows/python-checks.yaml`.

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

Lets go through this Github Action and what it's doing.

- **Black**: Auto-formatter that makes code adhere to a consistent style. Useful for eliminating debates about code style in a project.

- **Ruff**: Linting tool that detects potential errors, bad practices, and style issues. Helps improve code readability and maintainability.

- **mypy**: Static type checker that catches type errors before runtime. Enhances code quality and can serve as documentation.

Create a new python file in `pre_commit_test/test_ci.py` and add the following code block:

```python
# test_ci.py

def greet(name: int) -> str:
    print("Hello, " + name + "!")
    return 42


greet("world")
```

Commit the changes, push to Github and open a pull request and see what happens!

<details>
<summary markdown='span'>💡 What should have happened </summary>
Oh no! Our action has failed on mypy's type checking action.

But we had to open a pull request to get that feedback - let's look at pre-commit hooks and how they can shorten the development cycle!

Although we failed the CI actions on this attempt, let's see how we can improve our development cycle. Leave the pull request open for now and somewhere easily accessible, we will be coming back to it 😉
</details>

<br>

# 2️⃣ Pre-commit

[Pre-commit](https://pre-commit.com/) allows you to run checks locally before each commit, catching issues earlier in the development cycle.

**Why Use It**:
  1. Faster Feedback: Errors are caught on your local machine not after pushing to the repository.
  2. Consistency: Ensures every developer runs the same checks making codebase more uniform.
  3. Saves CI Time: By catching issues locally it reduces the load on the CI pipeline making it faster for everyone and also reduces cost of CI actions!

Using both pre-commit hooks and CI checks provides a more robust setup. Pre-commit catches issues earlier while CI serves as the final gatekeeper before code gets merged.

On the same branch create a file in the project root called `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    # Ruff version.
    rev: 'v0.0.265'
    hooks:
      - id: ruff
        args: ["--ignore=E501,F821"]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0
    hooks:
      - id: check-json
      - id: check-merge-conflict
      - id: check-xml
      - id: check-yaml
      - id: debug-statements
      - id: detect-private-key
      - id: pretty-format-json
        args: ['--autofix', '--indent=2', '--no-sort-keys']
      - id: sort-simple-yaml
      - id: trailing-whitespace
      - id: end-of-file-fixer

  - repo: https://github.com/psf/black
    rev: '23.3.0'
    hooks:
      - id: black
        args: ['--line-length=88']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: 'v1.10.0'
    hooks:
      - id: mypy

```

This is the one used at Le Wagon - with the exception of the `mypy` hook.

To use it install pre-commit globally with:

```bash
pipx install precommit
```

and then we can install all the hooks and run it against all of our files.

```bash
# Install relevant packages and hooks
pre-commit install --install-hooks
```

Lets change `test_ci.py` by putting `greet(world)` inside an `if __name__ == "__main__"` block.

```python
# test_ci.py

def greet(name: int) -> str:
    print("Hello, " + name + "!")
    return 42

if __name__ == "__main__":
    greet("world")
```

Add the file to staging with `git add pre_commit_test/test_ci.py` then try to commit!

What happens when you run another `git status`?

<details>
<summary markdown='span'>💡 What just happened?!</summary>
`pre-commit` should have failed the mypi check and returned something similar to the image below:

<img src="https://wagon-public-assets.s3.eu-west-3.amazonaws.com/mtl6ce5fa5iqzgo5se9mm4vj3pa1" width=600>

If you run `git status` you'll see that `test_ci.py` was never committed - so you can fix the file and commit it again!
</details>

Notice how `pre-commit` has only run the relevant hooks for python files and skipped hooks for JSON, YAML, and XML. Pre-commit checks the files that are in **the current commit** and runs the relevant hooks.

<br>

# 3️⃣ Code correction and push to Github

Now that we have a quicker feedback loop using pre-commit hooks, let's fix up our code and push to the existing branch.
- Make the appropriate changes to `test_ci.py`
- Add the file to staging and commit
- Once pre-commit has passed all its checks, push your changes to github
- Navigate to your open pull request and have a look at the CI actions. They should all be passing!

<br>

# 🏁 Resources and further reading

Have a look at all the supported pre-commit hooks [here](https://pre-commit.com/hooks.html). Hooks exist for a wide range of different languages and file types!

[Ruff linting rules](https://docs.astral.sh/ruff/rules/) to customise your linting.

If you want to run your pre-commit hooks against all current files:

```bash
pre-commit run --all-files
```

<br>
