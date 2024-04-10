from youtube_transcript_api import YouTubeTranscriptApi

def get_video_transcript(url):
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    clean_transcript = ''
    for x in transcript:
        sentence = x['text']
        clean_transcript += f' {sentence}'
    return transcript, clean_transcript

url = 'https://www.youtube.com/watch?v=1DEtdr_oc9s'
print(url)
transcript, clean_transcript = get_video_transcript(url)
print(transcript, clean_transcript)
print(type(transcript))