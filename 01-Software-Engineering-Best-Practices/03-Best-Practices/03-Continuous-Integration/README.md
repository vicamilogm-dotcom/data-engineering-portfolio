# Continuous Integration

Having tests on a repository gives you a tremendous advantage: you can set up [**Continuous Integration**](https://en.wikipedia.org/wiki/Continuous_integration). The _Best Practices_ section of this Wikipedia article is worth a read.

The goal of this exercise is to link our version control software with a build automation tool. The idea is that you want the build automation to run every time a commit reaches the version control, in any branch, a build is triggered to give feedback to the developers as soon as possible if this commit is _green_ or _red_ (meaning the tests are passing / the build can complete).

## Tools

As for version control software, there are many tools available to achieve Continuous Integration:

- [Jenkins](https://jenkins.io/), the most popular on-premise CI software (you need to install it)
- [Github Actions](https://github.com/features/actions), the tool from Github to set up automated workflows and CI/CD
- [Travis](https://travis-ci.com/), the most popular **cloud** CI service
- [Many others](https://en.wikipedia.org/wiki/Comparison_of_continuous_integration_software)

To keep this exercise simple, we will use Github Actions, as it integrates perfectly with GitHub (and you'll see that's important) without any configuration effort on the developer's side. Plus, it's **free** for public GitHub repositories!

## Service installation

We will deploy the repository you created in the previous exercise:

```bash
cd ~/code/<user.github_nickname>/longest-word

git init
git add .
git commit -m "Game development with TDD"

gh repo create --public --source=.

git push origin master

code . # Let's work directly on your package for this challenge
```


## Worfklow CI

You now need to write a CI configuration file. Those tools are _generic_, they can build programs in many languages, with many frameworks. We need to be specific and explain to Github Actions that our project is a Python 3 one, that we use `poetry` to handle external dependencies and that we use `pytest` to run tests.

In order to do that, Github reads the `.python-ci.yml` file located in the folder  `.github/workflows` :

```bash
mkdir -p .github/workflows
touch .github/workflows/.python-ci.yml
```

```yml
# .python-ci.yml

name: basic CI
on:
  push:
    branches: [ master, main ]
  pull_request:
    branches: [ master, main ]
jobs:
  build-and-run-pytest:
    runs-on: ubuntu-latest
    steps:
    # First step (unnamed here) is to checkout to the branch that triggered the event
    - uses: actions/checkout@v3
    # Second step: install python 3.8
    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: "3.8"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        poetry install
    - name: Run tests
      run: |
        poetry run pytest
```

Save this file in VS Code, and perform a commit:

```bash
git add .github
git commit -m "Configure Github Actions CI to run pytest"
```

Awesome! Before we actually push, go to this page:

[github.com/<user.github_nickname>/longest-word/commits/master](https://github.com/<user.github_nickname>/longest-word/commits/master)

You should have one commit. Now go back to the terminal:

```bash
git push origin master
```

When the push is done, go back to the page, and **reload** it. You should see the commit get a yellow circle, and then a green tick! This is the integration between GitHub and Github Actions. It will run everytime you push commits to GitHub.

You can view the actions in browser or through the cli with `gh run watch`!

📚 Take 10min to read this [Github Docs](https://docs.github.com/en/actions/using-workflows/about-workflows) to better understand how workflows work

## Continuous Integration & Pull Request

Let's enhance our Game with a refined validation. Right now, you can win with the following scenario:

```
Grid: KWIENFUQW
My proposition: FEUN
```

```python
new_game = Game()
new_game.grid = list('KWIENFUQW')
new_game.is_valid('FEUN')
# => true
```

Sure, it is syntatically valid (each letter of `FEUN` can be found in the grid), but this is not a valid English word from the dictionary!

Let's work on that in a new feature branch:

```bash
git checkout -b dictionary-api
```

Following the TDD paradigm, we need to add a test:

```python
# tests/test_game.py
# [...]
    def test_unknown_word_is_invalid(self):
        """A word that is not in the english directory should no be valid"""
        new_game = Game()
        new_game.grid = list('KWIENFUQW') # Force the grid to a test case:
        assert new_game.is_valid('FEUN') is False
```

Let's commit this right now:

```bash
git add test_game.py
git commit -m "TDD: Check that attempt exists in the English dictionary"
git push origin dictionary-api
```

Now let's open a Pull Request on GitHub for this branch.
- 💡 To make a pull request quickly you can use `gh pr create` or to directly open the correct page use `gh pr create --web`!
- You might find it a bit early but that's something which is actually encouraged by the [GitHub flow](http://scottchacon.com/2011/08/31/github-flow.html): If you are stuck in the progress of your feature or branch and need help or advice, or if you are a developer and need a designer to review your work (or vice versa), or even if you have little or no code but some screenshot comps or general ideas, you open a pull request.
- At Le Wagon, developers open Pull Request early on for their feature branches to show teammates what they are doing and solicit feedback early. No need to wait to be code-complete to open the Pull Request! Here is a screenshot of our main application, using the `[WIP]` prefix in the pull request titles to showcase the fact that the branch is not ready yet to be merged:

<img src="https://res.cloudinary.com/wagon/image/upload/v1560714921/kitt-wip-prs_obp6e7.png" width=600>

Back to our Pull Request. If you scroll a bit below the PR description and the list of commits, you will see the Github Actions shine:

<img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/github_actions_picture.png?raw=true" width="700">

The benefit is really important. You have a direct feedback, right in GitHub, about the build status of your branch. Of course here we actually _want_ to have a red branch as we added a test but did not implement the behavior yet. Still, you can imagine that someone pushing some code and forgetting to run the tests locally on their machine will be warned directly on GitHub that they broke the build.

---

❓ **Let's go back to the implementation of our feature: Try to pass the following test**

```python
poetry run pytest -k test_unknown_word_is_invalid
# 💡 See how we just run *one* test and not the whole suite?
```
Using Le Wagon's homemade simple [Dictionary API](https://dictionary.lewagon.com/)
  - [https://dictionary.lewagon.com/tomato](https://dictionary.lewagon.com/tomato)
  - [https://dictionary.lewagon.com/notomato](https://dictionary.lewagon.com/notomato)

💡 You can `poetry add requests` to make [HTTP requests](http://docs.python-requests.org/en/master/) to this API in Python

<details><summary markdown='span'>🎁 View solution
</summary>

We can implement a private `__check_dictionary` method to run an API call.

```python
# game.py
# [...]
import requests

class Game:
    # [...]

    def is_valid(self, word):
        # [...]

        return self.__check_dictionary(word)


    @staticmethod
    def __check_dictionary(word):
        response = requests.get(f"https://dictionary.lewagon.com/{word}")
        json_response = response.json()
        return json_response['found']
```

</details>

<br>

Don't forget to run the tests locally until you have 5 passing tests. When you are done, time to observe the effect on GitHub / Github Actions!

```bash
git add .
git commit -m "Feature complete: Dictionary check of attempt"
git push origin dictionary-api
```

Go back to your Pull Request page, you should see the icons turning from red crosses to yellow dots. It means that Github Actions is building the code against the latest commit. Wait a few seconds, and it should update the status. This is what you should see:

<img src="https://res.cloudinary.com/wagon/image/upload/v1560714701/github-travis-passing_vppc1l.png" width=500>

Awesome job 🎉! Invite your buddy as a repo collaborator to review the code in the Pull Request and **merge** it.

## 🏁 Conclusion

Adding tests to a repository and coupling GitHub with a service like Github Actions gives the developer peace of mind when adding code, checking for possible regressions, exercising the whole test suite for _every single_ commit!

Before pushing DevOps farther with the next exercise about Continuous Deployment, some final advices:

- Keep Pull Request diffs as short as possible. A good size is **less than 100 lines** in the diff (`Files changed` tab on the Pull Request)
- Keep Pull Request focused on a _single_ feature. Add at least a test for each pull request
- Before asking for a review, re-read your code in the `Files changed` tab. Seeing the code from this perspective (in a web browser under a diff format) will help you spot style issues, refactoring opportunities, etc. that you could not see directly in your text editor.
- Finally, your friends at GitHub wrote a great piece on [how to properly write](https://blog.github.com/2015-01-21-how-to-write-the-perfect-pull-request/) in a Pull Request (both for the reviewee and the reviewer).
