# 🎯 Goal

Docker is the most common tool for containerisation and will be used heavily for the rest of this bootcamp. Being familiar with the basic usage will greatly enhance your learning experience for future units!

The purpose of this exercise is to:

- Guide you through common `docker` CLI commands - with some details and associated Docker concepts
- Starting, stopping, and cleaning up containers
- Executing commands inside running containers

If your familiar with Docker already this challenge might be relatively straightforward, but you can never have too much practice in the basics!

<br>

# 1️⃣ Docker Hub 💻

#### Sign up
Docker Hub is a hosted repository service provided by Docker for finding and sharing container images with your team. Once you create a Docker ID (a user), you will be able to pull and push images to the Hub.

Create a personal account 👉  [here](https://hub.docker.com/signup).

#### Login

Open a terminal and type:

```bash
docker login
```

You will be prompted for your username and password:
<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/docker-login.png?raw=true" width="500"></p>

When successful, your terminal should tell you "Login Succeeded" 🙌!

<br>

# 2️⃣ Hello world!

Let's validate our Docker installation by running our first container: `hello-world`. To do so, run the following in your terminal:

```bash
docker run hello-world
```

You should have run this image during Setup Day to verify your docker install, if not it will:

- It will first pull the `hello-world` image from docker hub. If the image exists on your host it will use the existing image.
- Then run a container from this image

This container _only_ prints a message

```bash
Hello from Docker!
```

#### To see the containers that are running on your VM:

```bash
docker ps
```

Not seeing anything? That's normal!
Your `hello-world` container is not running any more: it exited as soon as it was done. Its job was simply to print a message.

But what about viewing all containers? The `docker ps` command has flags to change the output!

#### To view all containers (even non-running ones), run:

```bash
docker ps -a
```

You should see a container here. What is its name? Which image was used to run it? What is its state?

#### To view images on your VM:

```bash
docker images
```

You should your `hello-world` image. This command will also show other details such as:

- Image ID
- Image tag - used to convey information about the image, typically the version for pulled images like postgres. If no tag is specified when an image is built it will default to _latest_
- Image size
- When the image was created (built). This is different from when you pulled an image from a remote repository.

<br>

# 3️⃣ Common Docker commands

#### Run a container

The [**`docker run`**](https://docs.docker.com/engine/reference/run/) command is used to run a container from an image. You should pass the image name to it:

```bash
docker run <SOME_IMAGE>
```

- Docker will use the image from the VM if it exists
- If the image is not present in the VM it will go to Docker Hub and pull the image for you 👌

👉 For instance, run a container from the `postgres` image. You can see [here](https://hub.docker.com/_/postgres) that the postgres image is available on the Hub!

```bash
docker run postgres
```

This will break...👇

```bash
Error: Database is uninitialized and superuser password is not specified.
   You must specify POSTGRES_PASSWORD to a non-empty value for the
   superuser. For example, "-e POSTGRES_PASSWORD=password" on "docker run".
```

👉 Check the error message. Try to fix your command and run it again!

The `-e` flag in `docker run -e ...` stands for *environment variable*. Using the appropriate flag and arguments we created a password for the database superuser and passed it to the `docker run` command.

🍾 That's it! **No need for a complex installer, no conflicts on your laptop, no long hours scrolling tech forums to fix your problem**. You have a running database with a single command. Running a database locally is relatively stable when using a virtual machine. But often you want to use a database without having to set up a whole new machine just for that. Docker can help!

Try the previous `docker run ...` command with the additional flag and you should see an output in your terminal: it looks like your database is initialized and ready to accept connections!

👉 Stop the container by hitting `ctrl + c`.

#### Run a container in the background

Another thing you can do is to run a container in the background (using the "detached" mode). This way, your terminal prompt will be available.

👉 Try to run a new postgres container in the detached mode and give it a name: `pg`. `docker run --help` or `tldr docker run` are your best friends!

<details>
<summary markdown='span'>💡 solution</summary>

```bash
docker run -d -e POSTGRES_PASSWORD=password --name=pg postgres
```
</details>

You should now see it running in `docker ps`.

💡 If you don't specify a name for a container, Docker will generate random name for it!

#### Access the Postgres database

Now that your container is running, you might want to run an SQL query.
Let's first get a bash shell in the container with the following command:

```bash
docker exec -it pg /bin/bash
```

What have we done here 🤔? We have asked Docker to run a command (`/bin/bash`: to get a bash shell) in the container, passing the flags:
- `-i` flag for "interactive" mode: this flag provides us with a standard input **stdin**. By default, a container runs in a non-interactive mode: it does not listen for input from your side. To provide an input, you need to pass this `-i` flag.
- `-t` flag stands for **tty**, a Unix-like operating system command. This flag provides a terminal interface.

The combination of these two flags give us access to a "terminal" inside the container 🎉

We can now access our DB using the `psql` CLI:

```bash
psql --username postgres
```

You should now be on the Postgresql command line where you can interact with the database and write SQL queries. Here's a few to test out, don't forget the `;` at the end of the query!

```sql
SELECT 1 + 1 as test;
```

```sql
SELECT current_user;
```

<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/psql-docker.png?raw=true" width="500"></p>


To navigate back to your Virtual Machine's terminal:
- Exit `psql` prompt: `\q` + **Enter**
- Exit container bash shell: `exit` + **Enter**

<br>

# 4️⃣ Clean up 🧹

#### Stopping and removing containers

To stop a container use the [`docker stop`](https://docs.docker.com/engine/reference/commandline/stop/) command. You will need to pass the container ID or the container name.

To stop your `pg` container:

```bash
docker stop <CONTAINER_ID>
```

Now list running and exited containers:

```bash
docker ps
docker ps --filter "status=exited"
```

You should see that your container changed its state from `running` to `exited` but it is still there! To remove it from your VM run the `docker rm` command:

```bash
docker rm pg
```

#### Removing an image

So you have stopped and removed your postgres container but how about the postgres image that your VM initially pulled from Docker Hub?

Do you remember how to list docker images?

<details>
<summary markdown='span'>🎁 Solution (after trying yourself!)</summary>

```bash
docker images
```

</details>

Try to remove the `postgres` image using [`docker rmi`](https://docs.docker.com/engine/reference/commandline/rmi/) and double check it worked.

<details>
<summary markdown='span'>🎁 Solution (after trying yourself!)</summary>

```bash
docker rmi postgres
docker images
```
</details>

If you have other containers using the `postgres` image, you will not be able to remove it... You need to get rid of the containers first!

#### Cheatsheet: docker cleaning

```bash
# Containers
docker stop $(docker ps -q) # Stop all running containers
docker container prune # Remove all stopped containers

# Images
docker rmi image_name

# Big Clean: Remove container & images
docker system prune
```

<br>

# 🏁 Finish

Congratulation on finishing! The commands you went through in this challenge are key to working with Docker and you'll be using them frequently throughout the rest of the bootcamp.

🧪 Run `make test`, commit the `test_output.txt`, and push it up to github so Kitt can track your progress!

<br>
