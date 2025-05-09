# Big data - Live code

Break down an application with 2 endpoints

- one with a lot of traffic
- one with a lot less traffic

by decoupling the monolith into two separate applications, allocating different resources to each application using CloudRun.

We'll do an overview of the GCP services that can be useful when scaling up.

- Cloud CDN
- Kubernetes
- Functions
- API Gateway
- Load balancing

We can use resources like this [AWS article, Break a Monolith Application into Microservices](https://aws.amazon.com/getting-started/hands-on/break-monolith-app-microservices-ecs-docker-ec2/module-four/).


## Different stages of our app

- 10 users, running one computation every now and then
  - Show how to split the code
- Introducing simulations, we can run 100 computations concurrently (introduce Cloud Run and break out the monolith)
  - Break the monolith into two apps
  - Introduce Cloud Run
- Introducing "faster simulation" with a GPU (add a queue)
  - GPU resources are scarce
  - Add a queue
- Give access to our database as a service (break out monolith and scale out Postgres)
  - One more breakout of the app / 100s of calls per second on a given endpoint
  - Scale out Postgres read-only


## Final picture

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/Day9-Recap.drawio.png" width=600 />

<br>

# Extra fun project to review

Check out [Hugging Face Datasets Server](https://github.com/huggingface/datasets-server) project.

__This has been written on October 6th 2022, so if the code structure changed when you read this, make sure to navigate to the right commit.__

Microservices under `/services`:
- `admin`
- `api`
- `reverse-proxy`
- `worker`

Comment on:
- Their structure, always a `pypoetry.toml`, `Dockerfile`, `Makefile`, `README.md` that documents the endpoints and environment variables.
- `/api/pyproject.toml` uses `starlette` (`FastAPI` built on top of it) and `uvicorn`.
- `/worker/pyproject.toml` uses `apache-beam` and `aiohttp`, so we're talking asynchronous programming and Beam magic.

Then check out the Kubernetes YAML structure under `chart/values.yaml`.
