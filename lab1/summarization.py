# https://platform.openai.com/apps
import os
import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def fetch_webpage_content(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/112.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text.strip()

def summarize_text(input_text, max_length=100):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Summarize the following text in less than {max_length} words: '{input_text}'"}
        ]
    )
    summary = response.choices[0].message.content.strip()
    return summary

if __name__ == "__main__":
    url = "https://medium.com/@cognidownunder/openais-o1-vs-gpt-4o-a-deep-dive-into-ai-s-reasoning-revolution-fd9f7891e364"
    webpage_content = fetch_webpage_content(url)
    if not webpage_content:
        print("No content found on the webpage.")
    else:
        print("Webpage content fetched successfully.")
        summary = summarize_text(webpage_content)
        print("Summary:")
        print(summary)
