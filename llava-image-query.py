import base64
import aiohttp
import asyncio
import json
import nest_asyncio

nest_asyncio.apply()

async def fetch(session, url, data):
    async with session.post(url, data=data) as response:  
        return await response.text()

async def main(image_data: str, prompt: str = "What is this image about?"):
    url = "http://8.12.5.48:11434/api/generate"  
    data = json.dumps(
        {
            "model": "llava:7b-v1.6-mistral-q5_K_M",
            "prompt": prompt,
            "stream": False,
            "images": [image_data]
        }
    )
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            response = await fetch(session, url, data)
            return response
        except (aiohttp.ClientError, asyncio.TimeoutError) as e: 
            print(f"Error making request: {e}")
            return None  

def process_image(image_path, question):
    
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    response = asyncio.run(main(image_data, question))
    if response: 
        response = json.loads(response)
        return response["response"]
    else:
        return None  


image_path = f"D:\\CODESPACES\\Hackathons\\Learner's Video - Analyser\\assets\\images\\Picture2.png"

question = "You are expert at explaing things, i want you to explaing the contents of the image to me in greath depth. expalin the contents of the image, what is in the image and all"

result = process_image(image_path, question)

if result:
    print(result)
else:
    print("Error: Failed to process image.")
