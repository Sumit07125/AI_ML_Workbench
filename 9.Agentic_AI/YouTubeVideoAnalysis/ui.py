import streamlit as st
from youtube import build_youtube_agent

st.set_page_config(page_title="YouTube Video Analysis", page_icon="🎥", layout="wide")

st.title("🎥 AI YouTube Video Analysis") 

@st.cache_resource #store code or model in cache memory to avoid reloading every time
def get_agent():
    return build_youtube_agent()

build_agent = get_agent()


video_url = st.text_input("Enter YouTube Video URL:") # string
button_clicked = st.button("Analyze Video") # true or false

if video_url and button_clicked:
    with st.spinner("Analyzing video..."):
       response =  build_agent.run(
            f"Analyze this video: {video_url}"
        )
       st.markdown("Analysis Report Of Video:")
       st.markdown(response.content)