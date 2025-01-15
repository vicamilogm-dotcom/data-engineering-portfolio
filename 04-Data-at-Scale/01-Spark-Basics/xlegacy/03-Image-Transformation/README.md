# Image transformation with Python

In this exercise, we'll build a cool real-time face detection app, step by step!

As a bonus, for the bravest, you'll have the opportunity to deploy it to your cloud provider and show it to the world 😎.

The exercise is broken down into the following bits:

1. Build a function that detects faces from images
2. Hook this function to a simple Streamlit app. Images will be uploaded to the app, faces detected using the function in step 1, and results displayed back on the Streamlit app.
3. First deployment to the internets 🔌.
4. Enhance the Streamlit app and hook it to your webcam 📹.
5. Enhance the image detection module with a deep learning model 🧮.
6. Deploy the now multi-page app to the cloud again.

## Python code directory structure

The code is split between three files:

```bash
├── lwface
│   ├── Home.py
│   └── pages
│       ├── Face.py
│       └── Webcam.py
```

- As the names suggest, the app entrypoint is in `lwface/Home.py`, you shouldn't need to touch this file.
- We'll first work on the `lwface/pages/Image_Upload.py` file, it has the code for face detection on an uploaded image.
- Then on `lwface/pages/Webcam.py` file, which has the code to hook your app up to your webcam and do face detection through a deep learning model.

## Dive into the Python libraries

Let's look into our `pyproject.toml` file to understand which libraries we've installed and why.

### Image analysis

- [Matplotlib](https://matplotlib.org/) is the most used data visualization / plotting library in Python.
- [Seaborn](https://seaborn.pydata.org/) is the second most used data visualization / plotting library in Python. More modern but also less featured than Matplotlib. It is used under the hood in the webcam page.
- [Pillow](https://pillow.readthedocs.io/en/stable/) is the Python Imaging Library, you'll find it used everywhere images are loaded and transformed. It is compatible with Numpy, images are "just" arrays of integers at the end of the day. **Ask your TA for more details about this if you're curious as to why**.
- [Scikit-Image](https://scikit-image.org/) is a collection of algorithms for image processing, highly compatible with the Numpy ecosystem and Pillow.
- [Torch](https://pytorch.org/), developed by Facebook Research, is one of the three most popular deep learning frameworks. We use it to enhance our face detection algorithm.
- [Torchvision](https://pytorch.org/vision/stable/index.html) is part of Pytorch, and extends it with methods to manipulate image data.
- [Numpy](https://numpy.org/), the fundamental package for scientific computing with Python. As images are just Numpy arrays for the computer, all packages above use Numpy for processing.
- [OpenCV](https://opencv.org/) is a famous C++ image manipulation / transformation library, it has great Python bindings with `opencv-python`. It is used under the hood in the webcam page.


### Server

- [Streamlit](https://streamlit.io/) which you've seen previously, is a simple yet powerful way to build data apps.
- [Watchdog](https://pypi.org/project/watchdog/) when combined with Streamlit, allows us to run the app while working on the code. Just run `make run` to run the app, then work on the code and just reload the page in your browser for changes to take effect. Magic 🎂!
- [Streamlit WebRTC](https://github.com/whitphx/streamlit-webrtc) to hook your camera to a Streamlit application using [WebRTC](https://webrtc.org/).
- [av](https://pypi.org/project/av/) is used to convert the WebRTC video frames to Python-friendly data structures that can be fed to our image processing algorithms.
- [tqdm](https://github.com/tqdm/tqdm) is a nice looking progress bar, used under the hood in the webcam page.


## Extract faces using Scikit-image

### Setup note

You might need to install additional `apt` libraries. Feel free to run `sudo apt install -y <library1> <library2>` etc. for the extra libraries. If you encounter an error while running the code below, you should be hinted on what to install.

### Exercise

Let's start the work on `lwface/pages/Image_Upload.py`.

We'll start by building the simpler face detection function `def detect_face(...)`.

Use the [face detection module](https://scikit-image.org/docs/stable/auto_examples/applications/plot_face_detection.html#sphx-glr-auto-examples-applications-plot-face-detection-py).

Only accept JPEG images of type `jpeg` or `jpg`.

<details>
  <summary markdown='span'>💡 Hint</summary>

  - If you struggle finding the right bits to use, try running the example.
  - Then import the right libraries.
  - Use the function signature to understand the right input and output types.
  - Then only keep the bits needed in `detect_face`, given an image, to return the detected patches.
</details>


## Set up Streamlit with image upload

Use the Streamlit documentation on [file upload](https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader) to fill the `def streamlit_read_uploaded_file()` function. **This should return the uploaded file**.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Notice that the Streamlit example gives you many ways to load and then convert the `uploaded_file`, we only care about the file loading part.
</details>

## Find the face patches on the uploaded image

In the main function, called `def streamlit_page()`, we want to build the image with embedded face patches on it, like in the Scikit image tutorial (see the red square around the face). The result is stored in the variable `img_with_patches` which we've initialized to `img_with_patches = None`.

<img src="https://scikit-image.org/docs/stable/_images/sphx_glr_plot_face_detection_001.png" width=400>

We've written the function `def apply_face_patches_to_original_image(...)` for you, it's just a matter of applying it to the right inputs to get the image with face patches. **Can you do it?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  The function `apply_face_patches_to_original_image` has two inputs.

  - `img` of type `np.ndarray`
  - `face_patches` of type `List[Patch]`

  Use the types to find the right values to plug in as inputs, from what has already been calculated in this function `def streamlit_page()`
</details>

## Display the image back on the page

Now that we have:

- Uploaded an image
- Applied the face recognition onto it
- Embedded the face patches on the original image

**Let's display that image with face patches in the webapp**. This last bit of code needs to be added at the end of `def streamlit_page()`.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Look at the [official documentation](https://docs.streamlit.io/library/api-reference/media/st.image) from Streamlit.
</details>

## Deploy to the cloud this first version of the app

Congratulations, you've built a fun webapp to detect faces. Let's share it with the world 🌏.

**Step 1**

Regardless of your cloud provider, we'll need to **package the app within a Docker image**. We've already written the `Dockerfile` for you. We've left a lot of comments in it. Please take a moment to read through it and **follow the instruction at the end**. Run `make test` and `git push` your code, `test_dockerfile` should pass.

**Now build the Docker image with `make build`.**

**Step 2**

We assume below that you have followed the first exercise setup instructions, and now have a working Google `Cloud Artifact Registry` Docker repository. If not, please go back to that exercise 👈.

We need you to find your registry prefix. You'll find it by selecting the registry repository created in the first exercise, then clicking on the `Copy` icon at the top right.

It should look like `europe-west9-docker.pkg.dev/subtle-creek-348507/data-engineering-docker`.

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/lw-artifact-registry-copy.png" alt="Copy" width=600>

**Once you have it, set the value of `REGISTRYPREFIX` in your `Makefile`, at the top.**

**Step 3**

👉 Now you can re-tag the image with `make tag`. **We highly encourage you to read carefully through the commented Makefile, it should be instructive 🔓.**

**Step 4**

👉 Finally, let's push it to the cloud with `make push`.

**Go to your cloud console, Artifact Registry and look for this newer version, can you find it?**

**Step 5**

Deploy it!

Go to Cloud Run and create a new service: click `CREATE SERVICE`.

- `Deploy one revision from an existing container image`, click `SELECT` and in the tab `Artifact Registry`, look for your image
- Give it the service name `lwface`
- Pick the closest region, if you're in Europe, pick `europe-west` for instance.
- CPU allocation: `CPU is only allocated during request processing`
- Autoscaling: Minimum of 0 and Maximum of 3
- Open `Container, Variables & Secrets, Connections, Security`
  - What's the container port? Hint 💡: look in the `CMD` of the `Dockerfile`
  - Up the memory to 8 GiB
  - Keep the CPU at 2
  - Maximum requests per container: 50
  - Minimum = 1 and Maximum = 1 for the number of instances
  - Connection tab: check "Session affinity"
  - In the environment variables, set `HOME` to `/root`. By default, Google Cloud Run has a [strange behaviour](https://chanind.github.io/2021/09/27/cloud-run-home-env-change.html) we need to override.
- Click `CREATE` 🚀

Once deployed, your app should be live with a URL, try it, share it with your peers!

## Pimp the app, real-time face detection using Streamlit

Uploading an image and detecting a face is fun, but adding real-time person detection features is more fun 🎥.

We have pre-filled the `lwface/pages/Webcam.py` file with code from the project below, please have a look at it:

- Code [here](https://github.com/nicolalandro/yolov5_streamlit)
- Demo [here](https://share.streamlit.io/nicolalandro/yolov5_streamlit/main)

You'll notice that this doesn't use standard image transformation libraries like OpenCV or Scikit-Image, but a deep learning model, loaded in the Pytorch library.

**To make it work, you need to call `run_webrtc_streamer()` in the `lwface/pages/Webcam.py` file**.

Run your app with `make run` and go to the `Webcam` page. Now stand in front of it, does it work?

**Note** It's normal that the page takes up to a minute to load.

**Update the `TAG` variable in the `Makefile` to be of version 0.2 instead of 0.1**.

## Bonus - Final optimization!

**If you feel like you've spent enough time on this exercise, skip this part and move on to the next exercise!**

You might have noticed that the first time you run the Webcam app, it takes a while for it to load.

If we look closely into the `Webcam.py` file, we'll notice a line that smells like it could use some optimization

```python
    if not hasattr(st, 'classifier'):
        st.model = torch.hub.load('ultralytics/yolov5', 'yolov5s',  _verbose=False)
```

In this line, the Pytorch model (a file that weights several megabytes), is downloaded. Your user will have to bear the wait time because we load it when the page loads for the first time, instead of downloading it at **build** time.

Let's run this step at build time, this should improve the app's performance.

In your Dockerfile, add the following command

```Dockerfile
RUN poetry run python -c "import torch; torch.hub.load('ultralytics/yolov5', 'yolov5s',  _verbose=False)"
```

Let's break this down:

- `RUN` instructs Docker to run this step at **build** and not **run** time (that would be the `CMD` instruction)
- `poetry run python` is simply to help find the right Python install. It's equivalent to just running `python` if the setup is right (like on your VM, thanks to [direnv](https://direnv.net/)).
- `python -c` means "I'm going to give you some Python code now, run it as a script for me.
- And `"import torch; torch.hub.load('ultralytics/yolov5', 'yolov5s',  _verbose=False)"` is the Python code you'd like to run. That'll download the model within your Docker image.

Once you're done, tag your `TAG` in the `Makefile` to version 0.3! Does this page load faster this time?

## Final note

For your own projects, Streamlit offers a turnkey deployment with the [Streamlit Community Cloud](https://streamlit.io/cloud). Check it out!
