from pytube import YouTube

def get_video_metadata(video_url):
    # Create a YouTube object with the provided video URL
    yt = YouTube(video_url)
    
    # Function to get the description of the video
    def get_description():
        stream = yt.streams.first()
        desc = yt.description
        return desc
    
    # Extract metadata
    metadata = {
        'title': yt.title,
        'duration': yt.length,
        'publish_date': yt.publish_date,
        'description': get_description(),
        'views': yt.views,
        'Is Age Restricted' : yt.age_restricted,
        'author': yt.author,
        'rating': yt.rating,
        'keywords': yt.keywords,
        'Thumbnail Url' : yt.thumbnail_url,
    }
    
    return metadata

# Example usage:
video_url = 'https://youtu.be/TdzaYiXJ8D0?si=nwS5boy6kh6nk1E_'
metadata = get_video_metadata(video_url)
print("Metadata:", metadata)
