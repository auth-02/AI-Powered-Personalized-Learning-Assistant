import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip
from youtube_transcript_api import YouTubeTranscriptApi
import whisperx
import re
from urllib.parse import parse_qs, urlparse


# Function to convert seconds to minutes and seconds format
def convert_to_min_sec(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return minutes, remaining_seconds

# Function to get video length for local video
def get_video_length(video_file):
    with open("temp_video.mp4", "wb") as f:
        f.write(video_file.getvalue())

    clip = VideoFileClip("temp_video.mp4")
    length_seconds = int(clip.duration)
    return length_seconds


def get_video_metadata(video_url):
    # Create a YouTube object with the provided video URL
    yt = YouTube(video_url)
    
    # Function to get the truncated description of the video
    def get_description():
        stream = yt.streams.first()
        desc = yt.description
        # Truncate description to 50 words
        desc_words = desc.split()[:50]
        truncated_desc = ' '.join(desc_words)
        return truncated_desc
    
    # Extract metadata
    metadata = {
        'title': yt.title,
        'duration': yt.length,
        'publish Date': yt.publish_date,
        'description': get_description(),
        'views': yt.views,
        # 'Is Age Restricted' : yt.age_restricted,
        'author': yt.author,
        # 'rating': yt.rating,
        'keywords': yt.keywords,
        # 'Thumbnail Url' : yt.thumbnail_url,
    }
    
    return metadata


def get_video_transcript(url):
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    clean_transcript = ''
    for x in transcript:
        sentence = x['text']
        clean_transcript += f' {sentence}'
    return transcript, clean_transcript


def transcribe_audio(audio_file, device="cpu", batch_size=2, compute_type="int8"):
    options = {
        "max_new_tokens": None,
        "clip_timestamps": None,
        "hallucination_silence_threshold": None,
    }
    
    audio = whisperx.load_audio(audio_file)
    model = whisperx.load_model("base", device, compute_type=compute_type, asr_options=options)
    
    transcript = model.transcribe(audio, batch_size=batch_size)
    segments = transcript.get('segments', [])  # Get the list of segments
    text_list = []  # Initialize an empty list to store the text from each segment
    
    # Iterate over each segment and extract the text
    for segment in segments:
        text = segment.get('text', '')  # Get the text from the segment
        text_list.append(text)  # Append the text to the list
    
    # Join the text from all segments into a single string
    clean_transcript = ' '.join(text_list)
    
    return transcript, clean_transcript

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

def search_dictionary_streamlit(video_url):
    # Get inputs from the user
    # video_url = st.text_input("Enter YouTube Video URL:")
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