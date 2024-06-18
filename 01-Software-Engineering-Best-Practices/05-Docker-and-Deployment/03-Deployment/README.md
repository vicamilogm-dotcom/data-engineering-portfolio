# 🎯 Goal

We want to deploy our API inside our container to cloud run so that anybody can access it! [Cloud Run](https://cloud.google.com/run?hl=en) on GCP allows you to deploy containerized applications in a fully managed environment. You package your code in a Docker container, upload it to GCP, and Cloud Run handles scaling, load balancing, and HTTPS. It abstracts away infrastructure management letting you focus on code.

<br>

# 1️⃣ Deployment

1. Setup your `.env` here you can duplicate the `.env.example` and rename it to `.env` and fill in the `DOCKER_IMAGE_NAME`! Pick a name which pushes to the artifact registry you setup before!

2. Setup the makefile with the following commands:
    ```makefile
    build_docker_image:
        build the container using DOCKER_IMAGE_NAME

    run_docker_image:
        run the container using DOCKER_IMAGE_NAME

    push_docker_image:
        push the container using DOCKER_IMAGE_NAME
    ```
    For run_docker_image make sure you can access the API locally on localhost:8000!

3. On a Cloud Run deployment we can't hardcode the port. You will need to add a `PORT` variable to the `.env` file and use it in the Dockerfile! Don't forget to update the `RUN` command in the makefile to use the `PORT` variable! Passing it as an environment variable in the run command.

    <details>
    <summary markdown='span'>💡 Solution</summary>

    In `makefile`:
    ```makefile
    -e PORT=$(PORT)
    ```

    In `dockerfile`:
    ```
    CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
    ```
    </details>

4. Add one last command to the makefile:
    ```makefile
    deploy_docker_image:
        deploy
    ```

Using the [Cloud Run documentation](https://cloud.google.com/sdk/gcloud/reference/run/deploy) make sure to allow unauthenticated invocations so you can access your class mates API's!

<br>

# 🏁 Finished

We have now set up a very basic deployment! But we want to add CI/CD in our next exercise in order to maintain best practices!

<br>
