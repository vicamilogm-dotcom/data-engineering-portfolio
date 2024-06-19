# 🎯 Goal

Docker has some advanced features that can be used in conjunction with compiled languages that can produce some very small images. Let's explore multi-stage builds and how they work.

In this example is a program written in `Golang`, a compiled language that is popular for writing API's.

<br>

# 1️⃣ Build a single-stage image

First, run:

```bash
docker build -f Dockerfile-single-stage -t single-stage .
```

This image builds an API which runs on port 8080. We can run it with:

```bash
docker run -p 8080:8080 single-stage
```

❗ You might have to manually forward port 8080 from your Virtual Machine to your local computer on VSCode. Gin, the package used to build API's in Go, doesn't log to stdout that the API is active so VSCode may not automatically port forward.

Let's explore the image with dive!

```bash
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest single-stage
```

That image size is large! It includes the Golang `tool-chain`, the necessary tools required to compile `.go` files into an executable machine code binary.

Now let's see what benefits we get with a multistage build!

<br>

# 2️⃣ Build a multi-stage image

Build your multi-stage image:

```bash
docker build -f Dockerfile-multi-stage -t multi-stage .
```

Run it and access it on port 8080.

```bash
docker run -p 8080:8080 multi-stage
```

❗ You might have to manually forward port 8080 from your Virtual Machine to your local computer on VSCode. Gin, the package used to build API's in Go, doesn't log to stdout that the API is active so VSCode may not automatically port forward.

Once you've verified that it works the same was as the single-stage container, dive in and explore the image!

```bash
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest multi-stage
```

Have a look at the image size and compare the differences!

The size is massively smaller because after we compile the code with the Go `tool-chain` it can be discarded entirely, leaving us with just the executable binary file that is executed in a [`scratch`](https://hub.docker.com/_/scratch) base image.

# 🏁 Finishing up

This is quite an extreme example. But you should be able to see the efficiency gains of using a multi-stage Docker build when using a compiled language like Go, Rust, or the C family of languages. There are some other benefits, like enhanced security, by excluding unnecessary tools and dependencies, the attack surface is minimised.

Multi-stage builds are tricky to implement in python because it is an interpreted language. The gains made are small, prone to creating complex errors.

Multi-stage builds also add some additional complexity when building micro-services as well:
- They have to be built iteratively, stage by stage.
- Can be harder to debug and when you look inside the container, it will only contain files copied from the previous stage of the build.
- Potential for longer build times.

Generally, follow the software development flow of **make it work, make it right, make it fast**.

<br>
