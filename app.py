import streamlit as st
from utlis import *

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def main():
    st.title("Learner's Video Analyzer")

    # Create a session state
    state = SessionState(yt_option=False, local_option=False)

    # Create a sidebar menu
    menu_options = ["Dashboard", "About", "Contact"]
    selection = st.sidebar.radio("Menu", menu_options)

    if selection == "Dashboard":
        st.subheader("Dashboard")
        st.write("Welcome to Learner's Video Analyzer!")

        # Option to select YouTube or local video
        option = st.sidebar.selectbox("Select Option:", ["YouTube Video", "Local Video"])

        if option == "YouTube Video":
            state.yt_option = True
            state.local_option = False
            yt_url_input = st.sidebar.empty()  # Create empty container
            yt_url = yt_url_input.text_input("Enter YouTube Video URL:")
            if st.sidebar.button("Analyze"):
                if yt_url:
                    try:
                        yt_url_input.empty()  # Hide the input field
                        metadata = get_video_metadata(yt_url)
                        st.sidebar.subheader("YouTube Video:")
                        st.sidebar.video(yt_url)  # Display video in sidebar
                        with st.sidebar.expander("Video Metadata"):
                            for key, value in metadata.items():
                                if key == 'duration':
                                    min_length, sec_length = convert_to_min_sec(value)
                                    st.write(f"Length: {min_length} minutes {sec_length} seconds")
                                else:
                                    st.write(f"{key.capitalize()}: {value}")
                        with st.sidebar.expander("Video Transcript"):
                            transcript, clean_transcript = get_video_transcript(yt_url)
                            st.write(clean_transcript)
                            # print(clean_transcript)
                    except Exception as e:
                        st.error(f"Error: {e}")
            search_dictionary_streamlit(yt_url)

        elif option == "Local Video":
            state.local_option = True
            state.yt_option = False
            video_file_input = st.sidebar.empty()  # Create empty container
            video_file = video_file_input.file_uploader("Upload Local Video:", type=["mp4", "mov"])
            if video_file is not None:
                title = st.sidebar.text_input("Video Title:")
                if st.sidebar.button("Analyze"):
                    try:
                        video_file_input.empty()  # Hide the file uploader
                        st.sidebar.subheader("Uploaded Video:")
                        st.sidebar.video(video_file)  # Display video in sidebar
                        with st.sidebar.expander("Video Metadata"):
                            # Get video metadata
                            length_seconds = get_video_length(video_file)
                            min_length, sec_length = convert_to_min_sec(length_seconds)
                            st.write(f"Title: {title}")
                            st.write(f"Length: {min_length} minutes {sec_length} seconds")
                        with st.sidebar.expander("Video Transcript"):
                            path = "temp_video.mp4"
                            transcript, clean_transcript = transcribe_audio(path)
                            st.write(clean_transcript)
                            # print(clean_transcript)
                    except Exception as e:
                        st.error(f"Error: {e}")

    elif selection == "About":
        st.subheader("About")
        st.write("This is a Streamlit app for analyzing YouTube videos and local videos.")

    elif selection == "Contact":
        st.subheader("Contact")
        st.write("For any inquiries, please email us at example@example.com")

if __name__ == "__main__":
    main()
