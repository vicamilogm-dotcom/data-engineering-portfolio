
## Goal 🎯

The goal of this exercise is to give you the necessary tools to load test, log and monitor your systems.
This way, you'll be able to understand where your system is the most likely to break using load testing.
You'll also be able to collect the logs, so no information is lost in the void. Finally, you'll set up a simple monitoring system that will alert you and keep track of all your system malfunctions.

For this exercise, we'll only scratch the surface as this is a complex and time-consuming topic. We'll rely on some already provided snippets and codebase and of course, out-of-the-box 3rd party tools and libraries 🎁

## Setup

All you need for this exercise is a working docker setup 🐳

Explore the files in the `/app` folder, where some code is prefilled for you:

```bash
tree app/
app/
├── logs                  # a folder for storing log files
├── __init__.py
├── config.py             # Pydantic Settings model
├── fibonacci.py          # A class to compute Fibonacci numbers
├── logging.conf          # A config file for logging
├── main.py               # Entrypoint for the FastAPI
└── request_models.py     # Pydantic models for API endpoints
```

## 1️⃣ Load testing

<details>
  <summary markdown='span'><strong>📝 Instructions (expand me)</strong></summary>

Let's start by load testing the FastAPI server included with this exercise in the `app` folder.

Disclaimer: **this server has a buggy endpoint**. We'll see how to monitor and address those issues during this exercise. So don't worry if this is not working flawlessly. That's exactly what you're here to fix!

In order to load test, we'll use a package named [Locust](https://locust.io/). We'll create a docker compose stack to run our server and locust and create a small locust file that will simulate a user's behavior.

### Create the Docker compose stack
in the `docker-compose-task-1.yml` please do the following:

**1. API Service 🌐**

1. Add the API service, running the FastAPI server (we'll not going to deploy this one on Cloud Run).
 - create a service named: `webapi`
 - Building the docker image `Dockerfile-fastapi` (already written for you 🎁)
 - With a `on-failure` restart policy (we'll actually see it in action today!)
 - Expose port 8000
 - Mount the `./app` dir into the `/app/app` container dir
 - The `command` will be picked up from the Dockerfile - if you add one in the `docker-compose` file, it will take priority ℹ️


**2. Locust Service 🦗**

[Documentation](https://docs.locust.io/en/stable/running-in-docker.html)

Using the documentation, add the following snippet to your docker compose file. It creates a master and worker node to run the load testing. 👇

```yaml
  master:
    image: locustio/locust
    ports:
     - "8089:8089"
    volumes:
      - ./:/mnt/locust
    command: -f /mnt/locust/locust.py --master -H http://webapi:8000

  worker:
    image: locustio/locust
    volumes:
      - ./:/mnt/locust
    command: -f /mnt/locust/locust.py --worker --master-host master
```

❓ Adjust the host `-H webapi:8000` as needed for Locust depending on your **service name.**


**3. Build and test ⚙️**

- Build the stack `docker compose -f docker-compose-task-1.yml build`
- Run the stack `docker compose -f docker-compose-task-1.yml up`
- If you head to http://localhost:8000 you should see "hello world"
- If you head to http://localhost:8089 you should see the locust homepage

**3. Creating a load testing scenario 🗺️**

Now we need to set up the load test! To do so let's refer to Locust's [documentation](https://docs.locust.io/en/stable/writing-a-locustfile.html).
The `locust.py` at the root of the folder defines the load testing scenarios and configuration.
It simply defines the simulated user behavior for locust to use.

💻 It's your turn to complete the `WagonFakeUser` class:

- Configure the wait time to be between 1,5; the user will wait between 1 & 5 seconds before firing a new request.
- Add 3 tasks to hit the 3 endpoints of our server:

```
task: index - GET /
task: compute_addition - POST /addNumbers JSON Body: { "a": <random Int>[-150, 150], "b": <random Int>[-150, 150]}
task: compute_fib - POST /computeFib JSON Body: { "iteration": <random Int>[0, 30]}
```

- Adjust each task priority with a `@task(<PRIORITY>)` decorator. The higher the relative number, the most likely the simulated user will run it.


**4. Load testing 🔫**

- Build and run the docker compose stack
- Head to localhost:8000 -> you should see `hello world`
- Head to localhost:8089 -> This is the locust interface
- Configure the load test host. It should how the right `host` to hit your `api` 👇

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D5/locust-home.png" width=700>

Let's find the server breaking point; API failures are expected since the logic has an issue on purpose.
(depending on your machine, the breaking point will be different)
- Simulate 1 user and observe the test; the server should handle it fine; click the stop button
- Simulate 10 users with a spawning rate of 1
- Simulate 50 users with a spawning rate of 3
- Simulate 100 users with a spawning rate of 10

It should probably be broken by now; congrats! i.e., the server is stalling, new logs aren't printed, and the service is defaulting; if it is not stalling, keep going to infinity and beyond.
You should also notice the restart policy kicking in when the server crashes.

The reason is that the server is running a single node and is not capable of handling all the users we throw at it; we need to create more nodes/workers to be able to handle the load. 🏋️‍♂️

</details>

## 2️⃣ Handling more requests 🔥

<details>
  <summary markdown='span'><strong>📝 Instructions (expand me)</strong></summary>

To solve the problem we faced in task 1, we'll introduce [Gunicorn](https://gunicorn.org/), a WSGI HTTP server that will help us create more uvicorn workers and manage them.

Gunicorn will act as a process manager for our uvicorn+fastAPI server - basically it will dispatch requests to Uvicorn instances. [You should read more about it here](https://www.uvicorn.org/deployment/#using-a-process-manager) 📚

Fortunately for us, the FastAPI team already provided the resources to run this production-like setup on our machine; let's use that! 🙌

**1. Switch up the stack**

We will rely on this [docker image](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#uvicorn-gunicorn-fastapi) - It is a performance auto-tuned gunicorn-uvicorn-fastapi stack (lots of unicorns here 🦄).

For this task, use the `docker-compose-task-2.yml`

**2. Update the webapi service**

- Change the dockerfile built to `Dockerfile-gunicorn-poetry`, a multistage build for poetry, our dependencies and relying on the unicorn image.
- Add restart policy: `on-failure`
- Export port `8000:8000`
- Map the volume `./app` to `/app/app`
- Add an `.env` file with the below variables and load it in the service
```
      - PORT=8000
      - PYTHONBUFFERED=1
```
- Build and run the stack - You should immediately notice the multiple uvicorn workers being spawned. it's almost magical (it just means someone made it magical for us 🙏)

What we just did is called **horizontal scaling** - we added more replicas without adding more resources. ⚠️ Note that you don't need to add your own `command` or `CMD` - it's a bit hidden away, but it's actually handled by a script [here](https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/58ce0895f8c38b895e84f7ddb2128d66748b437c/docker-images/start.sh#L34).

**3. Load test again 🔫**

Re-run the previous load testing scenarios; the breaking point should be pushed a lot further - you will hit one eventually because your machine can't infinitely scale vertically (*psst*, you can use Kubernetes for that).

Some workers will get killed in the process due to our malfunctioning code, and you should see how they are spawned back up by gunicorn.

Your job here is done. 👏

Feel free to play around with the [environment variables](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#environment-variables) accepted by the gunicorn docker image to see if you can squeeze more performance from your machine 🧽.

Also, a few numbers to put things in perspective 🪞:

`1 RPS` = 1 Request per second
if you have a service receiving 1 RPS - it adds to 86400 requests a day (that's good for most MVPs)

`20 RPS` - 1.7 million requests a day

Ikea.com had 209 Million visits in November 2022 [link](https://www.similarweb.com/website/ikea.com/#overview); this is equivalent to 80 RPS - were you able to beat Ikea.com today? 😬 By the end our `vm` can handle 100 rps comfortably 👇 before finally crashing trying to go up to 200 🤯

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D5/locust-max.png">

</details>


## 3️⃣ Logging 📄

<details>
  <summary markdown='span'><strong>📝 Instructions (expand me)</strong></summary>

Now let's try and improve our app's logging going to debug our issue. Logging is a fairly complex topic and requires some attention to setup properly when using different systems together.

For us, we are using FastAPI -> Uvicorn -> Gunicorn, which means we have to **propagate*** and handle the logs properly between each layer to be able to retrieve them.

Here we'll start from an already existing configuration and extend it. They are many ways of doing that, such as creating a [gunicorn config file](https://docs.gunicorn.org/en/stable/settings.html), a dict config or setting it in the code. We choose to do a specific `logging.conf` file to cleanly isolate the logging configuration from the rest of the system. ✨

We aim to log all the incoming requests and errors to a file for later inspection.

Head to the `logging.conf` file. You will rely on the python [documentation](https://docs.python.org/3/library/logging.config.html#configuration-file-format) to create the configuration. 💻

**1. Sections 🗃️**

First create the following sections at the top of `logging.conf`:

- 3 `loggers`: `root`, `gunicorn.error`, `gunicorn.access`
- 3 `handlers`: `console`, `error_file`, `access_file`
- 2 `formatters`: `generic`, `access`

You'll notice we have provided you with the **most of the required sections!**

**2. Configuration 🛠️**


Each logger must define a default configuration composed of a `level`, a `handler` and the `propagate=1` to forward logs to a parent logger, where one exists.

❓ You need to define the final `root` logger with the correct configuration! We want it at debug level and output to the console!


We added the formatter for you - they define the format of the output and can be **finicky** to adjust. For a deep-dive, check the [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html). 📚


Our handlers are responsible for redirecting the log object to the appropriate output for example to the correct `file`

Your logging configuration should now be ready to be used. 🙌

**3. Configuration update 🔧**

To use this configuration for our stack, we need to pass the location of our config file as a command argument to gunicorn and set the log level to `DEBUG`.

❓ Check the gunicorn-uvicorn docker image [environment variables](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#environment-variables) documentation to find which variables you should add to `.env`?

  <details>
    <summary markdown='span'>💡 Answer</summary>

  ```
  #.env
  - LOG_LEVEL=DEBUG
  - GUNICORN_CMD_ARGS=--log-config /app/app/logging.conf
  ```
  </details>


- Run the stack, and trigger a load test; you should see the `.log` files appear and populate in your local file system in the `/app/logs` directory! 🙌

You can also add custom logging calls in your `main.py` to test the log output:

```python
logger.info("this is an info message")
logger.warning("this is a warning message")
logger.error("this is an error message")
```

**4. Grep 🔍**

Now that we have our logs, we can use one of the most useful commands while groveling through the logs: `grep` ⭐

> ℹ️ `grep` searches the input files for lines containing a match to a given pattern list. When it finds a match in a line, it copies the line to standard output (by default), or whatever other sort of output you have requested with options.

1. Find all the errors in the log file, sort them

```bash
grep "STR_TO_LOOK_FOR" <file> | sort
```

2. Find all the failing requests in the access log (status code != 200)

```bash
grep -v -e 200  <file> # -v is invert match and -e is pattern matching
```

</details>

## 4️⃣ Monitoring 🔬

<details>
  <summary markdown='span'><strong>📝 Instructions (expand me)</strong></summary>

Now that we have our load test & logging, we want to make sure that we'll get alerted and have a trace when things go bad when we are away.

To do so, we'll introduce [Sentry](https://sentry.io/welcome/) - a convenient and easy monitoring tool, albeit not totally free. In this task, we'll setup Sentry using a Pydantic `Settings` model and the [sentry-sdk](https://pypi.org/project/sentry-sdk/) pip package.

**1. Creating the Settings class ⚙️**

Use the [FastAPI setting documentation](https://fastapi.tiangolo.com/advanced/settings/) to help you!

- Head to the `config.py` file and add a class property `sentry_key: str` to the Settings model. We'll use this property to store our very secret sentry key.
- Add a `SENTRY_KEY` variable to your `.env`. We'll populate it later.
- Configure the `Settings` model to load variables from the `.env` file
- Head to `main.py` and add the following snippet after the FastAPI app creation `app = FastAPI()`

```python
@functools.lru_cache()
def get_settings():
    return Settings()
```

Our Settings model should be ready for usage 🙌

**2. Create a sentry account 👤**

- Create a sentry account to get the key; it has a free trial of 2 weeks and a [limited dev tier that is free](https://sentry.io/pricing/).

**3. Sentry integration 🧰**

We are going to use the [ASGI Middleware](https://docs.sentry.io/platforms/python/guides/asgi/) plugin since we are using FastAPI, and [ASGI](https://asgi.readthedocs.io/en/latest/) framework.

- Create your first project in sentry
- Choose the `asgi` integration
- Copy and paste the key in the `dsn=` to the `.env` file. It's an API token and your `SENTRY_KEY` that allows you to communicate to your sentry project

```
SENTRY_KEY="https://examplePublicKey@o0.ingest.sentry.io/0"
```

- Add the following snippet of code below the settings section in `main.py` to integrate sentry

```python
sentry_sdk.init(
    dsn=get_settings().sentry_key,
    traces_sample_rate=1.0,
)
app.add_middleware(SentryAsgiMiddleware)
```

**🚨 Reduce your Locust RPS to a minimum (say, 10 max) so as not to use all your Sentry Monthly Free Credits! 🚨**
- 10,000 transaction max / month
- 5,000 error logs max / month


**4. Monitoring 📈**

- Stop and relaunch your docker stack
- Do a query to the below endpoint - using `ipython`, `curl`, browser, or whatever you prefer.
```
GET - http://localhost:8000/sentry
```
Sentry propagates any exception your system encounters to your sentry dashboard.
- Check that you have this exception in your dashboard
- Run a Locust load test and watch the dashboard fill up!
- After a few minutes, the "Performance" dashboard should also start showing some info


Congrats, you have now all the tools to properly debug an app in production and understand its breaking points 💪

</details>


## 5️⃣ Fix the server 🧰

<details>
  <summary markdown='span'><strong>📝 Instructions (expand me)</strong></summary>

**1. addNumbers**

Find out why this simple addition is not working and correct it. The goal is to either only allow some numbers to be added or to allow any numbers to be added.

> You probably already figure out why this endpoint breaks. But if not yet, why not create a custom log for the crashes to help you? Check out Optional Task #1

**2. computeFib**

Find out why the Fibonacci endpoint is slow for high iterations (>20). Try to fix it using memoization (i.e., caching) by adding a `compute_fast` method to the class. Hint: have you seen some other caching method used in this exercise already? 🤔

### You did it! Let's test! 🛠️

Run `make test` which will test your `docker-compose` and `logging.conf` files. All green? 🟢 **Congrats! 🥳**

In this exercise you went end-to-end from broken server, to:

- Load testing it with Locust to see what's broken and the server's limits 🏋️‍♂️
- Scaling the server with `gunicorn` as your `uvicorn` process manager 🦄 🦄 🦄
- Logging the observed requests and issues with Python `logging` module 📝
- Monitoring performance and errors on Sentry 📉
- And finally fixing your server! 🙌

Time to commit and push your code and onto the next challenge 🏇

</details>

## 6️⃣ Optionals

<details>
  <summary markdown='span'><strong>📝 Instructions (expand me)</strong></summary>

**Optional #1 - custom event logging in Sentry**

You've probably already figured out why the `addNumbers` endpoint sometimes breaks. But what if you need to support another team to understand the errors? Or what about your colleagues who don't know `numpy`? 😱

By default, when using the ASGI middleware provided by `sentry-sdk`, the exception inside the endpoint will get captured in the dashboard. But it's hard to debug when we can't easily see what was the payload that crashed the server 🥷

To help with analysis of this error, instead of just `raise e` what was coded for you in the endpoint to start with, let's track this exception on Sentry **along with the params received by the endpoint**.

💻 Check out the [FastAPI custom instrumentation](https://docs.sentry.io/platforms/python/guides/fastapi/performance/instrumentation/custom-instrumentation/) documentation on Sentry to see how to track a custom `span` and with it send custom `tag`s or `data`.

🟢 Once successfully implemented, you should see your custom error log appear in `Performance -> Suspect Spans` in the Sentry dashboard.

**Optional #2 - custom logging**

To better understand the caching mechanism used for our Fibonacci `compute_fast` method, let's log the cache status of this method each time the endpoint is called. 📝 This type of logging can also help spot excess caching on your server.

💻 In the `computeFib` endpoint add a `INFO` level log of the method's current cache state. [functools documentation](https://docs.python.org/3/library/functools.html#functools.lru_cache) will help you find the right code to access it! 🙌

🟢 Once successfully implemented, you should see your custom log appear in one of your `.log` files.

</details>
