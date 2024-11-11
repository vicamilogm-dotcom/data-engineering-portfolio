
# Kubernetes lecture

If you want to rebuild the lecture image, here are the ressources for `europe-west1-docker.pkg.dev/data-engineering-students/student-images/k8s-lecture-app:dev`

## Dockerfile

``` bash
FROM python:3.8.14-buster

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn

COPY main.py main.py

RUN mkdir pv-data

CMD uvicorn main:app --host 0.0.0.0 --port 8080
```

## main.py

``` python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    try:
        with open("/app/pv-data/count.txt", "r+") as f:
            data = f.read()
            x = int(data) + 1
            f.seek(0)
            f.write(str(x))
            f.truncate()
    except FileNotFoundError:
        with open("/app/pv-data/count.txt", "w") as f:
            x = 1
            f.write(str(x))
    return {"Read": f"{x} times"}
```

## Makefile

``` bash
GCP_PROJECT_ID=le-wagon-data
DOCKER_IMAGE=pv-count
GCP_REGION=europe-west1
DOCKER_REPO=my-first-repo
DOCKER_REPO_DESCRIPTION=First repo
VERSION=0.3

ARTIFACT_IMAGE=${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${DOCKER_REPO}/${DOCKER_IMAGE}:${VERSION}

build:
	docker build -t api .

explore:
	docker run -it api sh

run:
	docker run -p 8000:8080 api

create_artifacts_repo:
	gcloud artifacts repositories create ${DOCKER_REPO} \
		--repository-format=docker \
		--location=${GCP_REGION} \
		--description="${DOCKER_REPO_DESCRIPTION}"

build_artifact:
	docker build -t ${ARTIFACT_IMAGE} .

run_artifact:
	docker run -p 8000:8080 ${ARTIFACT_IMAGE}

push_artifact:
	docker push ${ARTIFACT_IMAGE}
```

# Kubernetes recap options

## Helm challenge port forward

Do the challenge as per instructions.

To access the Airflow GUI, look for the deployed service:

``` bash
kubectl get services
```

Expose Airflow UI:

``` bash
kubectl port-forward svc/airflow-cluster-web 8080:8080 --namespace airflow
```

## k9s

Optionally demo the [k9s](https://k9scli.io/) 🔗 cli tool allowing to manage cluster ressources

### Install on vm

Install [brew](https://brew.sh/) 🔗 on ubuntu:

``` bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install k9s:

``` bash
brew install k9s
```

Usage:

``` bash
k9s
```

### Ressources

``` bash
Ctrl A              show all available ressources

:ctx                show contexts
:ns                 show namespaces
:node               show nodes
:pod                show pods
:svc                show services
:pvc                show persistent volume claims
:secret             show secrets
:configmap          show configmaps

:ingress            show ingresses
:helm               show releases

:pulse              show cluster dashboard
```

### Navigation

``` bash
:q                  quit

⬆️⬇️                navigate list of ressources
Enter               navigate ressources items:
                    for example when viewing a node: `node` → `pod` → `container` → `logs`

y                   show yaml definition of ressource
s                   attach a shell when viewing a pod or a container
```
