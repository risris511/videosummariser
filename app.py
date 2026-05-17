import streamlit as st
from google import genai
from google.genai import types
import tempfile
import time
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

st.set_page_config(
    page_title="Video Summarizer",
    page_icon="🎥",
    layout="wide"
)

st.title("Gemini Video Summarizer")
st.header("Powered by Gemini 2.5 Flash")

video_file = st.file_uploader(
    "Upload a video",
    type=["mp4", "mov", "avi"]
)

if video_file:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

    st.video(video_path)

    user_query = st.text_area(
        "Ask something about the video",
        placeholder="Summarize this video..."
    )

    if st.button("Analyze Video"):

        if not user_query:
            st.warning("Please enter a query.")

        else:
            with st.spinner("Uploading and analyzing video..."):

                uploaded_file = client.files.upload(
                    file=video_path
                )

                while uploaded_file.state.name == "PROCESSING":
                    time.sleep(2)

                    uploaded_file = client.files.get(
                        name=uploaded_file.name
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        uploaded_file,
                        user_query
                    ]
                )

                st.subheader("Result")
                st.write(response.text)