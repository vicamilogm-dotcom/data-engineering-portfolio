# 🎯 Goal

Remember our CLI's `connect` function we build on setup day? It works great when the VM is running, but not so well if it is not running: it tries to connect. So instead lets create a check before we attempt to ssh in!

Our final goal will be to setup continuous deployment of our CLI so that when we push an update to Github, it will also be automatically deployed on Gemfury!

<br>

# 1️⃣ Creating the CI

Lets return to our CLI so far:

```bash
cd ~/code/<user.github_nickname>/<user.github_nickname>-de-toolkit
```

Before we get started, let's initialize the repo, create a new branch and bump the minor version number:

Careful when using a `.env` file - don't forget to git ignore it!

```bash
echo ".env" > .gitignore
git init
git add .
git commit -m "cli 0.0.1 code"

gh repo create --private --source=.
git push origin main

git checkout -b connect-status-check

poetry version minor
```

We need to call the VM with `gcloud compute instances describe`, so let's write a function calling that to spread our code. Let's create a new file to store these extra utilities that won't be directly accessible by the CLI!

```bash
touch <user.github_nickname>-de-toolkit/vm_utils.py
```

<br>

# 2️⃣ Testing functions

Let's test our function (ideally we would test all parts of our CLI but let's stick to just this new helper function). The obvious difficulty is that currently the function relies on whether our vm is running or not. This means that, within our test file, we need to create a function to create fake output.

The first step is to create a test file!

```bash
touch tests/test_vm_utils.py
```

Next we want to create files which show the two states

```bash
gcloud compute instances describe --zone=europe-west1-b <user.github_nickname> > tests/<state>.txt
```

Now inside `tests/test_vm_utils.py` create a helper function which would return the same as calling our function!

```bash
import pathlib
from <user.github_nickname>_de_toolkit.vm_utils import check_running

def fake_input(state):
    path = pathlib.Path(__file__).resolve().parent.joinpath(f'{state}.txt')
    with open(path, 'r') as file:
        data = file.read().replace('\n', '')
    return data

def test_state_check():
    assert check_running(fake_input("stopped")) is False
    assert check_running(fake_input("running")) is True
```

We can now include our CI implementation from the previous exercise!

```bash
cp -r ../longest-words/.github .
```

Now, if we push our work and create a pull request, you should see the CI running. One of the best parts about CI is how easy everything is. Once we have a workflow, it is easy to use on many repos.

But we are not quite there yet. Your CI should now fail, so try and debug it by reading the action output!

<details>
<summary markdown='span'>Solution</summary>

```bash
poetry add -G dev pytest
```
</details>

Now when you push again, you should see green (ideally our CI would fully check our package, but not today!)

# 3️⃣ Implementing CD

If you have set a Gemfury password, you will have to add another secret to Github and set the relevant environment variable in `.fury-cd.yml`

```bash
cp .github/workflows/.python-ci.yml .github/workflows/.fury-cd.yml

gh secret set GEMFURY_TOKEN --body "$GEMFURY_TOKEN"

pipx uninstall <user.github_nickname>-de-toolkit && pipx install $_ --pip-args='--extra-index-url https://<deploy token>@repo.fury.io/<user.github_nickname>/'
```

<br>

# 🏁 Finishing up

Now you should have CI/CD on your Gemfury package!

As you can see, there is a lot of boiler plate in Github Actions, so if you have written one Github Action, you've written most of your next one!

<br>
