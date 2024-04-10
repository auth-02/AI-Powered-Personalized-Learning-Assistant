from youtube_transcript_api import YouTubeTranscriptApi
import urllib.request
import json
import urllib


VideoID = '1DEtdr_oc9s'

params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
url = "https://www.youtube.com/oembed"
query_string = urllib.parse.urlencode(params)
url = url + "?" + query_string

with urllib.request.urlopen(url) as response:
    response_text = response.read()
    data = json.loads(response_text.decode())
    print('Titel: ' + data['title'])
    

print(' ')


# retrieve the available transcripts
transcript_list = YouTubeTranscriptApi.list_transcripts(VideoID)

# iterate over all available transcripts
for transcript in transcript_list:

    # the Transcript object provides metadata properties
    print(
        #transcript.video_id,
        #transcript.is_generated,   
    )

    # fetch the actual transcript data
    # print(transcript.fetch())
    data = transcript.fetch()
    
# you can also directly filter for the language you are looking for, using the transcript list
transcript = transcript_list.find_transcript(['en'])  

user_input = input("Enter a word or sentence: ")
user_input = user_input.lower()

dictionary = data

def search_dictionary(user_input, dictionary):
    
    link = 'https://youtu.be/'

    for i in dictionary:
        i['text'] = i['text'].lower()


    for i in dictionary:

        try:
            if user_input in i['text']:
                
                for i in dictionary:
                    if user_input in i['text']:
                        
                        #I added -1 seconds to give the user a little more time 
                        print(str(i['text']) + '...' + ' ' + str( round(i['start'] // 60, 2)) + ' min' + ' und ' + str( round(i['start'] % 60, 0)) + ' sec' + ' ' + ':: ' + link + VideoID + '?t=' + str(int(i['start'] - 1)) + 's')
            
                break
            
        except:
            if user_input not in i['text']:
              print('Not Found')
  
    



search_dictionary(user_input, dictionary) 