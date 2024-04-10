import aiohttp
import asyncio
import json
import nest_asyncio
from youtube_transcript_api import YouTubeTranscriptApi

# Apply nest_asyncio
nest_asyncio.apply()

async def fetch(session, url, data):
    async with session.post(url, data=data, timeout=60) as response:
        return await response.json()

async def main(video_id, transcript, prompts):
    url = "http://8.12.5.48:11434/api/generate"
    
    # Combine all prompts
    full_prompt = ''.join(prompts) + transcript
    
    data = json.dumps(
        {
            "model": "llava:7b-v1.6-mistral-q5_K_M",
            "prompt": full_prompt,
            "stream": True,
            "video_id": video_id
        }
    )
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession(headers=headers) as session:
        response = await fetch(session, url, data)
        return response

# Function to get video transcript
def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    clean_transcript=''
    for x in transcript:
        sentence = x['text']
        clean_transcript += f' {sentence}\n'
    return transcript
    
# Example usage:
if __name__ == "__main__":
    url = 'https://www.youtube.com/watch?v=UCGaKvZpJYc'
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    transcript = get_transcript(video_id)
    
    # Define all prompts
    summary_prompt = "Provide a summary of the video based on the transcript:\n\n"
    tags_prompt = "Provide tags for the video based on the transcript:\n\n"
    topics_prompt = "Extract topics discussed in this video along with start time codes in seconds and minutes/seconds:\n\n"
    
    # Call main function with all prompts
    response = asyncio.run(main(video_id, transcript, [summary_prompt, tags_prompt, topics_prompt]))
    
    # Extract responses
    summary = response["response"][:len(summary_prompt)]  # Assuming the summary ends at the length of the summary prompt
    tags = response["response"][len(summary_prompt):len(summary_prompt) + len(tags_prompt)]  # Assuming tags start after the summary and end at the length of the tags prompt
    topics = response["response"][len(summary_prompt) + len(tags_prompt):]  # Assuming topics start after tags
    
    print('>>>SUMMARY:')
    print(summary)
    print('>>>TAGS:')
    print(tags)
    print('>>>TOPICS DISCUSSED:')
    print(topics)
