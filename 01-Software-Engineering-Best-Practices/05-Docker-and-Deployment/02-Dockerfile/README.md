### Engineering context - Real life use

As data scientists or engineers, packaging your code through Docker is key to ensure portability and reproducibility of your results on different hosts. This way, anyone that opens your code will be able to run without issues. Creating clean and extensible Docker images will also help DevOps engineers downstream as they run & test them inside CI/CD systems, or in production (Docker swarm, virtual instances, Kubernetes).

# Goal
This exercise will teach you the Docker fundamentals necessary to mount and operate a Docker container.
You will learn to:
- Create a `Dockerfile` based on the best practices
- Build & tag a Docker image
- Analyse the content and construction of a Docker image
- Spin containers up/down
- Access containers & execute commands inside them with the CLI
- Push images to remote Docker hubs (DockerHub, GCP Artifact Registry)

# Layers
This part illustrates the concept of layers. We will write a bad Dockerfile on purpose to highlight the internal structure of an image.

Open this challenge in the VSS and head to the `Dockerfile-task-1` file. This will be your Dockerfile for this part of the challenge.

**❓Write code in the Dockerfile to meet the following requirements:**

1. Based on ubuntu 20.04

1. Add `ARG DEBIAN_FRONTEND=noninteractive`

*note:* **Do not use ENV as this would mean that your containers would inherit it after the build**

1. Add `ENV PYTHONUNBUFFERED 1` this forces the stdout and stderr streams to be unbuffered.

See more in this [explanation](https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file)

1. Install python 3.8.10 from [deadsnake ppa](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa):
    ```Dockerfile
    # Upgrade package list
    apt-get -y update
    #install required dependencies
    apt-get -y install software-properties-common
    # Add PPA to system's source list
    add-apt-repository ppa:deadsnakes/ppa
    # Upgrade package list to take into account new PPA
    apt-get -y update
    #install python 3.8
    apt-get install -y python3.8
    ```
1. Install pip
    ```Dockerfile
    apt-get install -y python3-pip
    ```
1. Install fastapi (0.78.0), SQLAlchemy (1.4.36), Alembic (1.7.7) and, uvicorn[standard] (0.17.6). Make sure to specify the selected versions.

1. Create `WORKDIR` app

1. Copy the complete current directory into the working directory `/server`

1. Exclude unnecessary files with `.dockerignore`
    ```markdown
    Dockerfile*
    makefile
    Readme.md
    .pytest*
    .venv
    ```
1. Expose the port 8000 to be able to access the server from outside of the container

1. Create an `ENTRYPOINT` for `uvicorn`

1. Create a `CMD` to run fastapi via uvicorn, listening on all interfaces on the host `0.0.0.0` and port `8000`

    ```Dockerfile
    app.main:app --host 0.0.0.0 --port 8000
    ```
1. Build the image using the tag `base-image-fastapi-ubuntu-fat:test`
    <details>
      <summary markdown='span'>💡 Hint</summary>

    We provided you with the `make buildTask1` command (cf `Makefile`)
    </details>

1. Run the container to make sure it’s functional -- it should start the fastapi server on the localhost interface and port 8000
    <details>
      <summary markdown='span'>💡 Hint</summary>

    Look at your `Makefile`, you should easily find a command to do so.
    </details>

1. Head to the [localhost:8000](http://localhost:8000) you should see `Hello World`.
    <details>
    <summary markdown='span'>💡 Hints</summary>

    If it doesn't work, check that you have forwarded the port from your VM to your local machine.
    <img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/port_forwarding_vs_code.png' width=400>
    </details>

1. Inspect the size and the layers using [dive](https://github.com/wagoodman/dive)

    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest base-image-fastapi-ubuntu-fat:test
    ```
1. Inspect the layers, check the image size, and check the wasted space.
    <details>
      <summary markdown='span'>💡 Hint</summary>

    You could save space deleting the files and directories in `/var/lib/apt/lists/`.
    </details>

1. Push the image to [Google Artifact Registry](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling)
    - Set the following variables in your terminal:
        ```bash
        LOCATION=europe-west1
        HOSTNAME="$LOCATION-docker.pkg.dev"
        PROJECT_ID=<INSERT_YOUR_GCP_PROJECT_ID_HERE>
        REPOSITORY=docker-hub
        IMAGE_NAME=base-image-fastapi-ubuntu-fat
        IMAGE_TAG=test
        ```
    - Retag the image with the registry name
        ```bash
        docker tag "$IMAGE_NAME:$IMAGE_TAG" "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"
        ```
    - Push the retagged image to the container registry
        ```bash
        docker push "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"
        ```
    - Check the image is present in the registry
        ```bash
        gcloud container images list-tags  "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME"
        ```
    <details>
      <summary markdown='span'>💡 Hints</summary>

    - Find your repo `LOCATION` with `cat ~/.docker/config.json`
    - Find your `PROJECT_ID` with `gcloud projects list`
    - Find your repo name with `gcloud artifacts repositories list`
    - Find your `IMAGE_NAME` and `IMAGE_TAG` with `Docker images`
    </details>

1. Shut down the server by using the shortcut `CTRL` + `c`

**Test your code with `make testTask1`**

# Caching - easy wins

This tasks illustrates the concept of caching and unwanted dependencies installed via regular commands. When doing a simple `apt install` or `pip install`, by default, those package managers install quantity of life dependencies to make any development work easy. To reduce the size of the Docker image, you can easily trim down the fat by installing **only** what's necessary and using as few layers as possible.

**❓ Refactor the Dockerfile from part 1 to save some space**

1. Copy the content of `Dockerfile-task-1` into `Dockerfile-task-2`

1. Refactor the `Dockerfile-task-2` to use a single layer to install your dependencies
    <details>
      <summary markdown='span'>💡 Hints</summary>

    Instead of running these 2 instructions separately:
    ```Dockerfile
    RUN apt-get -y update
    RUN apt-get -y upgrade
    ```
    You have to combine them into a single instruction:
    ```Dockerfile
    RUN apt-get -y update && apt-get -y upgrade
    ```
    You can also launch use `\ &&` to break up the instruction in several lines:
    ```Dockerfile
    RUN apt-get -y update \
        && apt-get -y upgrade
    ```
    </details>

1. Disable the installation of recommended packages when using `apt-get install` using the flag `--no-install-recommends` 👉 [apt documentation](https://manpages.ubuntu.com/manpages/xenial/man8/apt-get.8.html)

1. Disable the caching of packaging downloads and builds when using `pip install` with the flag `--no-cache-dir` 👉 [pip caching documentation](https://pip.pypa.io/en/stable/topics/caching/)

1. Clean up apt lists using the following command `rm -rf /var/lib/apt/lists/*`

1. Build the image using the tag `base-image-fastapi-ubuntu:test`
    <details>
      <summary markdown='span'>💡 Hint</summary>
        Use the Docker command or look at your `Makefile`, you should easily find a command to do so.
    </details>

1. Run the container to make sure it’s functional -- it should start the fastapi server listening on the localhost interface and the port 8000 - Head to [localhost:8000](http://localhost:3000). You should see `Hello World`

1. Inspect the size and layers with `dive`
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest base-image-fastapi-ubuntu:test
    ```
1. Inspect the layers, check the image size, and check the wasted space.

1. Push the image to the remote hub
    <details>
      <summary markdown='span'>💡 Hint</summary>
        Be careful, the image name differs from task 1
    </details>

**Test your code with `make testTask2`**

# The importance of a base image

This task elaborates on the concept of a base image and how it can be used in real-life scenarios to spin up images/containers easily and efficiently. Previously, we have installed our own version of python, pip and other dependencies. However, the community has already built many robust base images. Using the right base image can save time, space and often headaches.

**❓ Enhance the performance of your image**

1. Using the content of `Dockerfile-task-2`, do the following tasks in `Dockerfile-task-3-1`
1. Update the `Dockerfile-task-3` to use python:3.8.14 as a base image. You may need to remove some of the steps since your python and pip now come with automatically with your image.
1. We are going to use [poetry](https://python-poetry.org/) to handle all the dependencies and package-management for python instead of using the traditional `pip` and `requirements.txt`. To do so:
    1. Replace all the previously added pip packages running poetry in your terminal
        ```bash
        poetry add <package>
        ```
        This will generate 2 files `pyproject.toml` & `poetry.lock`, defining your dependency tree
        <details>
          <summary markdown='span'>ℹ️</summary>

        You should get a `No dependencies to install or update` message, because we already provide you with the 2 configuration files `pyproject.toml` & `poetry.lock` 👌.
        </details>
    1. Update the `RUN` command:
        ```Dockerfile
        #add the following lines
        pip install --no-cache-dir poetry
        poetry install --only main

        #Remove all of the manual python package installations via pip
        ```
        ☝️ `--only main` is equivalent to `--without dev` and skip `pyproject.toml` [tool.poetry.dev-dependencies] category
1. Change the `ENTRYPOINT` to use poetry
    ```Dockerfile
    poetry run
    ```
1. Change the `CMD` to
    ```Dockerfile
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
1. Build image using the tag `base-image-fastapi-fat:test`
1. Run the container to make sure it’s functional -- it should start the fastapi server listening on the localhost interface and port 8000 - Head to [localhost:8000](http:localhost:8000). You should see `Hello World`
1. Inspect the size and layers with `dive`
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <your_image_name:tag>
    ```
1. Inspect the layers, check the image size, and check the wasted space.

**Test your code with `make testTask3-1`**

---

**❓ Shrink your image size**

1. Copy the content of `Dockerfile-task-3-1` into `Dockerfile-task-3-2`
1. Now switch to the `python:3.8.14-slim` base image
1. Build the image using the tag `base-image-fastapi:dev`
1. Run the container to make sure it’s functional
1. Inspect the size and layers using dive
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <your_image_name:tag>
    ```
1. Inspect the layers, check the image size, check the wasted space.

**Test your code with `make testTask3-2`**

<br>

# Inspect what's inside a running container!

So far, we've been focusing on inspecting built **images** with dive.
Let's now *run* an image and inspect what's inside the running container!

- 🆚 Install [VS Code Docker extension](https://code.visualstudio.com/docs/containers/overview)
- Run your latest `base-image-fastapi:dev` image with interactive shell control:
```bash
docker run --rm -it -p 8000:8000 base-image-fastapi:dev /bin/bash
```
- Inspect your current working directory with `pwd`, and what's inside with `ls`. You should be able to find your local files copied inside the container!
- Create a new file `toto.py`. Check that it's there with `ls`, then use the VS Code Docker extension to navigate there too!
<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/docker_extension_vs_code.png" width=200>

- Now, exit the container (exit, or ctrl-D), so that the container is stopped (`Docker ps` is empty). Run your container again. This time, try to find `toto.py`.

It's gone! Containers are the running instances of `images` and they contain additional variables in memory only for the time that the container is running! You will soon see how to "persist" data inside the container...but before then, let's get to security!

# Improve security

This task will fix an issue you might have already seen when building your container.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/pip-root.png">

<br>

For pip, we don't mind ignoring this. Since we were running as the root user, everything has been working smoothly! It points us too a deeper issue though: **in general, when possible, it is better to run containers as a non-root user**. The isolation of containers is mostly broken with tools available only to the root user, so to maximise security, non-root is better wherever possible!

**❓ Make you image non-root**

1. Copy the content of `Dockerfile-task-3-2` into `Dockerfile-nonroot`
1. Update your `Dockerfile` with the following guide:

```Dockerfile
RUN ...
    ...
    # ❗️ We create a user called `"runner"`, with id `10000`
    && useradd --uid 10000 -ms /bin/bash runner

# ❗️ We want to work inside the user local folder now
WORKDIR /home/runner/server

# ❗️ We swap from root to that user
USER 10000

# ❗️ We make sure that the user's files are on the path
ENV PATH="${PATH}:/home/runner/.local/bin"

COPY ./  ./

# Now, we will be running pip to install packages for the user non-root!
RUN pip install ...
```

❓ Build the image using the tag `nonroot-image-fastapi:dev` and run the container to make sure it’s functional.

👉 This time, you shouldn't be able to `touch` any file when running it with /bin/bash as we did previously. And you don't have sudo access anymore either, which is exactly what we wanted! Our set up is now more secure and follows the best practices.


# 🏁 Congratulations for completing the challenge!
- Run the final `make test`
- Save your work on GitHub even if you aren't completely finished so we can track your progress


# Some cool tools (to keep for later)!

✨ [Haskell Dockerfile Linter](https://github.com/hadolint/hadolint)

🛠 [Container Structure Tests](https://github.com/GoogleContainerTools/container-structure-test)

🤿 [dive](https://github.com/wagoodman/dive)

🍰 [Dockerfile parsing API](https://github.com/asottile/dockerfile)
