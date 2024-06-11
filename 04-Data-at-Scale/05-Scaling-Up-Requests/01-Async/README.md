## Intro

As seen today, queues allow our programs to talk asynchronously to one another or between functions internally. Imagine it as a queue in a fast food restaurant:

- Place an order == call a function/API 🗣️
- Get a ticket with your order number == place the pending function in a queue 🎟️
- Periodically check your order on the screen == periodically check the queue for any completed functions 👀
- Pick up your order when alerted that it's ready == return a function's result when it's completed 🍔

While Python is fundamentally synchronous by design, Python 3.4 and later bring ways to program asynchronously.

In the exercise below, we introduce asynchronous programming in Python and a FastAPI server. By the end, you'll have implemented and deployed a simple server that responds to both `sync` and `async` requests. We'll call these simultaneously and test the differences in speed and scale of using `sync` and `async` programming.

In this exercise, we will leverage the fact that these API endpoints don't do any heavy computing, making them mostly **I/O bound, and not CPU bound**.

Wait 🖐️, you said *"I/O bound and CPU bound"*, what does this mean? 🤔

<details>
  <summary markdown='span'>Click me to read about it 📚</summary>

We can split work that a computer executes into two parts:

- Computation that runs on the CPU. For instance, a program that computes new digits of Pi π or does large matrix multiplications will typically be doing these calculations on the CPU, it's just crunching numbers. **CPU bound is: if you get a faster CPU, the program runs faster 🚲 => 🛵.**

- Data exchange that is managed by the I/O (Input / Output) subsystem. There are one or more subsystems for each of the peripheral devices your computer works with: disks, terminals, printers, and.. **networks** like the Internet. A program is **I/O bound if it runs faster if the I/O subsystem was faster**.

For instance, take a program that downloads a 1GB file from the internet. Your computer is just exchanging data between two I/O subsystems: the Internet network and your computer disk. There is no computation happening per se. Using a faster CPU should not help download the file faster. Hence, your CPU is essentially waiting for I/O to finish the data transfer - **meaning, this task is I/O bound**.

⌛ I've got a program that requires to download 20 files, I need it to go fast. What do I do?

⭐ Enter **asynchronous programming!**

</details>


# 1️⃣ Key concepts 🔑

<details>
  <summary markdown='span'><strong>📝 Instructions (expand me)</strong></summary>

**Event loop ♻️**

The event loop is the core of every `asyncio` application. Event loops run asynchronous tasks and listen for their callbacks, perform network I/O operations, and run subprocesses.

In short, there is one master process called the **event loop**. You can queue tasks on it (mainly I/O bound tasks), it will run the I/O operations in the background and "alert you" when they're done. This way, if you have many simultaneous I/O bound operations to run, queueing them on an event loop in Python is an easy way to speed up the work. ⏩

**`async` / `await`**

Python introduced in version 3+ two keywords: `async` and `await` that allow to define and call asynchronous functions.

Typically, here's how you use them:

- Instead of naming a function `def call_api(...)` you name it `async def call_api(...)`. It will "tell" the Python interpreter this function is mostly I/O bound and can be run on an event loop.
- To call this function and tell the program to wait for the result, you don't just call it `call_api(arg1, arg2)` but you prefix the call with `await call_api(arg1, arg2)`.

Then, to actually **run** these api calls, you need to call `asyncio.run(call_api(...))`

```python
async def call_api(address):
    print(f"call_api {address} started...")
    await asyncio.sleep(2)
    print(f"call_api {address} done")

asyncio.run(call_api("one"))
# --> call_api http1 started...
# --> call_api http1 done
```

You can make 2 concurrent calls with `asyncio.gather()` before `run()`

```python
async def call_many_api():
    await asyncio.gather(call_api("http1"), call_api("http2"))

asyncio.run(call_many_api())
# --> call_api http1 started...
# --> call_api http2 started...
# --> call_api http1 done
# --> call_api http2 done
```

⚠️ `asyncio.run()` is a new syntax (python >3.7), and you may find an older one on the internet where you manually call the event loop:

```python
# Equivalent (old syntax)
loop = asyncio.get_event_loop()
loop.run_until_complete(call_many_api())
```

Now let's write our own example together! 🙌

</details>


# 2️⃣ First Python **async** program 💻

<details>
  <summary markdown='span'><strong>📝 Instructions (expand me)</strong></summary>

The files are under the `lwasync` directory.

```bash
tree lwasync/
lwasync/
├── client_asynchronous.py
├── client_synchronous.py
└── server.py
```

**Objective**

We've added a FastAPI server that you will use, but not change, in `server.py`. It has a few API endpoints that you will be testing:

- `GET /say-hi` which will respond with a greeting and the time it took to process the request

And three endpoints that simulate a real task being done with :

- `GET /standard-run` which is a traditionally defined route, no `async/await`
- `GET /slow-run` which is an `async` route but uses a traditional `time.sleep`
- `GET /fast-run` which is an `async` route that uses an `await`'ed sleep


🚀 Run `make run-server` and keep the server running in a dedicated terminal window.

### A "naive" synchronous example 🎠

Synchronous code lies in the `client_synchronous.py`. Follow the function docstrings and comments to complete `make_one_call`, `make_many_calls` and `generate_statistics_sync` functions. 💻

When you're done:
- Make sure the server is running in a terminal window. If not, open one and run `make run-server`.
- Run your code with `generate_statistics_sync` - feel free to use `ipython`, notebook or any other way. You can replace the default number of calls, 10, by any other number. **How long did it take?**

### An asynchronous equivalent 🏎️

Open the files `client_synchronous.py` and `client_asynchronous.py` side by side in VSCode (you can use "View: Split Editor Right"). Read through the code in `client_asynchronous.py` - pay attention to the key differences, comments and docstrings.

💻 Now fill in the blanks in the `make_one_call`, `make_many_calls` and `generate_statistics_async` functions to test the `/say-hi` endpoint.

### Let's run a comparison

1️⃣ Run synchronous and asynchronous calls to `/say-hi` with a call number of 10. Which one wins? By how many multiples?
2️⃣ Double the number to 20. Is the speed factor the same or twice as good? Make sure you understand *why?* 🤔

### Let's test! 🛠️

Run `make test_sayhi` to test the code you've written so far. Remember to keep your server running in a terminal tab while testing.

Everything green? 🟢 Let's move on to a **scaling this API with serverless execution!**

</details>

# 3️⃣ Serverless Scaling

<details>
  <summary markdown='span'><strong>📝 Instructions (expand me)</strong></summary>

In this exercise you'll deploy this API to a cloud provider's serverless framework for Docker containers:

- GCP: [Cloud Run](https://cloud.google.com/run).
- Amazon: [Fargate](https://aws.amazon.com/en/fargate/).
- Azure: [Container instances](https://azure.microsoft.com/en-us/services/container-instances/)


In the exercise below, we'll follow the GCP route. But the steps are fairly similar between all serverless Docker container execution providers.

## Step 1/5 Test other API endpoints locally

We've already built a small FastAPI server. We've tested the `/say-hi` endpoint already, now let's look at the other 3 endpoints that simulate running a longer task.

Run the app locally with `make run-server`. Now let's check that the endpoints work:

- Run `curl http://127.0.0.1:8080/slow-run -w %{time_total}`
- Run `curl http://127.0.0.1:8080/fast-run -w %{time_total}`
- Run `curl http://127.0.0.1:8080/standard-run -w %{time_total}`

You should notice four things:

1. We've added the option `-w %{time_total}` to `curl` which prints the total time the endpoint takes in seconds - very handy in testing response time!
2. Check the amount returned by the `curl` commands in all calls. Is it almost the same across 3 endpoints? Good! 🙌
3. See the `app_instance_id` returned by the app, it should be the same as we're running the same instance of the application (our terminal window).
4. Now stop the app and re-run it with `make run-server`. Make another curl call (either one above works). Is the `app_instance_id` the same? It shouldn't be! We're running a new instance of the application. This will help us identify which instance of the application is running in the cloud for the purposes of this exercise. 🌩️

## Step 2/5 Build the Docker image

We've written the Docker image for you, see the `Dockerfile` contents below. Run through its lines and comments and make sure you understand each step. Then paste it into the `Dockerfile` file.

```Dockerfile
# Start from Python 3.8.14 base image, the slim version is usually enough (stripped from packages that aren't useful for our purpose)
# and way smaller than the non-slim version
FROM python:3.8.14-slim

# Setting PYTHONUNBUFFERED to 1 is useful for logging
# See https://stackoverflow.com/a/59812588
ENV PYTHONUNBUFFERED 1

# Set a working directory that maps our data-engineering-challenges repository structure
WORKDIR /03-Data-at-Scale/05-Scaling-Up-Requests/01-Async/

# Install Poetry
RUN pip3 install --upgrade --no-cache-dir pip \
    && pip3 install poetry

# Copy the installation files and local dependencies first (in this case there aren't local dependencies)
COPY poetry.lock pyproject.toml ./

# Now we are ready to install the packages
RUN poetry install --only main

# Copy this package's Python files last
COPY ./ ./

# Set a default PORT environment variable to 8080
ENV PORT 8080

# Run the `FastAPI` application on port 8080
CMD poetry run uvicorn lwasync.server:app --host 0.0.0.0 --port $PORT
```

**Then run `make build` to build the Docker image locally**. Feel free to test it locally - remember to forward ports to your VM's localhost with `-p` flag when using `docker run` and let VSCode port forwarding magic handle the rest 🪄

## 3/5 Set up the Artifact Registry

**Note: if you've already set one up in the bootcamp, reuse it ♻️ and skip this step!**

We're going to deploy our Docker image to a repository on [Google Cloud Artifact Registry](https://cloud.google.com/artifact-registry).

❓ Check their [CLI documentation](https://cloud.google.com/sdk/gcloud/reference/artifacts/repositories) - can you construct the command to create a Docker image repository **called `docker-hub`**, in a **region of your choice**, that accepts **Docker format images** and with a short **description** 🤔

<details>
  <summary markdown='span'>💡 Solution</summary>

  ```bash
    # run this first if your Artifact Registry services is not yet enabled
    gcloud services enable artifactregistry.googleapis.com

    # then the command itself
    LOCATION=europe-west1 # or another location of your choice (gcloud artifacts locations list)
    gcloud artifacts repositories create docker-hub \
    --repository-format=docker \
    --location=$LOCATION \
    --description="Docker image storage"
  ```

  You then need to allow Docker to push to and pull from this repository:

  ```bash
    # If $LOCATION is "europe-west1"
    HOSTNAME=europe-west1-docker.pkg.dev

    gcloud auth configure-docker $HOSTNAME

    # then press 'y' when prompted
  ```

  This should have updated credentials in your `~/.docker/config.json` file.
</details>

Once you have a repository on Artifacts Registry, copy it's full address using the "Copy" icon on the right of your registry (see screenshot below) and write the value in the `Makefile`, in the `REGISTRYPREFIX` variable.

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/lw-artifact-registry-copy.png" alt="Copy" width=600>

Run `make test` to check you're ready to deploy 🛠️

We're all set on the browser side, let's go back to the terminal and push our first Docker image to our remote repository now. 🚀

## 4/5 Deploy the image to the artifact registry

Let's do:
- Run `make tag`, which will tag our local image with the remote repository prefix.
- Run `make push`, which will push our image to the remote repository.

Once done with the upload, refresh your browser page, you should see a Docker image showing up in the registry.

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/lw-artifact-registry-images.png" alt="Images" width=600>

> ❓ Bonus points - can you find a CLI command in [gcloud artifacts](https://cloud.google.com/sdk/gcloud/reference/artifacts) docs to list the images instead? 🤔

## 5/5 Deploy the application in Cloud Run

> ❓ Super bonus points - can you construct a [gcloud run](https://cloud.google.com/sdk/gcloud/reference/run) command to do all the steps below from your terminal? 💪

Almost there! In the browser, go to the Cloud Run service and click `CREATE SERVICE`.

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/lw-cloud-run-create.png" alt="Create" width=600>

- In "Deploy one revision from an existing container image", click `SELECT`. In the `Artifact Registry` tab, you should find your image 🤙.
- Give it a unique service name
- Pick a local region.
- Select "CPU is only allocated during request processing" (should be selected by default).
- Autoscaling: 0 (minimum) to 3 (maximum) instances
- Authentication: choose `Allow unauthenticated invocations`, this allows you to call this API from anywhere on the internet.
- Open `Container, Variables & Secrets, Connections, Security`
  - What should the container port be? Hint 💡 : what is the port the FastAPI app runs on? Check the `Makefile`, `run` target.
  - Keep the capacity at its lowest values, our app doesn't do much 🦶.
  - Maximum requests per container: **set it to 5**.
  - In the environment variables, set `HOME` to `/root`. By default, Google Cloud Run has a [strange behaviour](https://chanind.github.io/2021/09/27/cloud-run-home-env-change.html) we need to override.
- We're good to go! Click `CREATE` and let the magic happen. Once up and running (which can take up to 5 minutes), you'll get a URL for your service. 🙌

<details>
  <summary markdown='span'>💡 Bonus points solution</summary>

  ```bash
  TAG=lewagon/serverless:0.1 # adjust this and further ENV vars as needed

  gcloud run deploy $SERVICE_NAME \
  --image=$LOCATION-docker.pkg.dev/$PROJECT_ID/docker-hub/$TAG \
  --region=$LOCATION \
  --min-instances=0 --max-instances=3 \
  --allow-unauthenticated \
  --port=8080 \
  --concurrency=5 \
  --set-env-vars=HOME=/root
  ```

  Check if you got any `warnings` in the command response - it might ask you to update IAM policy for the Cloud Run services with a command similar to this:

  `gcloud beta run services add-iam-policy-binding --region=$LOCATION --member=allUsers --role=roles/run.invoker $SERVICE_NAME`

  You're good to go! 🙌
</details>

Congrats! You should now have a production FastAPI running on Cloud Run 🥳 Check that it's online by going to the `/docs` endpoint of your given Service URL.

</details>


# 4️⃣ API Analytics

<details>
  <summary markdown='span'><strong>📝 Instructions (expand me)</strong></summary>

To understand the internals of Cloud Run and sync/async routes, we are going to
- make a lot of requests to our API
- check on which instance of the API the request was processed
- run some analytics on load time
- find the root cause why we're getting these statistics! 🕵️‍♂️

Time to go back to the `generate_statistics_async` function in `client_asynchronous.py`.

- Update the url you're calling to `https://serverless-something-ew.a.run.app/fast-run` and replace `serverless-something-ew.a.run.app` with your own Service URL

### Experiment 1

- Open an IPython interactive shell by just typing `ipython` in your terminal. Jupyter works too if you prefer.
- Load the `autoreload` extension with mode `2` as we will need to update `api_url` during the experiment 😉
- Import the function `generate_statistics_async` from the `lwasync.client_asynchronous` module.
- Let's run the following calls:

  ```python
  # Run a first "cold" call of 25
  stats_first_run_25, duration_first_run_25 = generate_statistics_async(25)

  # Run the exact same call a second time
  stats_second_run_25, duration_second_run_25 = generate_statistics_async(25)

  # Run a call for 15
  stats_run_15, duration_run_15 = generate_statistics_async(15)

  # Run a call for 12
  stats_run_12, duration_run_12 = generate_statistics_async(12)
  ```

Now let's test some observations 🧐

❓ The first call of 25 takes longer than the second call of 25. Why?

<details>
  <summary markdown='span'>💡 Hint</summary>

  We've set the minimum value of instances to 0. So when the instances aren't running, the first one needs to do a [cold start](https://cloud.google.com/run/docs/tips/general?hl=en#using_minimum_instances_to_reduce_cold_starts).
</details>

❓ How many different `app_instance_id` values are there? Look into `stats_second_run_25` by just typing it and evaluating it in the console.

<details>
  <summary markdown='span'>💡 Hint</summary>

  As many as the number of instances in Cloud Run! Check by doing `len(set(stats_second_run_25["app_instance_id"]))`
</details>

❓ Look into `stats_second_run_25` by just typing it and evaluating it in the console. What do you notice for the last 10 calls?

<details>
  <summary markdown='span'>💡 Hint</summary>

  We have a maximum of 3 (number of instances) x 5 (allowed concurrency of each instance) = 15 calls to our instances that can happen simultaneously to our cloud instances at most.

  Once the first 15 are filled, the following will have to wait for them to complete.
</details>

❓ Finally, what differences do you see in total runtime of the 15 versus 12 runs? Does it make sense?

<details>
  <summary markdown='span'>💡 Hint</summary>

  The calls all happen concurrently on 3 instances which can each accept 5 concurrent requests. Therefore running 4 requests or 5 requests on one instance shouldn't have a significant impact on the total runtime.
</details>


### Experiment 2 - `slow-run` and `standard-run`

Now run `25` API calls to the `/slow-run` and `/standard-run` endpoints and answer below questions:

❓ How long did the `slow-run` endpoint API requests take? Can you calculate why it took this long?

<details>
  <summary markdown='span'>💡 Hint</summary>

  They should have taken around 20 seconds (provided good network connection) ⏱️

  The first 15 requests were picked up by our 3 instance x 5 concurrent request capacity, but because these requests use *synchronous* code, they need to wait for the previous request (2 seconds) to be processed before starting the next one.

  So we still have 3 instances processing requests *in parallel*, but now each request waits for 2 seconds, so a total of 10 seconds to process.

  Then the last 10 requests can be picked by 2 freed-up instances, for another 5x2 = 10 seconds of processing.
</details>

❓ What makes `slow_run` function synchronous compared to `fast_run`? It still has the `async` keyword in definition 🤯

<details>
  <summary markdown='span'>💡 Hint</summary>

  That's right, but remember that `async` needs to be paired with `await` to tell the program what task can be put into the background and "waited for".

  In `fast_run` we tell the program that it can put the `asyncio.sleep` in the background with `await` keyword. But in `slow_run` we're using the synchronous `time.sleep` and not `await`'ing anything - hence the program just executes in a traditional synchronous Python way 🤷‍♂️

  In fact, you might have even received a `429` error from Cloud Run, saying that there was too much traffic for your instances to handle - it's a mechanism of Cloud Run to prevent queueing up too many pending requests.
</details>

❓ What's going on with the duration of 25 calls to `/standard-run`? 🧐

<details>
  <summary markdown='span'>💡 Answer</summary>

  You should notice that `standard_run` takes in essence the same amount of time as `fast_run`. How? It's not using `async/await` and it's using the synchronous `time.sleep` 🤯

  FastAPI is kind enough to pass all `def` functions to an *external threadpool*, because if left in the main process, they would naturally block the execution of the `async def` functions. (slightly) more about it in [their docs](https://fastapi.tiangolo.com/async/?h=technical#path-operation-functions).
</details>

</br>

Were you able to answer all above questions? **Well done! 🔆**

You are discovering a key concept in scaling any application -  **concurrency** (or **asynchronicity**) - in this challenge you have both:

- consumed services concurrently (your `client_asynchronous.py`) 🧑‍🏭
- built services that can be consumed concurrently (your `/fast-run` endpoint) 🏭

</details>

</br>

Remember to commit and push your code to GitHub and onto the next challenge! 🏎️

**Bibliography 📚**

This [article](https://iximiuz.com/en/posts/explain-event-loop-in-100-lines-of-code/) brilliantly explains the event loop and proposes a 100 line implementation of the event loop. If you'd like to understand the internals of the event loop, we highly recommend reading this article and implementing its code as an optional exercise.
