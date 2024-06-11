# Test Driven Development

Test-driven development (aka **TDD**) is a software development process that relies on the repetition of a very short development cycle: red-green-refactor. The idea of this process is to turn a requirement into one or a couple of specific test cases, run those tests to make sure they are red, then implementing the code to turn those tests green. A third step is to refactor the code while keeping the tests green.

![](https://res.cloudinary.com/wagon/image/upload/v1560715040/tdd_y0eq2v.png)

The testing pattern encouraged is a four-phase one and well described in this [blog article by Thoughtbot](https://robots.thoughtbot.com/four-phase-test)

## 0️⃣ Our challenge: Longest Word

Let's practice TDD with a simple game that we will use until the end of the day. We will implement "The Longest Word", a game where given a list of nine letters, you have to find the longest possible English word formed by those letters.

Example:

```
Grid: OQUWRBAZE
Longest word: BAROQUE
```

The word [`baroque`](https://en.wiktionary.org/wiki/baroque) is valid as it exists in the English dictionary (even though its origin is French 🇫🇷 😋)

Note that the word [`bower`](https://en.wiktionary.org/wiki/bower) is also valid. The goal here is **not** to write code which finds the longest word, but to analyze a human player attempt and judge if this word is valid or not against the given grid!

We need to **break down** the problem in tiny pieces...

First, let's decide on the right level of **modelling** against the Object-Oriented paradigm.
We want to create a `Game` class in `game.py` that has the following blueprint:

```python
class Game:
    def __init__(self) -> list:
        """Attribute a random grid to size 9"""
        self.grid = None # TODO
        pass

    def is_valid(self, word: str) -> bool:
        """Return True if and only if the word is valid, given the Game's grid"""
        pass # TODO
```

So we as to play with it as follow

```python
game = Game()
print(game.grid) # --> OQUWRBAZE
my_word = "BAROQUE"
game.is_valid(my_word) # --> True
```

In the TDD paradigm, one question we always ask is:

> How can I test my code above?

Asking this question means you need to think about your code like a black box. It will take some parameters in entry and you will observe the output, comparing them to an expected result.


## Test n°1: Creating a valid Game board.

### Starting the project

Now that we have a better idea of the object we want to build, we can start writing a test. First of all, let's create a new Python project using poetry:

```bash
cd ~/code/<user.github_nickname>
poetry new longest-word && cd $_
poetry add pytest pylint

touch longest_word/game.py
touch tests/test_game.py

code .
```

- copy your `game.py` skeleton inside
- setup VScode Python interpreter path to that created by poetry (`poetry env info --path` to see where it is)

### Testing Game().__init__

❓ **Try to write your first test**. Follow the 4 steps principles (some can be empty):

```python
# tests/test_game.py
class TestGame:
    def test_game_initialization(self):
            # setup
            # exercise
            # verify
            # teardown
```

<details>
  <summary markdown='span'>🎁  Solution</summary>

```python
# tests/test_game.py
from longest_word.game import Game
import string

class TestGame:
    def test_game_initialization(self):
            # setup
            new_game = Game()

            # exercise
            grid = new_game.grid

            # verify
            assert isinstance(grid, list)
            assert len(grid) == 9
            for letter in grid:
                assert letter in string.ascii_uppercase

```

</details>


❓ Now it's time to run it first to make sure those tests are **failing**:

```bash
poetry run pytest
```

What next? Now you should **read the error message**, and try to **fix** it, and only this one (don't anticipate). Let's do the first one together:
<details>
  <summary markdown='span'>👀 Error message </summary>

```bash
============================== test session starts ===============================
platform linux -- Python 3.8.14, pytest-7.2.0, pluggy-1.0.0 -- /home/brunolajoie/.cache/pypoetry/virtualenvs/longest-word-IGw-ZBuq-py3.8/bin/python
cachedir: .pytest_cache
rootdir: /home/brunolajoie/code/brunolajoie/longest-word, configfile: pyproject.toml
collected 1 item

tests/test_game.py::TestGame::test_game_initialization FAILED              [100%]

==================================== FAILURES ====================================
_______________________ TestGame.test_game_initialization ________________________

self = <tests.test_game.TestGame object at 0x7f0c169e4af0>

    def test_game_initialization(self):
        new_game = Game()
        grid = new_game.grid
>       assert isinstance(grid, list)
E       AssertionError: assert <class 'NoneType'> == list
E        +  where <class 'NoneType'> = type(None)

tests/test_game.py:8: AssertionError
============================ short test summary info =============================
FAILED tests/test_game.py::TestGame::test_game_initialization - AssertionError: assert <class 'NoneType'> == list
=============================== 1 failed in 0.03s ================================
```

</details>


OK so the error message is `AssertionError: assert <class 'NoneType'> == list`

❓ **Try to fix this test**...and remember, you don't have to pass the test immediately! As soon as you have a new error message, it's already a PROGRESS 🎉🎉 !!!

<img src="https://res.cloudinary.com/wagon/image/upload/v1560715000/new-error_pvqomj.jpg" width=500>

💡 You can use you can use `pytest --pdb` to jump into the debugger on test failure.

<details><summary markdown='span'>🎁 Solution
</summary>

One possible implementation is:

```python
# game.py

import string
import random

class Game:
    def __init__(self):
        self.grid = []
        for _ in range(9):
            self.grid.append(random.choice(string.ascii_uppercase))
```

</details>

<br>

## Test n°2: Checking the validity of a word

Let's move to the second method of our `Game` class, using the same feedback loop

- carefully write a unit test
- run the test
- get an error message
- figure out how to fix only this
- run the test again
- move to a new error message!


❓ **It's your turn to implement a test for this new `is_valid(self, word)` method**!

<details><summary markdown='span'>🎁 A possible solution
</summary>

A possible implementation of the test would be:

```python
# tests/test_game.py

# [...]

    def test_empty_word_is_invalid(self):
        # setup
        new_game = Game()
        # verify
        assert new_game.is_valid('') is False


    def test_is_valid(self):
        # setup
        new_game = Game()
        test_grid = 'KWEUEAKRZ'
        test_word = 'EUREKA'
        # exercice
        new_game.grid = list(test_grid) # Force the grid to a test case
        # verify
        assert new_game.is_valid(test_word) is True
        # teardown
        assert new_game.grid == list(test_grid) # Make sure the grid remained untouched

    def test_is_invalid(self):
        # setup
        new_game = Game()
        test_grid = 'KWEUEAKRZ'
        test_word = 'SANDWICH'
        # exerice
        new_game.grid = list(test_grid) # Force the grid to a test case
        # verify
        assert new_game.is_valid(test_word) is False
        # teardown
        assert new_game.grid == list(test_grid) # Make sure the grid remained untouched

```
</details>

<br>


❓ **Now, update the `game.py` implementation to make the tests pass**!

<details><summary markdown='span'>🎁 A possible solution
</summary>

A possible implementation is:

```python
# game.py

# [...]

    def is_valid(self, word):
        if not word:
            return False
        letters = self.grid.copy() # Consume letters from the grid
        for letter in word:
            if letter in letters:
                letters.remove(letter)
            else:
                return False
        return True
```

</details>

<br>


## Style

Make sure to make `pylint` happy:

```bash
poetry run pylint longest_word/game.py
```

- `pylint` is the standard 'linter' for python, it checks the code without running.
- Its suggestions are mostly good practices - you can try to follow the [documentation](https://pylint.pycqa.org/en/latest/) but most of the suggestions are pretty intuitive.

You can disable those rules which you don't think should apply here, by adding the following lines at the top of each file for example:

```python
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
```
