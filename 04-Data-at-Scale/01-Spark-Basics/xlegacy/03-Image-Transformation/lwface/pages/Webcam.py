import av
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import torch


RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


class VideoProcessor:
    """
    VideoProcessor is the class needed to transform the input frame from the webcam
    into something usable by the Pytorch model, which detects objects, in particular "people".
    """

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # vision processing
        flipped = img[:, ::-1, :]

        # model processing
        im_pil = Image.fromarray(flipped)
        results = st.model(im_pil, size=112)
        bbox_img = np.array(results.render()[0])

        return av.VideoFrame.from_ndarray(bbox_img, format="bgr24")


def page_setup():
    """
    Setup. Configure the page and sidebar
    """
    st.markdown("# Real-time face detection 🤟 - Webcam")
    st.sidebar.markdown("# Real-time face detection 🤟 - Webcam")


def run_webrtc_streamer():
    """
    Runs a WebRTC streamer to feed the webcam streeam to
    - VideoProcessor first, which converts the Webcam frame into a useable object for Pytorch
    - Then runs the Pytorch model
    """
    if not hasattr(st, "classifier"):
        st.model = torch.hub.load("ultralytics/yolov5", "yolov5s", _verbose=False)

    webrtc_streamer(
        key="WYH",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=False,
    )


def streamlit_page():
    """
    Setup the Streamlit page and run the WebRTC server
    """
    page_setup()
    # Below, add a call to the function above, which runs the "WebRTC" server
    # used to connect to your webcam
    # YOUR CODE HERE


if __name__ == "__main__":
    streamlit_page()
