import streamlit as st
import re
from urllib.parse import parse_qs, urlparse
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # invalid YouTube URL
    return None

def extract_start_time(video_url):
    match = re.search(r'\?t=(\d+)s', video_url)
    if match:
        return int(match.group(1))
    else:
        return 0  # Default to start from the beginning if time parameter not found

def search_dictionary_streamlit():
    # Get inputs from the user
    video_url = st.text_input("Enter YouTube Video URL:")
    user_input = st.text_input("Enter a word or sentence to search for:")
    if st.button("Search"):
        if video_url.strip() and user_input.strip():
            video_id = extract_video_id(video_url)
            if video_id:
                # Retrieve transcript
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_transcript(['en'])
                data = transcript.fetch()

                # Create dictionary from transcript
                dictionary = []
                for segment in data:
                    dictionary.append({'text': segment['text'], 'start': segment['start']})

                # Search for user input in the transcript
                link = f'https://youtu.be/{video_id}'
                results = []
                for segment in dictionary:
                    if user_input.lower() in segment['text'].lower():
                        results.append(segment)

                # Format and display results
                st.subheader("Search Results:")
                if results:
                    for result in results:
                        start_time = result['start']
                        minutes = int(start_time) // 60
                        seconds = int(start_time) % 60
                        st.write(f"{result['text']} ... {minutes} min and {seconds} sec :: {link}?t={int(start_time)}s")
                else:
                    st.write("No matching segments found in the transcript.")
            else:
                st.write("Invalid YouTube Video URL.")

# Example usage:
search_dictionary_streamlit()
