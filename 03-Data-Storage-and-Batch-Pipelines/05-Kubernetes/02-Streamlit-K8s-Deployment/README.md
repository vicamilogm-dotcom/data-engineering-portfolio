🎯 The goal of this exercise is to put the Streamlit F1 dashboard app and accompanying Postgres database in production on Kubernetes (k8s).

🖥️☁️ We'll start off with a local deployment using Minikube then deploy in the cloud on Google Kubernetes Engine (GKE).

📦 The Streamlit F1 dashboard is the same dashboard that you worked on in the **Streamlit** challenge in the **Data Visualisation unit**. We've provided the Streamlit code so you can focus on the Kubernetes concepts. Feel free to have a look through the code if you didn't finish the Data Visualisation - Streamlit challenge.

❗ This is a substantial challenge, don't worry if you don't finish it during the bootcamp! It's a fantastic challenge to come back and revisit after you've finished! 💪

# 0️⃣ Context

<details>
  <summary markdown='span'> Open me! </summary>

This time, we'll have to deal with 2 separate containers:
- Streamlit (to build from our local Dockerfile)
- Postgres (to build from official dockerhub image)

Compared with 1 `docker-compose.yml`, K8s will require us to explode configuration into many configurations files!

- 3 for Streamlit:
  - service
  - deployment
  - secret

- 5 for Postgres:
  - service
  - deployment (statefulset)
  - secrets
  - volumes
  - volumes claims

- And for deployment on GKE we'll have to modify 4 existing `.yaml`'s with GCP specific parameters:
  - Streamlit deployment cloud
  - Postgres deployment (statefulset) cloud
  - volumes cloud
  - volumes cloud claim

🔍 Through this we will see a number of important concepts in k8s such as:
- secrets
- volumes
- communication between services
- scaling
- fault tolerance


Let's do it! 🏎️

</details>


# 1️⃣ Setup 🛠️

<details>
  <summary markdown='span'> Open me! </summary>

## 1.2) Clean Minikube cluster

We also want to start from a clean Minikube cluster, so if you did not delete yours at the end of the previous exercise, run this 👇

```bash
minikube delete
```

Then start a new cluster with 👇

```bash
minikube start
```

We can also check to make sure there are no other services by running 👇

```bash
kubectl get svc
```

which should return just:

```
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   2m12s
```

</details>

# 2️⃣ Postgres 🗄️

<details>
  <summary markdown='span'> Open me! </summary>

## 2.1) Service

The first step for our Postgres is to define the service.

❓ Create a `postgres-service.yaml`. Then populate it with the template using `k8sService` like in the image below.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/service-autocomplete.png" width=400>

You should get this template:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/service-template.png" width=400>

❓ **Now populate the template to create a clusterIP**. You can hover over all of the keys and you will get an explanation of what they do! 💡

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/cluster-ip.png" height=400 width=400>

- For now you can replace `MYAPP` with `postgres`.
- The type is already `ClusterIP` which is ideal for us, as we don't need to expose Postgres outside of k8s, just to our Streamlit app.
- Then delete the keys mentioning `sessionAffinity` and `nodePort`.
- Finally set the `port` and `targetPort`. Port can be what you like, but `targetPort` needs to be `5432` to target the port Postgres runs on.



<details>
<summary markdown='span'>💡 Completed Postgres service yaml</summary>

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: default
spec:
  selector:
    app: postgres
  type: ClusterIP
  ports:
  - name: postgres
    protocol: TCP
    port: 5432
    targetPort: 5432
```

</details>

## 2.2) Volumes

Next for our Postgres we will need a volume to keep our Postgres data in the same way we needed one for docker-compose.

There are two parts to volumes on Postgres - **volumes**, and **volume claims**. Volumes are the creation of the space on the cluster. Our pod then needs to access that volume and so the volume claim describes how the pod will be accessing the volume (i.e. how much space can the pod use of the total volume).

❓ **Create a new file for the volume `postgres-pv.yaml`.**

Generally most users won't be making volumes, only claims, but you can still start with a k8s template by typing `Persistent Volume` in the yaml file you just created. Then, add the code below and try to hover over the keys and understand them! 🔍

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-volume
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 2Gi
  hostPath:
    path: /data/postgres
  storageClassName: standard
```

Next - the part more commonly done by developers, which is making the claim.

❓ **So now make the file `postgres-pvc.yaml` and use the template `k8sPersistentVolumeClaim`.**

You can delete the `storageClassName` key and update the metadata so that the name matches `postgres-volume-claim` and the app label is `postgres`.

<details>
<summary markdown='span'>💡 Completed volume claim </summary>

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-volume-claim
  namespace: default
  labels:
    app: postgres
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
```
</details>

We now have a volume for our Postgres to store its data! 🙌

## 2.3) Secrets

We need secrets to store environment variables such as the Postgres user and password of your local Postgres services.

❓ Create another file `postgres-secret.yaml`.
You can use the `k8sSecret` template. Then set the name to `postgres-secrets`.

Now we need to fill the secrets here. The keys can be what you want as the environment variables, while the values have to be the **base64 encoding of the data**. For example for `POSTGRES_PASSWORD` set to `password`, the end result is:

```yaml
POSTGRES_PASSWORD: cGFzc3dvcmQ=
```

❓ Fill in your own `POSTGRES_USER` and `POSTGRES_PASSWORD` keys. To generate the base64 encoding you can use this 👇

```bash
printf password | base64
```

Now we have our secrets and are ready to create our Postgres pod! 🚀

## 2.4) `StatefulSet` (~ Deployments for pods with volumes)

We want to deploy our postgres pods which are associated with volumes.
We need to define a `StatefulSet`, which our service will use to run a pod with the Postgres container included!
We shouldn't use a `Deployment` (as with FastAPI), as these might get out of sync with the volumes according to [Kubernetes' Statefulset](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) docs:

>_"StatefulSet is the workload API object used to manage stateful applications. It manages the deployment and scaling of a set of Pods, and provides guarantees about the ordering and uniqueness of these Pods.  Like a Deployment, a StatefulSet manages Pods that are based on an identical container spec. *Unlike a Deployment, a StatefulSet maintains a sticky identity for each of their Pods*. These pods are created from the same spec, but are not interchangeable: each has a persistent identifier that it maintains across any rescheduling. If you want to use storage volumes to provide persistence for your workload, you can use a StatefulSet as part of the solution. Although individual Pods in a StatefulSet are susceptible to failure, the persistent Pod identifiers make it easier to match existing volumes to the new Pods that replace any that have failed."_




❓ Create another file called `postgres-statefulset.yaml`. Populate it with the code below 👇 (there is a template for this as well, called `k8sStatefulSet`, for when you write your own).

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-statefulset
  labels:
    app: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  serviceName: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:11.4
          env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  key: POSTGRES_USER
                  name: postgres-secrets
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  key: POSTGRES_PASSWORD
                  name: postgres-secrets
          ports:
            - containerPort: 5432
              name: access
              protocol: TCP
          volumeMounts:
            - name: postgres-mount
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-mount
          persistentVolumeClaim:
            claimName: postgres-volume-claim
```

🤯 Wow, a lot of code! Lets break down the parts you have not seen before.

To get our previously defined secrets into the environment variables of the container we use this syntax:

```yaml
env:
- name: POSTGRES_USER
    valueFrom:
    secretKeyRef:
        key: POSTGRES_USER
        name: postgres-secrets
```

Here the `name` refers to the name we set in `postgres-secret.yaml`. Along with the `key`, which is what the environment variable should be called inside the container! It might be a lot of code compared to compose but **a lot of it is boilerplate you can use over and over again! ♻️**

Then we have our ports section exposing 5432 on our container:

```yaml
ports:
- containerPort: 5432
    name: access
    protocol: TCP
```

Finally the most complicated difference is how we use our volume we created before.

```yaml
    volumeMounts:
    - name: postgres-mount
        mountPath: /var/lib/postgresql/data
volumes:
- name: postgres-mount
    persistentVolumeClaim:
        claimName: postgres-volume-claim
```

The `volumes` section brings our claim into this yaml with the name `postgres-mount`.
Then inside our container definition we use `volumeMounts` to describe where the volume should be mounted inside the container!

## 2.5) Connecting it all together 🧰

Now we have all our files lets apply them to our cluster! 👇

```bash
kubectl apply -f .
```

Then lets check if our pod is running with 👇

```bash
kubectl get pods
```

Once it's running, lets connect! (similar to docker exec) 👇

```bash
kubectl exec -it <pod_name> -- <your_command>
kubectl exec -it postgres-statefulset-0 -- psql --user=<your user>
```

❓ We are in now lets create a new db for our F1 data!

```bash
CREATE DATABASE f1;
```

Now lets get our F1 data in there! First lets redownload the data and get the `.sql` file.

```bash
curl --output f1db.sql.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/f1db.sql.gz && gunzip f1db.sql.gz
```

Now we can copy our file into our running pod with 👇

```bash
kubectl cp f1db.sql postgres-statefulset-0:f1db.sql
```

Finally we can use `exec` to execute the SQL script and load our new database!

```bash
kubectl exec postgres-statefulset-0 -- psql -f f1db.sql --user=<your user> <your database>
```

Now we are ready to plug in Streamlit! 🧑‍🎨

</details>

# 3️⃣ Streamlit 🖼️

<details>
  <summary markdown='span'> Open me! </summary>

## 3.1) Service

❓ Now try create your own `streamlit-service.yaml` and populate it with a `LoadBalancer` service, with name `streamlit-service` and selector `app: streamlit`. What port should you it target ?

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/load-balancer.png" width=400>

<details>
  <summary markdown='span'>💡 Hints on ports</summary>

Look at the hint provided by the person who wrote the streamlit Dockerfile!
[EXPOSE](https://docs.docker.com/engine/reference/builder/#expose:~:text=It%20functions%20as%20a%20type%20of%20documentation%20between%20the%20person%20who%20builds%20the%20image%20and%20the%20person%20who%20runs%20the%20container%2C%20about%20which%20ports%20are%20intended%20to%20be%20published) doesn't actually do anything, but simply inform the person who runs the container, about which ports are intended to be published. In this case, it's the default streamlit port.
</details>


<details>
<summary markdown='span'>🎁 Completed service if you want to check</summary>

```yaml
apiVersion: v1
kind: Service

metadata:
  name: streamlit-service

spec:
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 8501
      targetPort: 8501
  selector:
    app: streamlit
```
</details>


## 3.2) Secrets

For our secrets in the original app we used a `secrets.toml` file. In k8s we can actually mount an entire secrets file as a value in the YAML file!

❓ Create a new file `streamlit-secret.yaml`. Here the keys should be the name of the files in your `.streamlit` you used in the _Data Visualization - Streamlit_ challenge and the values should be the results of `base64 <file>`!
```yaml
data:
  secrets.toml: <result of base64 secrets.toml>
  config.toml: <result of base64 config.toml>
```

When you update the `secrets.toml` file, the host will be the `name` of the postgres service this is how services inside k8s can speak to each other with ease (don't forget to update the other params as well).

<details>
<summary markdown='span'>🎁 Example completed file</summary>

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: streamlit-secrets
type: Opaque
data:
  secrets.toml: W3Bvc3Rncm ...
  config.toml: W3NlcnZlcl0 ...
```

</details>

Now we are ready to put it into the container!

## 3.3) Deployment

❓ First, build the streamlit Dockerfile **inside minikube** (🚨 not in your VM docker deamon)
You should see it with `docker images` along with a dozen other k8s containers...

<details>
<summary markdown='span'>💡 How to change docker context</summary>
Run the following command and follow its instructions:

```bash
minikube docker-env
```

</details>

❓ Then, let's create a new `streamlit-deployment.yaml`

```yaml
apiVersion: apps/v1

kind: Deployment

metadata:
  name: streamlit-deployment

spec:
  replicas: 4 # Let's have 4 pods to handle more incoming traffic!
  selector:
    matchLabels:
      app: streamlit

  template:
    metadata:
      labels:
        app: streamlit

    spec:
      containers:
      - name: streamlit-container
        image: # Add your streamlit image name:tag
        imagePullPolicy: Never
        volumeMounts:
          - mountPath: # Add the absolute path in your container in which to add secrets
            name: streamlit-secrets
            readOnly: true
        ports:
        - containerPort: 8501
        args: # Add the ["command", "you", "want", "to", "run"] to start the advanced.py dashboard

      # 👇 We add the secrets into the container by treating them as a volume
      volumes:
        - name: streamlit-secrets
          secret:
            secretName: streamlit-secrets
      restartPolicy: Always
```

❓ `montPath` : You can see how we have added the secrets into the container by treating them as a volume. Try to mount them where they belong

❓ `args` command in k8s is what's *added* to the Dockerfile ENTRYPOINT. (❗the equivalent in compose would be `command`. But k8s `command` overrides the entrypoint 🤯)

## 3.4) Putting it all together 🎀

❓ Now that we have everything ready to go with the Streamlit, apply all your config files and access the service on chrome!

<details>
<summary markdown='span'> 🎁 If you've forgotten how to access the service!</summary>

```bash
kubectl port-forward services/<service_name> <VM_localhost_port>:<k8s_service_port>
```

</details>

🍾 It your app working-well ? Sit back, relax, and try to play a bit with Kubernetes's VScode extension and minikube dashboard to see your logs, etc...before we try to make it work on GKE 🌶️

</details>

# 4️⃣ Google Kubernetes Engine 🌎

<details>
  <summary markdown='span'> Open me! </summary>

## 4.0 Setup

We will need an extension to help us interact via kubectl -> gke

```bash
gcloud components install gke-gcloud-auth-plugin
```

## 4.1 Creating the cluster

First we want to create a new k8s cluster on gcloud use the command below 👇

```bash
gcloud container clusters create "streamlit-f1" \
  --region "europe-west1" \
  --machine-type "e2-standard-2" \
  --disk-type "pd-standard" \
  --disk-size "30" \
  --num-nodes "1" --node-locations "europe-west1-b","europe-west1-c"
```

This will take a while 😅 so we can continue and edit some of our files while it provisions!

## 4.2 Postgres

We need to change our volume config file from local [`PersistentVolume`](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) to [`StorageClass`](https://kubernetes.io/docs/concepts/storage/storage-classes/) for the cloud.

❓ **Replace your `postgres-pv.yaml` with the code below 👇**

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1 # K8s standard
metadata:
  name: postgres-volume
provisioner: kubernetes.io/gce-pd # Google Specific
parameters:
  type: pd-standard
  replication-type: regional-pd
allowedTopologies:
  - matchLabelExpressions:
      - key: failure-domain.beta.kubernetes.io/zone
        values:
          - europe-west1-b
          - europe-west1-c
```

🤯 This is one of the biggest areas of change when moving to the cloud.
- We are now describing the type of storage we want to take, based on a standardized API called "storage.k8s.io/v1"
- GCP is going to be reading our API call to provide the storage as we want it to be

🔍 Read the doc for [`StorageClass`](https://kubernetes.io/docs/concepts/storage/storage-classes/), it's well explained!

❓ **Then, just update your volume claim in a new `postgres-pvc.yaml`** by upgrading from 2 to `200G` to meet minimum Google requirement**

❓ **Finally, create a new `postgres-statefulset-cloud.yaml`** by simply adding an extra `PGDATA` envrioment variable to the postrgres `container`
```yml
- name: PGDATA
  value: /var/lib/postgresql/data/pgdata
```
GKE does not like us to directly put data into the root of the mount!


## 4.3 Streamlit

For streamlit, we can no longer use our local image. We need to build and push the container to an online registry, but to save time you can use ours.

❓ Simply replace these keys in your `streamlit-deployment.yaml`.

```yaml
image: europe-west1-docker.pkg.dev/data-engineering-students/student-images/streamlit-f1:0.1
imagePullPolicy: "IfNotPresent"
```

Hopefully our cluster is done provisioning now!


## 4.4 Putting it all together 🦋

❓ Lets make your local `kubectl` target your GCP new cluster (`minikube` was automatically kubectl target to minikube under the hood):

```bash
gcloud container clusters get-credentials streamlit-f1 --region europe-west1
# Then check that your kubectl context has indeed changed
kubectl config current-context
```

❓ Let's now apply all our config files at once by:

```bash
kubectl apply -f .
```

If everything go correctly you should see the pods running with:

```bash
kubectl get po
```

🍾 You can also see them in VScode extensions, and in [GCP console](https://console.cloud.google.com/kubernetes/workload_/gcloud/europe-west1/streamlit-f1).

❓ Try to find your public internet https address of your app running on GCP! You should also be able to find it with

```bash
kubectl get services
```

❓ It's just missing the f1db: Follow the steps we used earlier to put the f1 database in this new cluster.


🚀 We're in production 🚀

## 4.5 Simulating disaster 🔫

Keep your app open. Then lets find out where the database is currently running!

```bash
kubectl get pods -l app=postgres -o wide
```

Then take note of the `NODE`

```bash
kubectl cordon NODE
```

Will prevent anymore pods being provisioned on this node. Then delete the pod!

```bash
kubectl delete pod postgres-statefulset-0
```

Then checkout your app it should fail to connect to the database temporarily but keep refreshing and checking `kubectl get pods -l app=postgres -o wide`.

It will reprovision itself *on the other node* everything intact. For a complete failure like this it is incredibly impressive how fast k8s can fix everything (usually it can be seamless as most crashes you can see coming with load increasing)!

## 🏁 Lets cleanup so we don't spend too much:

To delete your cluster deployed on GKE 👇

```bash
kubectl delete -f . \
&& gcloud container clusters delete streamlit-f1 --region=europe-west1
```

To delete your local cluster to free up resources 👇

```bash
minikube delete
```

To stop Minikube 👇

```bash
minikube stop
```

</details>
