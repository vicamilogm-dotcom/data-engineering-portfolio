from typing import List, TypedDict

from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np
from PIL import Image

# Scikit-image (skimage) imports
# IMPORT YOUR PACKAGES HERE

# Streamlit, aliased 'st'
# IMPORT YOUR PACKAGES HERE


class Patch(TypedDict):
    c: float
    r: float
    width: float
    height: float


def detect_face(img: np.ndarray) -> List[Patch]:
    """
    Given an image `img` loaded as a `numpy.ndarray`, returns a list of detected patches.
    """
    # Insert code below to detect image patches from the image
    detected = None

    # YOUR CODE HERE

    return detected


def streamlit_read_uploaded_file() -> st.uploaded_file_manager.UploadedFile:
    """
    Configure streamlit to add file upload and read the bytes
    """
    # Load the uploaded file in this variable
    uploaded_file = None

    # YOUR CODE HERE

    return uploaded_file


def uploaded_file_to_image_ndarray(
    file: st.uploaded_file_manager.UploadedFile,
) -> np.ndarray:
    """
    Takes a file uploaded from Streamlit to an image in the numpy.ndarray format, perfect for image processing.
    """
    img = Image.open(file)

    basewidth = 300
    wpercent = basewidth / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    resized_img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)

    return np.array(resized_img)


def apply_face_patches_to_original_image(
    img: np.ndarray, face_patches: List[Patch]
) -> Image:
    """
    Given an image as a `np.ndarray` and a list of detected face patches
    - load the image in matplotlib
    - apply the face patches
    - then return the final image
    """

    # Load the image in Matplotlib
    plt.imshow(img)
    axes = plt.gca()
    plt.set_cmap("gray")

    for patch in face_patches:
        axes.add_patch(
            patches.Rectangle(
                (patch["c"], patch["r"]),
                patch["width"],
                patch["height"],
                fill=False,
                color="r",
                linewidth=2,
            )
        )

    fig = plt.gcf()
    fig.canvas.draw()

    return Image.frombytes(
        "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
    )


def streamlit_page():
    """
    Configure the full Streamlit app
    """
    # Setup. Configure the page and sidebar
    st.markdown("# Face detection 🤪 - Image file upload")
    st.sidebar.markdown("# Face detection 🤪 - Image file upload")

    # 1. Read an uploaded file
    uploaded_file = streamlit_read_uploaded_file()

    # Return early if no image has been uploaded
    if uploaded_file is None:
        return

    # 2. Convert the image file to a Numpy ndarray
    img_ndarray = uploaded_file_to_image_ndarray(uploaded_file)

    # 3. Detect the face patches
    face_patches = detect_face(img_ndarray)

    # 4. Print how many faces were detected
    st.write(f"Number of face(s) detected: {len(face_patches)}")

    # 5. Apply the patches to the original image
    img_with_patches = None
    # YOUR CODE HERE

    # 6. Display the image with face patches in Streamlit
    # YOUR CODE HERE


if __name__ == "__main__":
    streamlit_page()
