# API Requests

🎯 The goal of this exercise is to make some `GET` api calls via the python `requests` library

## Before you get started

If you did not setup the service to auto stop in the previous unit we recommend that you go back and do `010103-Linux-and-Bash` at some point throughout this first unit to make sure to minimize your vm costs!

## Introduction


We will be using the PokeApi to access information about pokemon. Here is the [documentation](https://pokeapi.co/docs/v2). We will begin with some basic calls and then move into functions which require multiple requests to get the proper information!

## Advice for writing api calls

1. Check the documentation and write out a call for lets say we wanted to look up a specific pokemon generation via an api call we would find out how to do there here: https://pokeapi.co/docs/v2#games-section

2. Next enter the call directly into the browser so for example look up generation 1 👇

```
https://pokeapi.co/api/v2/generation/1
```

For this to make it easier to interact with in the browser we recommend adding an extension for [firefox](https://addons.mozilla.org/en-GB/firefox/addon/jsonview/) or for [chrome](https://chrome.google.com/webstore/detail/json-viewer/gbmdgpbipfallnflgajpaliibnhdgobh) (if you use any other browser search for your browser + json viewer and you should find something similar!)

3. Check that it returns what you want! 🕵️‍♀️

4. Finally convert it into python so in this example this would be the call to requests

```python
requests.get("https://pokeapi.co/api/v2/generation/1")
```

## Import requests

❓ You need to add the requests library to the python file in `pokemon/lookup.py`!

If you get stuck checkout this [page](https://requests.readthedocs.io/en/latest/user/quickstart/)

Once you are done you can checkout whether it was done correctly by running the test from your terminal 💻

```bash
pytest tests/test_lookup.py::test_import_requests
```

## Get pokemon

Now go to `lookup.py` **your goal is to complete the first function** `get_pokemon`.
So far you have the function outline

```python
def get_pokemon(limit: int = 100, offset: int = 0) -> dict:
    """Get a list of pokemon. Return a dictionary containing the results. Limit the results to `limit` and offset by `offset`"""
    pass  # YOUR CODE HERE
```

There is some important information here to help you. The function has the params filled in with types so `limit: int` means your function will accept an integer argument called limit. The `-> dict` tells you that the function should return this type. Finally between the `"""` we have a docstring which describes the intent of a function.

❓ With all of the information try and code this function!

Once you think your function works you can test it with this command:

```bash
pytest tests/test_lookup.py::test_get_pokemon
```

If everything is good you will get a response similar to this 👇

```bash
============================================================================================================== test session starts ===============================================================================================================
platform linux -- Python 3.8.14, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/oliver.giles/code/lewagon_dev/data-engineering-solutions/01-Software-Engineering-Best-Practices/02-Python-For-Data-Engineering/01-API-Requests
collected 1 item

tests/test_lookup.py .                                                                                                                                                                                                                     [100%]

=============================================================================================================== 1 passed in 0.60s ================================================================================================================
```

**If you do move on to the next section!**

If not, try to read the message and understand why your function is not passing the test. Go back an iteration and try to update your function until it passes! Using the output of tests to write your code is a really important practice when working on a large codebase with lots of other engineers.

## Code the other functions

❓ Now code the other functions inside `lookup.py`

1.
Code `check_pokemon_move` which checks whether a pokemon can learn a move

Test 🧪:
```bash
pytest tests/test_lookup.py::test_check_pokemon_move
```
2.
Code `get_pokemon_types` which gets all the pokemon of a given type or of two types if an optional second type is given

Test 🧪:
```bash
pytest tests/test_lookup.py::test_get_pokemon_types
```
3.
Finally code the most complicated function `get_evolutions` which looks up the pokemon which either it has evolved from, to, or both!

Test 🧪:
```bash
pytest tests/test_lookup.py::test_get_evolutions
```

## 🏁

🚀 Finally run all of the tests:

```bash
make test
```

If they all pass you should push your code and move onto the next exercise!

```bash
git add --all
git commit -m "finished pokemon api exercise"
git push origin main
```
