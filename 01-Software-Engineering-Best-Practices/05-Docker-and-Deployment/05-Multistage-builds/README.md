# 🎯 Goal

Docker has some advanced features that can be used to produce even smaller images! Let's explore the difference between multi-stage builds and how they work.

## 🤏 Image Size Optimisation

In this unit we've been reducing image size as much as possible, but why is reducing the size of our image so important? 🤔

Some key reason to optimise image size are:
- **Fast build, pull, and deployment times:** Smaller images mean faster builds during CI/CD pipelines and faster container deployments. Especially important in auto-scaling environments (Kubernetes) where containers need to spin up or down quickly.
- **Improved Security:** Fewer dependencies, smaller attack surface, fewer vulnerabilities
- **Reduced Storage Costs:** Cloud platforms charge for storage. If you have 1000 microservice images and each is 500 MB instead of 100 MB, that's 400 GB of storage that you need to pay for!
- **Optimized Network Bandwidth:** Another cost consideration, if your application is multi-region or multi-cloud, you need to pay for the transfer of images around the network. Smaller image, smaller network costs.
- **Lower Compute Costs:** Large images increase memory and CPU usage, leading to higher cloud costs.

<br>

# 1️⃣ Build a single-stage image

First navigate into the `python/` directory and have a look at the (somewhat familiar Dockerfile) `Dockerfile-single` and build:

```bash
docker build -f Dockerfile-single -t fastapi-single .
```

This image builds an API which runs on port 8000. We can run it with:

```bash
docker run -p 8000:8000 fastapi-single
```

❗ You might have to manually forward port 8080 from your Virtual Machine to your local computer on VSCode.
Let's explore the image with dive!

```bash
dive fastapi-single
```

That image size is ~250 MB, a massive improvement over the >1 GB image that you first created from the day.

Now let's see what benefits we get with a multistage build!

<br>

# 2️⃣ Build a multi-stage image

The multi-stage Dockerfile takes heavy inspiration from a Docker with Python and Poetry best practices example from [depot.dev](depot.dev). Check out the original at [this link here](https://depot.dev/docs/container-builds/how-to-guides/optimal-dockerfiles/python-poetry-dockerfile).

Build your multi-stage image:

```bash
docker build -f Dockerfile-multi -t fastapi-multi .
```

Run it and access it on port 8000 to confirm that it works as intended:

```bash
docker run -p 8000:8000 fastapi-multi
```

While it's building, lets take a look at `Dockerfile-multi` and have a look at what is happening. This Dockerfile is broken into **three** stages.

❗ Note: Creating a user for simplicity, but you should absolutely create one!

## 2.1. Stage 1 - Set environment variables

Stage **one** builds a `base` that will be used by the **second** and **third** stages of this multi-stage build. Stage **one** starts from a base python image and is only setting environment variables:

```dockerfile
FROM python:3.12-slim as base

ENV  POETRY_VERSION=1.8.5 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
```

<details>
<summary markdown='span'>💡 Environment variables explained</summary>

Python and pip:
- `PYTHONUNBUFFERED=1` - Ensures python logs are written to terminal
- `PYTHONDONTWRITEBYTECODE=1` - Disables `.pyc` and `__pycache__` file creation. Saves disk space and unnecessary writes
- `PIP_NO_CACHE_DIR=off` - Retain pip cache for build speed
- `PIP_DISABLE_PIP_VERSION_CHECK=on` - Speeds up pip installation
- `PIP_DEFAULT_TIMEOUT=100` - Set default pip timeout (in seconds), prevents hanging installs

Poetry:
- `POETRY_VERSION=1.8.5` - Set Poetry version for consistency and reproducibility
- `POETRY_HOME="/opt/poetry` - Specify where Poetry itself will be installed
- `POETRY_VIRTUALENVS_IN_PROJECT=true` - Poetry will create venv in the project folder, not globally
- `POETRY_NO_INTERACTION=1` - Prevents Poetry prompts in docker builds

Paths:
- `PYSETUP_PATH="/opt/pysetup"` - Defines where dependencies are installed.
- `VENV_PATH="/opt/pysetup/.venv"` - Where the `.venv` will be created
- `PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"` - Ensures Poetry and Uvicorn are accessible

Why `/opt`?

`/opt` is for optional software instead of the system default (`/root` or `/usr/local`). This keeps dependencies isolated and *should* prevent conflicts with system packages.

</details>

<br>

## 2.2. Stage 2 - Build the poetry environment

The **second** stage is an intermediate stage and will:
- Start from **stage one**
- pip installs Poetry
- Use Poetry to create the python virtual environment

Note that this stage is creating a poetry cache for faster building.

```dockerfile
FROM base as builder

RUN --mount=type=cache,target=/root/.cache \
  pip install "poetry==$POETRY_VERSION"

WORKDIR $PYSETUP_PATH

COPY ./poetry.lock ./pyproject.toml ./

RUN --mount=type=cache,target=$POETRY_HOME/pypoetry/cache \
  poetry install --no-dev
```

## 2.3. Stage 3 - Final Image

The **third** stage is the final stage in the build and will:
- Start from stage **one**
- Copy the python virtual environment from stage **two**
- Set the work directory
- Copy the application files
- Launch the app!

The final image will only contain what is in stage **three**! All previous stages are allowing for a minimal production ready image!

```dockerfile
FROM base as production

COPY --from=builder $VENV_PATH $VENV_PATH

WORKDIR /app

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

We get all the environment variables from stage **one** and copy the python `.venv` from stage **two**.

A visual representation of how this multi-stage Dockerfile is working:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/01050R-docker-multistage.png" width=600>

<br>

Once you've verified that the multi-stage container works the same was as the single-stage container, dive in and explore the image!

```bash
dive fastapi-multi
```

Have a look at the image size and compare the differences!

<br>

# 3️⃣ Alpine Base Images

So far we've been using the `python:3.12-slim` base image. A **Debian** (a Linux OS) based image. There is an *even smaller* base image: `python:3.12-alpine` based on a different Linux distribution, **Alpine**.

Alpine is even smaller with fewer pre-installed packages. Using it with complex python applications with lots of packages will often cause dependency issues, and can be tricky to debug and get your application to work.

To try out an **Alpine** base image, change the base image in stage **one** to `python:3.12-alpine` and change the system update block in stage **one** from:

```dockerfile
RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

To:

```dockerfile
RUN apk update \
    && apk upgrade \
    && rm -rf /var/cache/apk/*
```

**Alpine** uses a different system package manager from **Debian** based distributions.

Build the image with:

```bash
docker build -t fastapi-multi-alpine -f dockerfile-multi .
```

Have a look at the difference in image size with:

```bash
docker images
```

Feel free to test it out with:

```bash
docker run -p 8000:8000 fastapi-multi-alpine
```

And dive into it to look at the file structure!

<br>

# 🏁 Finishing up

Multi-stage builds can be tricky to wrap your head around. If you don't fully understand how they work, that's totally fine. If you want some extra clarity, put the `Dockerfile-multi` into your LLM of choice and ask it to explain it in detail.

It's worth noting that multi-stage builds add some additional complexity when building micro-services like:
- Can be harder to debug and when you look inside the container, it will only contain files copied from the previous stage of the build.
- Potential for longer build times. Can be mitigated with caching.

Generally, follow the software development flow of **make it work, make it right, make it fast**.

Multi-stage builds definitely fall in the **make it right, make it fast** part of the cycle. It's absolutely fine to use a single stage Dockerfile when developing your app!

💡 The **multi-stage Dockerfile** was created to be a re-usable reference for you to use in other projects!

## Option: Docker Multistage Builds for Compiled languages

If you want to see an even more extreme example. Have a look at the `golang` directory for a docker multi-stage build using a compiled language, **Go**. Follow the README for instructions.

<br>
