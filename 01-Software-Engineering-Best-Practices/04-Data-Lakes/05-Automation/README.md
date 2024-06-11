# 🎯 Goals

We have a pipeline that does a fair bit, but how can we automate the process? One way is to deploy a cloud function to automate it to happen everyday! A cloud function is a small piece of code that runs on the cloud. It is a great way to run small pieces of code without having to worry about servers or infrastructure. We will use a cloud function to run our scraper everyday.

You may have heard of the equivalent AWS product: Lambda Functions!

<br>

# 1️⃣ Deploying a Cloud Function

Here's a basic guide to deploying a multi-file Cloud Function:

1. **Project Structure**:
   - Your Cloud Function can have a directory structure similar to this:

     ```bash
     /my-function
         |- main.py
         |- helper.py
         |- requirements.txt
     ```

   In this example, `main.py` contains the Cloud Function entry point, while `helper.py` contains some additional functions or classes that the main function uses.

2. **main.py**:

   ```python
   import helper

   def my_cloud_function(request):
       # Use functions or classes from helper.py
       result = helper.some_function()
       return result
   ```

3. **helper.py**:

   ```python
   def some_function():
       return "Hello from helper!"
   ```

4. **requirements.txt** (optional):

   If your function requires third-party libraries, you can list them in a `requirements.txt` file. Google Cloud will install these dependencies when you deploy the function:

   ```bash
   flask==1.1.2
   requests==2.25.1
   ```

5. **Deploying the Function**:

   Navigate to your function's root directory (`/my-function` in this case) and use the `gcloud` CLI to deploy your function:

   ```bash
   gcloud functions deploy my_cloud_function \
     --runtime python310 \
     --trigger-http \
     --allow-unauthenticated \
     --set-env-vars "KEY=VALUE" \
     --memory 256MB
   ```

   In the command above:
   - `my_cloud_function` is the name of the function you're deploying.
   - `--runtime python310` specifies that you're using Python 3.10.
   - `--trigger-http` indicates that this function is triggered by HTTP requests.
   - `--allow-unauthenticated` allows the function to be called without authentication (for testing purposes, but be careful in a production environment).
   - `--set-env-vars "KEY=VALUE"` sets environment variables for the function. You can set multiple variables by separating them with commas, like this: `--set-env-vars "KEY1=VALUE1,
   KEY2=VALUE2"
   - `--memory 256MB` sets the memory limit for the function. The default is 256MB, but you can increase it up to 2GB.

6. **Testing the Function**:

   Once deployed, you can use the provided URL to test your function.

Remember, when using multiple files in a Cloud Function, you must ensure that all the necessary files are in the deployment directory or specified in the `requirements.txt` file. All dependencies must be available at runtime for the function to successfully execute.

<br>

# 2️⃣ Create a Cloud Function for our pipeline

Make sure to read this section in full before you start, you'll need to make some changes to the code to deploy the package as a Cloud Function.

Start by copying over the code files from the previous challenge. You will need to generate a `requirements.txt` from poetry.

❓ The first code change you will need is to make main accept an argument (it does not need to be used) and return a string.

❓ The second code code change is that the csv needs to be written to `/tmp` this is a special directory that is writable by the cloud function.

😓 Great expectations does not work so well in a cloud function so you should also probably remove that step (you would generally use it inside airflow which we will see later)!

<br>

# 3️⃣ Make the cloud function run everyday

Use the following command!

```bash
gcloud scheduler jobs create http daily_scrape --schedule="0 0 * * *" --http-method=POST --uri=your_function_uri --time-zone=Europe/Paris --headers="Content-Type=application/json" --message-body='{}'
```

Give the scheduler permission to run the function:

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member=serviceAccount:service-YOUR_PROJECT_NUMBER@gcp-sa-cloudscheduler.iam.gserviceaccount.com --role=roles/cloudfunctions.invoker

```

Then to run it ahead of time:

```bash
gcloud scheduler jobs run daily_scrape
```

<br>

# 🏁 Finish

We now have a fully automated scraper that runs everyday without our intervention!

<br>
