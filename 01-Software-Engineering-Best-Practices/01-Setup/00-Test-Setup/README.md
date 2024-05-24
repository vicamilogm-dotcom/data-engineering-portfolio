# 🎯 Goals

This first challenge will test if your setup is correct, and help you understand how the bootcamp works.

- We'll have a look at the data-engineering-challenges repository structure
- A cheatsheet that can help you throughout your bootcamp journey
- Understand how VSCode chooses the correct poetry virtual environment for each challenge
- We'll complete a dummy challenge to see how your repository integrates with Kitt!

Open two separate vscode windows (you can use `code path/to/challenge_directory` in your VM terminal to open a new VSCode window):
- One at this challenge-level folder (you should already be here)
- Another one at `data-engineering-challenges` root level

<br>

# 1️⃣ Understand your repository structure

❓ Take a look at your `data-engineering-challenges` structure with `tree -a -L 2` and take some time to understand it.

```bash
.
├── 01-Software-Engineering-Best-Practices # Module level
│   ├── 01-Setup                           # Unit level
│   │   ├── 00-Test-Setup                  # Challenge level
            ├── app
            │   ├── __init__.py
            │   └── main.py                # YOUR CODE HERE
            └── tests
            │   ├── __init__.py
            │   └── test_your_function.py  # OUR TEST CODE HERE
            ├── .venv                      # your virtual-env for this challenge, created automatically by poetry
            ├── .envrc                     # direnv call to activate your poetry venv as soon as you cd into the foler
            ├── makefile                   # Contains `make test` and `make install` commands for you
            ├── poetry.lock                # Created by you when running `make install`
            ├── pyproject.toml             # We already wrote this for you so that poetry install will create all you need
            ├── README.md                  # Kitt-displayed readme
...
...
...
├── .dockerignore
├── .gitignore          # globally ignore file pattern (.env, etc...)
├── CHEATSHEET.md       # Some tips for you
├── Makefile            # Gobal bootcamp commands (e.g. run all `make install` for each challenges, run all tests etc...)
├── make.inc            # This file is accessed by every challenges-level makefile (for refactoring purposes)
├── README.md
├── common              # Le Wagon shared logic between all challenges (used for test purposes)
├── direnvrc-template   # You can remove it once you've added it to your ~/.direnvrc
└── yapf                # Formatting rules for you to auto-format your code
```

<br>

# 2️⃣ CHEATSHEET.md

👉 Read the `CHEATSHEET.md`  we created for you to help you throughout the camp! At least, focus on section 1️⃣ to 3️⃣ now

> 💡 You can use VScode to render HTML properly by clicking on the top-right icon, or "Command Palette (Cmd-Shift-P)" --> "Open Preview to the side".

<br>

# 3️⃣ How does VSCode know what poetry virtual environment to use?

We are using poetry to manage the python virtual environments and package dependencies for each individual challenge in the bootcamp. If you want to have a look yourself, they are contained in the `.venv/` directory in the root of each challenge folder!

For VSCode to recognise the virtual environment for a challenge, you **must** open VSCode at the root for a challenge directory. For this **Test Setup** challenge it would be:

```bash
code ~/code/<user.github_nickname>/data-engineering-solutions/01-Software-Engineering-Best-Practices/01-Setup/00-Test-Setup
```

With each challenge having a separate virtual environment we don't have to worry about managing python package dependencies so that they work with ALL challenges 😉

This VSCode *hook* was set during your VM setup by modifying the following line in your **VSCode: Remote Settings (JSON)** to the following:

```bash
"python.defaultInterpreterPath": ".venv/bin/python",
```

💡 If you run into any issues with `python interpreter not found` when working on python files, make sure VSCode has been opened to the challenge root.

<br>

# 4️⃣ Try to pass the tests of this dummy challenge

❓ Open your VScode at 00-Test-Setup level, then try to fill your code in `app.main`

For most challenges there will be an included `Makefile` that has an associated function to test your code: `make test`

Have a look at the `tests/` folder:
- There are some optional tests that will NOT be checked by running `make test` (which does a `pytest -m "not optional"` under the hood: have a look in `make.inc` to see how it's working!)
- Optional tests can still be tested by running pytest manually (e.g `pytest tests/test_our_function.py`)

To test your code run:
```bash
make test
```

It should PASS (hopefully 😅) and you should see a new `test_output.txt` file created. This `test_output.txt` file is used by Kitt to track your progress during the day. But for that to happen, you need to push your code to github first!

```bash
git add --all
git commit -m "010100 done"
git push origin main
```

👉 Go check on your progress status on Kitt's challenge page top right corner! It should be green.

Don't forget to follow the progress of your buddy of the day and help him out if needs be!

<br>
