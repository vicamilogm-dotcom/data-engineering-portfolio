# 🎯 Goal

We have a working API that is exposed to the world! But if we wanted to update the API with a new endpoint or a bugfix, we would have to manually re-deploy it on GCP Cloud Run - not ideal. We can use the skills we learnt in a previous module and use Github Actions to set up Continuous Integration with tests to check our API works and Continuous Deployment on GCP Cloud Run so that whenever an update is pushed to our main branch, the deployment onto Cloud Run is automatic!

<br>

# 0️⃣ Setup

To achieve this we'll need a bit of setup:

1. Duplicate the previous challenge to a new repo outside of the `data-engineering-challenges` directory on your Virtual Machine.
1. Initialize the copied directory with git, create a new github repository and push all of the code up to github!

<br>

# 1️⃣ Continuous Deployment with Cloud Run

We can set up Continuous Deployment on Cloud Run through the GCP Console. Under the hood, GCP will use [Cloud Build](https://cloud.google.com/build?hl=en) to manage the deployment of updates.

To set up, go to your Cloud Run service:

1. Cloud run service click setup continuous deployment

    <img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/cloud-run-service.png">

1. Select your repo

    <img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/cloud-run-select-repo.png" width=500>

1. Select the branch you want to deploy and the name of your dockefile

    <img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/cloud-run-build-config.png" width=500>

1. Go to the code and make a change to the response of the API

1. Push the code and go and view your repo and you will see the ci/cd pipeline in action automatically as an action!

    <img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/repo-action.png">

And done! 🎉

Cloud Run and Cloud Build offer some safeguards against deploying broken containers:
- Cloud Build: Compiles your source code and builds the Docker image. If the build process fails, it stops there, preventing a faulty image from being pushed.
- Cloud Run: Only deploys successfully built containers. If a container fails to start, it won't replace the currently running version, maintaining uptime.

Both mechanisms offer a safety net by ensuring only functional containers make it to production, even in the absence of a full-fledged CI system.

We want to be robust through so lets setup CI!

<br>

# 2️⃣ Setting up ci

We can create a CI action using Github Actions. We've created a template for you to use, read through it and understand what each part of the CI action is doing. If you can't remember where to put the template, have a look at your previous challenges for reference.

```yml
name: FastAPI CI and Lint

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Run Hadolint
      uses: hadolint/hadolint-action@v1.5.0
      with:
        dockerfile: Dockerfile

  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Build Docker image
      run: docker build -t my_fastapi_app .

    - name: Run Docker container
      run: docker run --name test_container -d -p 8000:8000 -e PORT=8000 my_fastapi_app

    - name: Wait for FastAPI to start
      run: sleep 10

    - name: Test API
      run: curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep 200

    - name: Save Docker image
      run: docker save my_fastapi_app:latest > my_fastapi_app.tar

    - name: Upload Docker image as artifact
      uses: actions/upload-artifact@v2
      with:
        name: my_fastapi_app
        path: my_fastapi_app.tar

  security-scan:
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
    - name: Download Docker image from artifact
      uses: actions/download-artifact@v2
      with:
        name: my_fastapi_app

    - name: Load Docker image
      run: docker load < my_fastapi_app.tar

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'my_fastapi_app:latest'
        format: 'table'
        exit-code: '1'
```

Try to add and push the action. Does something break?

Fix it and checkout the output of the actions!

They will probably fail but give interesting insights in improving your containers!

<br>

# 3️⃣ (Optional) Advanced CD

Sometimes you don't want Cloud Build to automatically build and deploy the containers but you do want it build and push the image to the Artifact Registry.

If you checkout [this github gist](https://gist.github.com/palewire/12c4b2b974ef735d22da7493cf7f4d37) you can attempt to do just that but it gets a little tricky!

<br>

# 🏁 Finishing up

If you've made it this far - congratulations 🎉

In these challenges you've learnt the foundations of Docker and how to use it for creating a microservice.

Although we used a really simple API that returned a static JSON object, you can apply the principles we've done here to many different use cases:
- You could build an API as a small, basic data pipeline that ingests data, cleans it, then loads it into a data lake or data warehouse.
- Build an API to interact with a database that is hosted on your VM, another server or on a managed cloud service - functionally how a lot of the web works.
- For machine learning workloads, you can package a model and supporting data preprocessing code into an API to so that it takes model inputs, pre-processes the data, perform inference, and return an output.

<br>
