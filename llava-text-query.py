import base64
import aiohttp
import asyncio
import json
import nest_asyncio

# Apply nest_asyncio
nest_asyncio.apply()

async def fetch(session, url, data):
    async with session.post(url, data=data) as response:  
        return await response.text()

async def main( prompt: str = "Explain about the topic?"):
    url = "http://8.12.5.48:11434/api/generate"  
    data = json.dumps(
        {
            "model": "llava:7b-v1.6-mistral-q5_K_M",
            "prompt": prompt,
            "stream": False,
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

def process_text(question):

    response = asyncio.run(main(question))
    if response:  
        response = json.loads(response)
        return response["response"]
    else:
        return None  

question = "You are expert at explaing things, i want you to explaing the concept to me in great depth about Elon Musk"

result = process_text(question)

if result:
    print(result)
else:
    print("Error: Failed to process image.")
