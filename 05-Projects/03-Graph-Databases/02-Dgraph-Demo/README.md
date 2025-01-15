# Dgraph

🎯 The goal of this demo is to setup a custom [k3s](https://k3s.io/) cluster and deploy dgraph on it!

## Deploy the cluster

1.
Go into the infrastructure folder and you need to fill two files

- `terraform.tfvars` adding an ssh key to the cluster
- `provider.tf` filling it out with the details of your project and area

2.
Now run `terraform init`

Plan and apply and this is enough to have your own kubernetes cluster totally managed by yourself 🤯

3.
We want to be able to connect to the cluster from `kubectl` in our machine to do that you need to copy `/etc/rancher/k3s/k3s.yaml` from the master **to your vm** use [scp](https://cloud.google.com/sdk/gcloud/reference/compute/scp)

4.
Now you can interact with the cluster you just need to update the k3s.yaml you copied over changing the `server` to have the ip address of your master then try
```bash
kubectl --kubeconfig=./k3s.yaml get nodes
```
You should have access to the cluster you setup yourself!

## Deploy dgraph

Now lets add dgraph to our cluster

```bash
kubectl --kubeconfig=./k3s.yaml create --filename https://raw.githubusercontent.com/dgraph-io/dgraph/main/contrib/config/kubernetes/dgraph-single/dgraph-single.yaml
```

That's it!

## Connect to dgraph

Port forward from the pods

```bash
kubectl --kubeconfig=./k3s.yaml port-forward pod/dgraph-0 8080:8080
```

```bash
kubectl --kubeconfig=./k3s.yaml port-forward pod/dgraph-0 8000:8000
```

Now if you **port forward to your host machine** you should be able to access the ui at localhost:8000

## Test it out

To test out your graph database follow the tutorial on the dgraph docs:

- https://dgraph.io/docs/dql/dql-get-started/

## Clean up 🧹

It is easy to clean up thanks to terraform!
```bash
terraform destroy
```
