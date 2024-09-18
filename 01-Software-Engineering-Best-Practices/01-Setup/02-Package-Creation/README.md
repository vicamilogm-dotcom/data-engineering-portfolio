# 🎯 Goals

The goal of this exercise is to:
- Create a command line tool to start and stop your VM using python and shell scripts.
- Use `poetry` to create the python package and manage dependencies.
- Publish the package so that your package is available to install anywhere.
    - Firstly to the public **pypi** repository
    - Secondly to a private package repository: **Gemfury**
- Optional: install the package locally if you have a local developer environment.

<br>

# 1️⃣ Lets start by creating a new poetry package!

We'll start with creating the package outside of the `data-engineering-challenges` folder so it is entirely separate from the challenges and can have its own github repository.

<details>
<summary markdown='span'>If you need a quick refresher on python packages</summary>
https://docs.python.org/3/tutorial/modules.html
</details>


```bash
poetry new ~/code/<user.github_nickname>/<user.lower_github_nickname>-de-toolkit && cd $_
```

☝️ Here we are using poetry to create a new package. Another useful terminal command is `$_`, which is the most recent parameter. In this case, the folder we've just created with `poetry new` lets us `cd` right into it.

Then, open this folder in your VS code Explorer, so that you see your package AND today's challenge in the same editor.
```bash
code -a . # open the folder in another workspace in the same VS code
```

At this point, we will have our `README.md`, a basic `pyproject.toml`, `<user.lower_github_nickname>_de_toolkit` package directory to populate, and a `tests/` folder if needed.

Your `pyproject.toml` should look like this:

```toml
[toml.poetry]
name = "<user.lower_github_nickname>-de-toolkit"
version = "0.1.0"
description = ""
authors = ["Your Name <example@email.com>"]
readme = "README.md"
packages = [{include = "<user.lower_github_nickname>_de_toolkit"}]

[tool.poetry.dependencies]
python = "^3.8"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

❗ Make sure that your `pyproject.toml` includes the `packages = [{...}]` line. This tells poetry that you want to install the package `<user.lower_github_nickname>_de_toolkit` as a python package. We're building a command line tool so we definitely want our package to be installed!

<details>
<summary markdown='span'>💡 When wouldn't I want to install my own package?</summary>
If you were only using poetry purely as an external python package depency manager and didn't want to install your python project locally. An example would be in a DBT or Airflow project, but we can save that idea for later!
</details>

Lets add [click](https://click.palletsprojects.com/en/8.1.x/) to our project to help develop our CLI:
```bash
poetry add click
```

❓ Now, **create** a main file to create our entry point and populate it with the code below:

```bash
touch <user.lower_github_nickname>_de_toolkit/main.py
```

```python
import click

@click.group()
def cli():
    pass


if __name__ == '__main__':
    cli()
```

Here, we are setting up the skeleton of a CLI using [group](https://click.palletsprojects.com/en/8.1.x/commands/) with the `@click.group()` decorator. This is where we will add other commands to flesh it out.

Now, if you run `poetry run python <user.lower_github_nickname>_de_toolkit/main.py`, you should see some empty documentation appear. One of the great features of click is how it uses doc strings in order to generate readable CLI feedback!

💡 **Let's alias** this long command. Add a line to our `pyproject.toml` to create alias `deng`:

```toml
[tool.poetry.scripts]
deng = '<user.lower_github_nickname>_de_toolkit.main:cli'
```
Now, we can run our CLI with `poetry run deng` instead 👌

<br>

# 2️⃣ Core logic
🎯 The goal of this package is to help you start and stop your VM at the start and end of every session in one line of code!

At the end, we'll want to use it as follows, from your local machine:

1️⃣ `deng start`: Start the vm (using `gcloud`)
2️⃣ `deng stop`: Stop the vm (using `gcloud`)
3️⃣ `deng connect` Connect directly to VScode inside your challenge folder!

❓ Create a new file `touch <user.lower_github_nickname>_de_toolkit/vm.py` to contain our vm commands. **Try to implement these** in the function shells below using the inbuilt [subprocess](https://docs.python.org/3/library/subprocess.html) module!

```python
import click
import subprocess

@click.command()
def start():
    """Start your vm"""
    # your code here

@click.command()
def stop():
    """Stop your vm"""
    # your code here

@click.command()
def connect():
    """Connect to your vm in vscode inside your ~/code/<user.lower_github_nickname>/folder """
    # your code here
```

<details>
<summary markdown='span'>💡 Hints: gcloud commands</summary>

```bash
# start vm
gcloud compute instances start --zone=<vm zone> <vm name>
# stop vm
gcloud compute instances stop --zone=<vm zone> <vm name>
# code into vm
code --folder-uri vscode-remote://ssh-remote+username@<vm ip>/<path inside vm>
# eg. code --folder-uri vscode-remote://ssh-remote+brunolajoie@35.240.107.210/home/brunolajoie/
```
</details>

❓ Add these three commands to our `cli` group using `cli.add_command(<your command>)` in main.py

Running `poetry run deng` should now list you these 3 options

```bash
$ poetry run deng
Usage: deng [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  connect  Connect to your vm in vscode inside your...
  start    Start your vm
  stop     Stop your vm
```

<br>

# 3️⃣ Publishing your package

## 3.1. Publish to pypi
<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D1/pypi-logo.png" width=100>

🎯 Now we have our CLI. We want to publish it to make it available from any computer with python without needing the `.py` files.

The python package index (known as pypi) is where packages that you can install directly with `pip` or in our case `poetry`, so that your package can become available on a new setup without having to re-clone the repository.

❓ Signup to [pypi](https://pypi.org/account/register/). Then create an api token from [account settings](https://pypi.org/manage/account/) and make sure it has the scope entire account so that it can generate new projects!

**Then create a `.env` at the root of your package** containing the following to store your token:

```bash
PYPI_USERNAME=__token__
PYPI_TOKEN=<Your Token>
```

This is the perfect place to use **direnv**. Let's create a .envrc to load our .env file:

```bash
echo "dotenv" > .envrc
```

Now, you can verify that your token is available as an environment variable with:
```bash
echo $PYPI_TOKEN
```

If it doesn't work, you may need to `direnv allow` once for all for this folder.

**Lets use poetry to quickly build and publish our package!**


```bash
poetry publish --build --username $PYPI_USERNAME --password $PYPI_TOKEN
```
(no worries, `.env` are not going to be part of the built archive, so won't be pushed to pypy by poetry)

Now go to [your package](https://pypi.org/project/<user.github_nickname>-de-toolkit/) directly on pypi. You should now be able to install this package from any machine. With pypi, the package is publicly available which is not an issue in our case but be careful in cases when you do not want to share the code with the rest of the world. The solution is using private package repositories instead!

👉 Go to this [page](https://pypi.org/manage/project/<user.github_nickname>-de-toolkit/settings/) to delete your package.

<br>

## 3.2. Publish to private repository instead with Gemfury


There are plenty of solutions for private repositories even hosting them [yourself](https://pypi.org/project/pypiserver/)! For ease, we will use [gemfury](https://gemfury.com/), you can login with Github and then go to this [page](https://manage.fury.io/manage/<user.github_nickname>/tokens/full) to get a full access token.

❓ Add the token to the `.env` file:

```bash
GEMFURY_TOKEN=<your_token>
GEMFURY_PASSWORD=<your_gemfury_password>
```

**Now to publish to your private repository you can follow this workflow!**

```bash
# Configure poetry to read your Gemfury repositories:
poetry config repositories.fury https://pypi.fury.io/<user.lower_github_nickname>/

poetry config http-basic.fury $GEMFURY_TOKEN $GEMFURY_PASSWORD

# Push the package and any future build versions with:
poetry publish --build --repository fury
```

Then, to use your packages from your private repo in another package, all you need to do is:

```bash
poetry source add fury https://pypi.fury.io/<user.lower_github_nickname>/
poetry add --source fury <user.lower_github_nickname>_de_toolkit
```

You can see that this workflow is slightly more long-winded than publishing to pypi, but it is something you only need to do at the start or end of projects and can add a lot of flexibility to how you distribute python packages around your team.

<br>

# 4️⃣ Optional: Install your private package on your LOCAL machine

>🚨 **ONLY DO THIS SECTION IF PYTHON IS INSTALLED ON YOUR LOCAL HOST MACHINE, OTHERWISE PLEASE SKIP.**

- Assumes you have GCP authentication on your **local** computer
- You do not need to have python locally installed on your machine for this bootcamp
- You do not have time to configure your local machine today

If you have python and pip installed locally, there are two options for installing your package locally:

**Option 1**: Create a `~/.pip/pip.conf` with these credentials below:
```bash
[global]
trusted-host = pypi.fury.io
extra-index-url = https://<YOUR_GEMFURY_TOKEN_HERE>@repo.fury.io/<user.lower_github_nickname>/
```
pip will now use Gemfury instead of pipy whenever the package name exists on the former:
```bash
pip install <user.github_nickname>-de-toolkit
```

**Option 2**: Just give the gemfury as a one-off, with pip or pipx:

```bash
# Inside your local python virtualenv
pip install <user.lower_github_nickname>-de-toolkit --index-url https://<your-token>@repo.fury.io/<gemfury-username>/
# OR globally with pipx
pipx install <user.lower_github_nickname>-de-toolkit --pip-args='--extra-index-url https://<YOUR_GEMFURY_TOKEN_HERE>@repo.fury.io/<user.lower_github_nickname>/'
```

If install was successful, try to run the following commands on your local computer to test it out:

👉 Try to `deng connect` !
👉 `deng start` at the start of every session
👉 `deng stop` at the end of every session

<br>
