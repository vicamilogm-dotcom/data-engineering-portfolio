# 🎯 Dask on K8s

The goal is to distribute computation across multiple machines by leveraging **Dask** with **k8s**.

**Dask** is a parallel computing library in Python that enables distributed computing and is designed to integrate seamlessly with **NumPy**, **Pandas**, and **scikit-learn**. It allows you to scale from a single machine to a cluster.

We will be able to process over **1,000,000,000** cells of New York taxi data in around **10 seconds** 💪

- That would never fit in your personal machine RAM memory 🤯
- That would take ages on your personal machine CPU 🤯

❗ If you start this challenge but do not finish - there are tear down instructions at the end. Make sure you tear down your cluster to avoid an unwanted bill 💸

<br>

# 0️⃣ Before we start

## Python version

The Python version on the cluster is controlled by the Dask helm chart, and they are quite low (3.8 or 3.9). It is possible to create our own Docker images and other Kubernetes configuration files to upgrade to 3.12, but to keep this as simple as possible, we're just going to downgrade our local python version to 3.8.14

To do this locally, make sure you're in the current challenge directory and run:

```bash
pyenv install 3.8.14
```

Locally set the python version in this challenge directory:

```bash
# Will create a .python-version text file
pyenv local 3.8.14
```

## Install the GKE auth plugin

Install the `gke-gcloud-auth-plugin` if not done yet. Normally you did this already in the Kubernetes unit, but you can safely run this a second time.

<details>
<summary markdown='span'>Installation instructions</summary>

We need this extension to help us interact via kubectl -> gke

```bash
gcloud components install gke-gcloud-auth-plugin
```

If the Google Cloud CLI was installed with a package manager, this simple command might not work.

In that case, we have to install manually. Run this:

```bash
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor --yes -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin
```

</details>

<br>

# 1️⃣ Cluster setup

Let's start by creating a cluster with a lot of **CPUs**: ideal for distributing our task across!

🚨 **Cost alert** 🚨
This will create **4 machines** (of `e2-standard-2`): 2 nodes in each of the 2 node-locations

Approximate cost (may vary depending on region and other factors):
- VM cost: 4 * $0.134/hour
- GKE overhead: $0.1/hour
- Total = $0.904/hour
- est. total for challenge ~ $1

👇 Run the following to create our **cluster**:

```bash
gcloud container clusters create mydaskcluster \
--machine-type e2-standard-2 \
--num-nodes 2 \
--disk-size "30" \
--zone=europe-west1-b \
--node-locations=europe-west1-b,europe-west1-c
```

```bash
# TO DELETE IT LATER ON
gcloud container clusters delete mydaskcluster --zone=europe-west1-b
```

⏰ Keep reading while its provisioning - the cluster can take ~10 minutes to spin up.

<br>

# 2️⃣ Adding our helm chart

First, install **helm** on your VM, if you haven't already:

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

We can install the **helm** chart on the cluster by first adding the repo.

```bash
helm repo add dask https://helm.dask.org/
helm repo update
```

❓**Checkout `config.yaml` which will be used by helm**

- We are telling the cluster what the **worker** pods need in terms of **resources**.
- We are adding the extra pip packages. ❗️ It is super important that the versions of packages you need for your code are the same locally and on the **pods** to allow it to be distributed.
- Finally we are disabling jupyter we are going to use the **jupyter on your vm!**

⏰ Hopefully the **GKE cluster** is done provisioning by now!

Kubectl should be configured to apply your commands to this GKE cluster:

```bash
kubectl config current-context
```

Checkout the nodes:

```bash
kubectl get nodes
```

Then apply the **helm** chart:

```bash
helm install mydask dask/dask -f config.yaml --version=2022.11.0
```

❓ Have a look at the the pods that were created!

```bash
kubectl get deployments
kubectl get services
kubectl get pods
kubectl top nodes # how cool is that 😎
```

You can see we have 4 pods running for **Dask**, with 1 CPU each. That is 4 CPUs for you to distribute your work on! One scheduler-pod is also using a CPU.

We've got 3 spare CPUs that we're not using 🥲. Finetuning the cluster is too much work for today, let's move on!

Then you can **port forward** from port **80** (the Dask default) on the `mydask-scheduler` **service** to **8000** on your vm.

<details>
<summary markdown='span'>💡 Port forwarding reminder!</summary>

```bash
kubectl port-forward services/mydask-scheduler 8000:80
```

</details>

This lets us access the dashboard which will allow us to track the computations across our **cluster!**

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D3-processing/dask/dask-dashboard.png" width=700>

<br>

# 3️⃣ Notebook time 📚

❓ **Open up `dask.ipynb` with `jupyter` (not vscode) and follow the notebook!**

Some jupyter dask extensions don't run in VSCode

<br>

# 4️⃣ Taking it further 🕵️

❓ If you have **time** you can change `config.yaml` and delete the part disabling jupyter! Then `helm upgrade` and connect to jupyter on the cluster and dask provides some great notebooks to further your knowledge!

<br>

# 🏁 Delete your cluster 🚨

Make sure to tear down your cluster to avoid an unwanted bill!

```bash
gcloud container clusters delete mydaskcluster --zone=europe-west1-b
```

<br>
