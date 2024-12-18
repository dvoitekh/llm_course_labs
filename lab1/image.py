import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def analyze_image(image_url):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
    )
    result = response.choices[0].message.content.strip()
    return result


if __name__ == "__main__":
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    analysis_result = analyze_image(image_url)
    print("Analysis Result:")
    print(analysis_result)
        