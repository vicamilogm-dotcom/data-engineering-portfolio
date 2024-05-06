The DevOps grail that teams want to achieve is **Continuous Deployment**. The idea is to configure your hosting environment in such a way that every change in `master` which yields a green build on the Build Automation tool _can_ and _will_ be pushed to production as soon as possible.

In this exercise, we will set up a [**PaaS**](https://en.wikipedia.org/wiki/Platform_as_a_service) to host our longest word game.

# HTTP server

Before pushing our code to a hosting provider, we would like to be able to interact with it. The easiest way to do this is to encapsulate the game around a small HTTP server.

We will build a simple page which will display the random grid. Underneath this grid, a form with an input to type a word, and a submit button.

When clicking the button, the form will be submitted and will reload the page to showcase the results.

![](https://res.cloudinary.com/wagon/image/upload/v1560714935/longest-word-mockup_mwtd3d.png)

Open VS code workspace at your "longest-word" folder, and create a branch to start working on this feature.

```bash
cd ~/code/<user.github_nickname>/longest-word

git status # is that clean?
git checkout master
git pull origin master
git branch -d dictionary-api
git checkout -b http-server
```

We are going to use [Flask](http://flask.pocoo.org/), a microframework to quickly build web apps.

```bash
poetry add flask
touch wsgi.py # "Web Server Gateway Interface"
```

Open the `wsgi.py` file and copy paste the following code:

```python
# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello world!"
```

You can start this very basic Flask app with:

```bash
FLASK_DEBUG=true poetry run flask run
```

Open your browser and go to [localhost:5000](http://localhost:5000/). Is it working, do you get "Hello World" as a text response from the server? If not, call a teacher.

This exercise's goal is **not** about implementing the little application (we will cover Flask or FastAPI in details in future lectures. Let's just build together our User Interface:

```bash
mkdir static
touch static/style.css
mkdir templates
touch templates/home.html
```

We just created a CSS stylesheet and the HTML template for the Home page. Let's add the business logic in `wsgi.py`:

```python
# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, render_template
from longest_wold.game import Game

app = Flask(__name__)

@app.route('/')
def home():
    game = Game()
    return render_template('home.html', grid=game.grid)
```

In the code above, we are initializing a new `Game` instance to generate a grid. We pass this grid as a local variable to the `home.html` template, so that we can use it in the view.

Let's add this code in `templates/home.html`:

```html
<!-- templates/home.html -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf8" />
    <title>Longest Word</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <h1>Longest Word</h1>
    <div>
      {% for letter in grid %}
        <span class="letter">{{ letter }}</span>
      {% endfor %}
    </div>
    <!-- Let's build an input "form" so user can type letters -->
    <form action="/check" id="form" method="post">
      <!--hidden input form that contains the game.grid to be sent alongside the word letters-->
      <input type="hidden" name="grid" value="{{ ''.join(grid) }}">
      <!--explicit input form which forces content to uppercase since our `Game` logic only take care of uppercase letters-->
      <input type="text" name="word" onkeyup="this.value = this.value.toUpperCase();">
      <button>Check!</button>
    </form>
  </body>
</html>

```

We give you also some CSS to add in `static/style.css`:

```css
/* static/style.css */
body {
  font-family: sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
.letter {
  border: 1px solid #999;
  padding: 8px 6px;
  width: 24px;
  display: inline-block;
  text-align: center;
  background-color: #333;
  color: #eee;
}
#form, #results {
  margin: 1em 0;
}
.valid {
  color: green;
}
.invalid {
  color: red;
}
```

Phew! Now let's try this! Head over to your browser and reload the page. Can you see the grid with a form? Awesome!

If you try to play, you will get an error. It's because we have not implemented the `/check` endpoint yet (the one where the form gets submitted to).
Let's do it :

```python
# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, render_template, request

# [...]

@app.route('/check', methods=["POST"])
def check():
    game = Game()
    game.grid = list(request.form['grid'])
    word = request.form['word']
    is_valid = game.is_valid(word)
    return render_template('check.html', is_valid=is_valid, grid=game.grid, word=word)
```

❓ Take some time to understand how this works.
- When we GET "/", we generate a grid and send game.grid to the `home.html`
- When we POST "/check", the `home.html` l:19 sends us back the `form['grid']` that we can parse in python
- We also receive `form['word']` that we check for validity
- We finally feed all this information back to the `check.html` view to be used to display the results...

💡 Notice how we need to actually pass the grid in the `POST` request as HTTP is **stateless**.

```bash
touch templates/check.html
```

```html
<!-- templates/check.html -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf8" />
    <title>Longest Word</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <h1>Longest Word</h1>
    <h2>Result</h2>
    <div>
      {% for letter in grid %}
        <span class="letter">{{ letter }}</span>
      {% endfor %}
    </div>
    <div id="results">
      Your word: <strong>{{ word }}</strong>.
      {% if is_valid %}
        <span class="valid">Congrats, it's valid!</span>
      {% else %}
        <span class="invalid">Sorry, it's invalid...</span>
      {% endif %}
    </div>
    <div>
      <a href="/">New game</a>
    </div>
  </body>
</html>
```

That's it! Your app should be working correctly. Time to commit, push and _open a Pull Request_ on GitHub:

```bash
git add .
git commit -m "Small web app wrapper around the Game"
git push origin http-server
# head to github.com to open a Pull Request!
```


# Deployment with Google App Engine (GAE)

We'll put our app in production on a live server accessible through world-wide-web.

There are various ways to do so, but we'll start today by the easiest one: Platform as a service (PaaS). In PaaS, you just give the application-code (here, our python package) to your cloud provider, which is going to "pip install it" for you on its own server, and make it readily available through public https address. Most importantly, it will auto-scale the servers for you should you start making lots of requests to the app. For all these convenient reasons, PaaS are almost never free.

In Google Cloud, the relevant service is called **Google App Engine**. Equivalents options are:
- AWS Elastic Beanstalk
- Azure App Service
- Salesforce Heroku

According to the [Google App Engine docs](https://cloud.google.com/appengine/docs/standard/python3/building-app/writing-web-service), your package requires at least the following minimal structure on top of our python package

```bash
├── app.yaml # Config file for GCE
├── main.py # Entry point for GCE
├── requirements.txt # to tell server to `pip install -r requirements.txt`
├── longest_word # Your package
│   ├── ...
│   ├── ...

```


#### `main.py`
This entrypoint should simply call your app instantiated in `wsgi.py`

```python
from wsgi import app

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app
    app.run(host='127.0.0.1', port=8080, debug=True)

```

#### `requirements.txt`

Google AE is not taking into account the modern poetry syntax but is going to try to "pip install -r requirements.txt" the good old way. Therefore, we need to convert `poetry.lock` into `requirements.txt` format:

```bash
poetry export --without-hashes --output requirements.txt
```
#### `app.yaml`
```bash
touch app.yaml
```

```yaml
runtime: python38 # Define the python version pre-installed on the machine
service: default # Give a name to your app. ❗️ First deployment must be called "default"
handlers: # Define how to handle incoming requests. Here, any request will be handled by main.py
- url: /.*
  script: main.py
```

💡 [Stack Overflow post](https://stackoverflow.com/questions/42360790/why-do-i-need-to-deploy-a-default-app-before-i-can-deploy-multiple-services-in) explaining why the first service deployed should be named "default"

🎉 And that's it! There are tons of other potential configuration parameters to play with for a real app, (how to scale, how to handle secrets etc...) but we don't need them today!

#### Deploy

```bash
gcloud app deploy
```
Should give you a public https address with your game playing!


# Continuous Deployment with Google App Engine + Gihub Actions

We are almost there. A quick recap gives us:

1. Our code is on GitHub
1. We have Continuous Integration set up thanks to Github Actions
1. Every commit (in `master` or a feature branch) triggers a compilation from Github Actions
1. A Pull Request status is updated by  Github Actions and gives context to reviewer
1. We still need to **manually** run the `gcloud app deploy` command to deploy

Let's automated this last part and reach the grail!

## Create new Github Action `cd.yml`

We want to create a GHA that is going to "gcloud app deploy" at each "push" on "master".

Remember how we told you that there are tons of officially maintained github actions that you can re-use? Well, we're going to use Google official [deploy-appengine](https://github.com/google-github-actions/deploy-appengine) GHA! (Google talking Microsoft language, how cool is that?)

The only difficulty is to give GitHub VMs your Google Cloud Credentials.

👉 Go to [console.cloud.google.com](console.cloud.google.com), "IAM", "Service Accounts", "Create Service Account"
- Name: "gha-longest-word"
- Description: "github action account for longest-word app"
- Grant the following roles, according to the deploy-appengine [documentation](https://github.com/google-github-actions/deploy-appengine#authorization)
  - App Engine Admin (roles/appengine.appAdmin): can manage all App Engine resources
  - Service Account User (roles/iam.serviceAccountUser): to deploy as the service account
  - Storage Admin (roles/storage.admin): to upload files
  - Cloud Build Editor (roles/cloudbuild.builds.editor): to build the application
  - Artifact Registry Reader (roles/artifactregistry.reader): to read the application's container image
- "Key" --> "Create new KEY" and download the JSON (keep it safe!)

👉 Now, go to your github repo, "Settings", "Secrets and variables", "Actions"
- Add this JSON as a new secret, name it for instance `GCP_SA_KEY`
- You can now use the this key in your GHA using `'${{ secrets.GCP_SA_KEY }}'`

👉 Let's now create the GHA passing these secrets
```bash
touch .github/workflows/.app-engine-cd.yml
```

```yml
# app-engine-cd.yml
name: basic CD
on:
  push:
    branches: [ master, main ]
jobs:
  deploy-to-app-engine:
    runs-on: ubuntu-latest
    permissions:
      contents: 'read'
      id-token: 'write'
    steps:

    # Checkout current branch
    - uses: 'actions/checkout@v3'

    # Authenticate via Service Account Key JSON
    # See https://github.com/google-github-actions/auth#authenticating-via-service-account-key-json-1
    - id: 'auth'
      uses: 'google-github-actions/auth@v1'
      with:
        credentials_json: '${{ secrets.GCP_SA_KEY }}'

    # Use Google official GHA to deploy 🎉
    - id: 'deploy'
      uses: 'google-github-actions/deploy-appengine@v1'

```

## Let's test it!

 That's it! But is it really working?

 Let's do a very simple change. We will update the background-color of grid letters.

```bash
git checkout -b yellow-letter
```

```css
/* static/style.css */
/* [...] */
.letter {
  /* [...] */
  background-color: #FFEB3B;
  color: #666;
}
```

You can test it locally with `FLASK_ENV=development poetry run flask run`. If the CSS change are not picked up, do a [force-refresh](https://superuser.com/a/89811).

Happy with the color? Let's commit:

```bash
git add static/style.css
git commit -m "Change letter grid background-color to yellow"
git push origin yellow-letter
```

Go to github.com:
- create a Pull Request
- wait for your "CI" Action to turn it green
- merge it to `master`
- **Go check your new "CD Action" running** --> It should work!
- Check your updated app online 🎉

👏 👏 👏

**Going further**

This kind of development with small feature branches which are automatically deployed to production as soon as they are merged to master might not work for big feature which need several steps, several pull request, etc. You don't want to keep a feature branch open for weeks as the Pull Request would be basically horrible to review, and merging it back to `master` would be a nightmare. We still encourage small pull requests, but hide the feature being developed behind a [**feature toggle**](https://en.wikipedia.org/wiki/Feature_toggle).


# (Optional) Score & Session


If this is done as well, you can try to implement a feature in the Longest Word Game: a global **score**! The idea is that every time a user finds a valid word, you increment points (1 point per letter). As HTTP is stateless, you need to use the Flask extension [Flask-Session](https://flask-session.readthedocs.io/en/latest/) to handle the concept of **session** (with `SESSION_TYPE='filesystem'`).

# 🏁 Delete your Google App to save costs
In the Google Cloud console, go to
- App Engine
- --> Settings
- --> Disable application
- --> Enter your project ID
