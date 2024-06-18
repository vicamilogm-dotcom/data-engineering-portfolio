# 🎯 Goal

Docker has some advanced features that can be used in conjunction with compiled languages that can produce some very small images. Let's explore multi-stage builds and how they work.

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

You might have to manually forward port 8080 on VSCode.

Let's explore the image with dive!

```bash
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest single-stage
```

Now, let's see what benefits we get with a multistage build!

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

You might have to manually forward port 8080 on VSCode.

Once you've verified that it works the same, dive in and explore the image!

```bash
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest multi-stage
```

Have a look at the image sizes and compare the differences!

The size is massively smaller because after we compile the code with the Go tool-chain, it can be discarded entirely, leaving us with just the executable binary file.

# 🏁 Finishing up

This is quite an extreme example. But you should be able to see the efficiency gains when of using a multi-stage Docker build when using a compiled language like Go, Rust, or C++

Multi-stage builds are tricky to implement in python because it is an interpreted language. The gains made are small, prone to creating complex errors, and generally not worth the effort.

Multi-stage builds also add some additional complexity when building micro-services as well. They are significantly harder to debug and when you look inside the container, it will only contain the binary that was created from the first stage of the build.

<br>
