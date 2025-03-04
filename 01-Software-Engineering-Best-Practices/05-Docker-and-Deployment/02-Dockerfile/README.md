# 🎯 Goal and Context

As data engineers, creating services and containerised applications is key to ensure portability, scalability, and deployment on different computers. By using a tool like docker to package and deploy your code, anyone that uses your container will be able to run it without any issues. Creating clean and extensible Docker images will also help DevOps engineers downstream as they run and test them inside CI/CD systems or in production (like in Docker Swarm, virtual instances, Kubernetes).

This exercise will teach you the Docker fundamentals necessary to mount and operate a Docker container.
You will learn to:
- Create a `Dockerfile` based on best practices
- Build and tag a Docker image
- Analyse the content and construction of a Docker image
- Spin containers up and down
- Access containers and execute commands inside them with the CLI
- Push images to remote Docker hubs (DockerHub, GCP Artifact Registry)

For this challenge you'll use a very basic API that's been created using FastAPI. Feel free to have a look at the contents of `app/` and review the code.

<br>

# 1️⃣ Layers

This section illustrates the concept of layers. We will write a bad Dockerfile on purpose to highlight the internal structure of an image.

Open this challenge in VSCode and head to the `Dockerfile-task-1` file. This will be your Dockerfile for this part of the challenge.

#### ❓ Write code in the Dockerfile to meet the following requirements:

1. Based on ubuntu 20.04

1. Add `ARG DEBIAN_FRONTEND=noninteractive`

    *note:* **Do not use ENV as this would mean that your containers would inherit it after the build**

1. Add `ENV PYTHONUNBUFFERED=1` - this forces the `stdout` and `stderr` streams to be unbuffered. Read more about why we set this environment variable in [this stack overflow post](https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file).

1. Install python 3.12.8 from [deadsnake ppa](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa):
    ```Dockerfile
    # Upgrade package list
    apt-get -y update
    #install required dependencies
    apt-get -y install software-properties-common
    # Add PPA to system's source list
    add-apt-repository ppa:deadsnakes/ppa
    # Upgrade package list to take into account new PPA
    apt-get -y update
    #install python 3.12
    apt-get install -y python3.12
    ```

1. Install pip
    ```Dockerfile
    apt-get install -y python3-pip
    ```

1. Install fastapi (0.115.6) and uvicorn (0.33.0). Make sure to specify the selected versions.

1. Create a `WORKDIR` named: `app`

1. Copy the complete current directory into the working directory `/app`

1. Exclude unnecessary files with `.dockerignore`
    ```bash
    Dockerfile*
    makefile
    Readme.md
    .pytest*
    .venv
    ```
1. Expose port 8000

1. Create an `ENTRYPOINT` for `uvicorn`

1. Create a `CMD` to run FastAPI via uvicorn, listening on all interfaces on the host `0.0.0.0` and port `8000`
    ```Dockerfile
    app.main:app --host 0.0.0.0 --port 8000
    ```

1. Build the image using the tag `base-image-fastapi-ubuntu-fat:test`
    <details>
    <summary markdown='span'>💡 Hint</summary>
    Have a look at the `makefile` - We have provided you with some useful commands!
    </details>

1. Run the container to make sure it’s functional. It should start the fastapi server on the localhost interface and port 8000
    <details>
    <summary markdown='span'>💡 Hint</summary>
    Look at your `makefile` - you should find a command to run the container.
    </details>

1. Head to [localhost:8000](http://localhost:8000) in your web browser. You should see `Hello World`.
    <details>
    <summary markdown='span'>💡 Hints</summary>
    If it doesn't work, check that you have forwarded the port from your host to your local machine.
    <img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/port_forwarding_vs_code.png' width=400>
    </details>

1. Inspect the size and the layers using [dive](https://github.com/wagoodman/dive)
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest base-image-fastapi-ubuntu-fat:test
    ```

1. Inspect the layers, check the image size, and check folders that are taking up a large amount of space that can be removed.
    <details>
    <summary markdown='span'>💡 Hint</summary>
    You could save space deleting the files and directories in `/var/lib/apt/lists/`.

    Read more on why this is safe to delete on [this stack overflow post](https://askubuntu.com/questions/179955/var-lib-apt-lists-is-huge).
    </details>

1. Push the image to [Google Artifact Registry](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling)
    - Set the following variables in your terminal:
        ```bash
        LOCATION=europe-west1
        HOSTNAME="$LOCATION-docker.pkg.dev"
        PROJECT_ID=<YOUR_GCP_PROJECT_ID>
        REPOSITORY=docker-hub
        IMAGE_NAME=base-image-fastapi-ubuntu-fat
        IMAGE_TAG=test
        ```
    - Re-tag the image with the registry name:
        ```bash
        docker tag "$IMAGE_NAME:$IMAGE_TAG" "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"
        ```
    - Push the re-tagged image to Container Registry:
        ```bash
        docker push "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"
        ```
    - Check the image is present in GCP Container Registry:
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

1. Shut down the uvicorn server by using the shortcut `ctrl + c`

Woah, that was a fair chunk of tasks! Lets see how we can improve our Docker image!

🧪 Test your code with `make testTask1`

<br>

# 2️⃣ Caching - easy wins

This tasks illustrates the concept of caching and unwanted dependencies installed via regular commands. When doing a simple `apt install` or `pip install`, by default those package managers install quality of life dependencies to make any development work on the installed package easier. To reduce the size of the Docker image you can easily trim down your image size by installing **only** what is necessary and using as few layers as possible.

#### ❓ Refactor the Dockerfile from Part 1 to reduce image size

1. Copy the content of `Dockerfile-task-1` into `Dockerfile-task-2`

1. Refactor the `Dockerfile-task-2` to use a single layer to install your dependencies
    <details>
    <summary markdown='span'>💡 Hints</summary>
    Instead of running these two instructions separately:
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

1. Clean up apt lists adding the following command `rm -rf /var/lib/apt/lists/*`

1. Build the image using the tag `base-image-fastapi-ubuntu:test`
    <details>
    <summary markdown='span'>💡 Hint</summary>
    Use the Docker command or look at your `makefile`, you should find a command to build your image.
    </details>

1. Run the container to make sure it’s functional. It should start the fastapi server listening on localhost, port 8000. Head to [localhost:8000](http://localhost:3000). You should see `Hello World`.

1. Inspect the images size and layers with `dive`
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest base-image-fastapi-ubuntu:test
    ```

1. Inspect the layers, check the image size, and check for wasted space.

1. Push the image to the remote hub
    <details>
    <summary markdown='span'>💡 Hint</summary>
    Be careful, the image name differs from task 1
    </details>

That should have cut down on the size of the image pretty considerably! But it was still a decent amount of work to build this image starting from just an ubuntu image. Next we will look at how using the appropriate `base image` can speed up the development cycle.

🧪 Test your code with `make testTask2`

<br>

# 3️⃣ The importance of a base image

This task elaborates on the concept of a base image and how it can be used in real-life scenarios when creating your own images and spinning up containers easily and efficiently. Previously we have installed our own version of python, pip, and other dependencies from an ubuntu base image. However the community has already built many robust base images that we can use as a starting point. Using the right base image can save time, space, and often headaches.

## 3.1. Enhance the performance of your image

1. Using the content of `Dockerfile-task-2`, do the following tasks in `Dockerfile-task-3-1`
1. Update the `Dockerfile-task-3` to use **python:3.12.8** as a base image. You may need to remove some of the steps since python and pip now come automatically with the base image.
1. We are going to use [poetry](https://python-poetry.org/) to handle all the dependencies and package-management for python instead of using the traditional `pip` and `requirements.txt`. To do so:
    1. Replace all the previously added pip packages by running the poetry command in your terminal:
        ```bash
        poetry add <package>
        ```
        This will generate two files: `pyproject.toml` and `poetry.lock` that define your projects dependencies.
        <details>
        <summary markdown='span'>❗ But nothing happened!</summary>
        You should get a `No dependencies to install or update` message because we have already provide you with the two poetry configuration files `pyproject.toml` and `poetry.lock` 👌
        </details>
    1. Update the `RUN` instruction:
        ```Dockerfile
        #add the following lines
        pip install --no-cache-dir poetry
        poetry install --only main

        #Remove all of the manual python package installations via pip
        ```
        ☝️ `--only main` is equivalent to `--without dev` and skips the `[tool.poetry.group.dev.dependencies]` section in your **pyproject.toml**
1. Change the `ENTRYPOINT` to use poetry:
    ```Dockerfile
    poetry run
    ```
1. Change the `CMD` instruction to:
    ```Dockerfile
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
1. Build image using the tag `base-image-fastapi-fat:test`
1. Run the container to make sure it’s functional. It should start the fastapi server listening on localhost, port 8000. Head to [localhost:8000](http://localhost:3000). You should see `Hello World`.
1. Inspect the images size and layers with `dive`:
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <your_image_name:tag>
    ```
1. Inspect the layers, check the image size, and check for wasted space.

That's simplified our Dockerfile but the size of the image is now way higher! Let's look at slimming it down a bit.

🧪 Test your code with `make testTask3-1`

## 3.2. Shrink your image size

There are can be multiple different types of base images depending on the application that you are building. Let's look at a slimmer python image.

1. Copy the content of `Dockerfile-task-3-1` into `Dockerfile-task-3-2`
1. Now switch to the `python:3.12.8-slim` base image
1. Build the image using the tag `base-image-fastapi:dev`
1. Run the container to make sure it’s functional
1. Inspect the size and layers using `dive`:
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <your_image_name:tag>
    ```
1. Inspect the layers, check the image size, check for wasted space.

That has massively shrunk our image size down from the previous iteration, but it might still be higher than the image we build using just Ubuntu. There will always be trade offs in software development, by using a pre-made python base image and poetry we can greatly reduce the development cycle and increase the portability of our code from local to container environment.

For more complex applications, especially where dependency resolution can be a pain, using a base image that someone else has already done the work for can make life easier.

If the app was going into long term production you could investigate further efficiencies with size and building from a lower abstraction base image, like an ubuntu base image instead of a python base image.

🧪 Test your code with `make testTask3-2`

<br>

# 4️⃣ Inspect what is inside a running container!

So far we've been focusing on inspecting built **images** with dive.
Let's now *run* an image and inspect what's inside the running container!

- Install the [VS Code Docker extension](https://code.visualstudio.com/docs/containers/overview)
- Run your latest `base-image-fastapi:dev` image with an interactive shell:
    ```bash
    docker run --rm -it -p 8000:8000 base-image-fastapi:dev /bin/bash
    ```
- Inspect your current working directory with `pwd` and its contents with `ls`. You should be able to find your local files copied inside the container!
- Create a new file `toto.py`. Check that it is there with `ls`, then use the VS Code Docker extension to navigate there too!
    <img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/docker_extension_vs_code.png" width=200>

- Now exit the container (`exit`, or `ctrl + d`) so that the container is stopped (`Docker ps` is empty). Run your container again. Now try to find `toto.py`.

It's gone! Containers are the running instances of `images` and they contain additional variables in memory that only exist for the time that the container is running! You will soon see how to "persist" data inside the container, but before then let's get to security!

<br>

# 5️⃣ Improve security

This task will fix an issue you might have already seen when building your container.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/pip-root.png">

<br>

For pip, we don't mind ignoring this. Since we were running as the root user everything has been working smoothly! It points us too a deeper issue though: **in general, when possible, it is better to run containers as a non-root user**. The isolation of containers is mostly broken with tools available only to the root user. So to maximise security non-root is better wherever possible!

This idea is called the [Principle of Least Privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege). Something we should always have in mind.

#### ❓ Make you image non-root

1. Copy the content of `Dockerfile-task-3-2` into `Dockerfile-nonroot`
1. Update your `Dockerfile` with the following:

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

👉 This time, you shouldn't be able to `touch` any file inside the container with `/bin/bash` like we did previously. You don't have `sudo` access any more either which is exactly what we wanted! Our set up is now more secure and follows best practice.

<br>

# 🏁 Finish

Congratulations on completing the challenge!

In this challenge we went through the fundamentals of creating and managing docker images, how to reduce image size, and optimising the developer experience!

🧪 Run a final `make test` to check all your `Dockerfile`'s

Make sure to commit and push to github so Kitt can track your progress!

#### Some cool tools (to keep for later)!

✨ [Haskell Dockerfile Linter](https://github.com/hadolint/hadolint)

🛠 [Container Structure Tests](https://github.com/GoogleContainerTools/container-structure-test)

🤿 [dive](https://github.com/wagoodman/dive)

🍰 [Dockerfile parsing API](https://github.com/asottile/dockerfile)

<br>
