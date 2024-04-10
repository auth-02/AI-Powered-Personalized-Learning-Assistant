import base64
import aiohttp
import asyncio
import json
import nest_asyncio

nest_asyncio.apply()

async def fetch(session, url, data):
    async with session.post(url, data=data) as response:
        return await response.text()

async def main(image_data=None, prompt="Expalin "):
    url = "http://8.12.5.48:11434/api/generate"
    data = json.dumps(
        {
            "model": "llava:7b-v1.6-mistral-q5_K_M",
            "prompt": prompt,
            "stream": False,
            "images": [image_data] if image_data else [],
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
        
question = "You are expert at explaining the concepts, you are tasked to explain the contents in great depth. Explain the concepts:"

def process_image(image_path=None, question = question):
    if image_path:
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        image_data = None  # Set image_data to None if no image provided

    response = asyncio.run(main(image_data, question))
    if response:
        response = json.loads(response)
        return response["response"]
    else:
        return None  # Handle case where no image or request fails


# Example usage with image
image_path = f"D:\\CODESPACES\\Hackathons\\Learner's Video - Analyser\\assets\\images\\Picture2.png"


result = process_image(image_path, question)

if result:
    print(result)
else:
    print("Error: Failed to process image.")


# Example usage without image
no_image_result = process_image(question)

if no_image_result:
    print(no_image_result)
else:
    print("No image provided, processing with a text prompt.")
