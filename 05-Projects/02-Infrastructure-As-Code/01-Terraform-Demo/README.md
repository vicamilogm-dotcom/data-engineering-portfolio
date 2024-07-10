# Terraform Demo

🎯 The goal of this demo is to provide a **basic** template for you to expand on if you want to use **terraform**

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/0502-IAC/terraform.png" width=400>

## Setup

1. First you need to install Terraform following the instructions for your OS [here](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).

2. Make sure you are authenticated to Google Cloud Platform!

## Testing the project

### 1. Define the infrastructure

Navigate to the production folder. 

Inside the folder are a few important files:

- `variables.tf`: where the required variables are defined for the  project
- `main.tf`: where the infrastructure is defined
- `provider.tf`: define the gcloud (or other cloud provider) to use
- `terraform.tfvars`: a file to define values for the variables defined in `variables.tf`

**Make sure to update** `provider.tf` and `terraform.tfvars` before moving onto creation

### 2. Create the infrastructure

Run the below commands:

```bash
terraform init
terraform plan
```

Checkout the plan and, if the resources look good:

```bash
terraform apply
```

🚀 You've now created some cloud resources just using code

### 3. Tracking the state of the resources 

At the moment the state of the cloud resources is tracked by the local .tfstate file. Let's change that:

Rename `backend.tf.example` and **manually complete it** with the name of the bucket you have just created!

❗️ It is not possible to use variables in the backend. That is why here we have to manually complete it.

💡 At this point you have a working setup and **can add and remove infrastructure as you need it**!

### 4. Cleanup

Cleanup will be just one command:

```bash
terraform destroy
```

The ease of this along with state matching our code means we never leave unwanted and costly cloud resources running!

## Going further

If you want to automate even further checkout this [tutorial](https://cloud.google.com/docs/terraform/resource-management/managing-infrastructure-as-code)
