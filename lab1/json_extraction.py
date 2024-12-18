import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def extract_email_to_json(user_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You extract email addresses into JSON data."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "email_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "description": "The email address that appears in the input",
                            "type": "string"
                        }
                    },
                    "additionalProperties": False
                }
            }
        }
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    user_input = "Feeling stuck? Send a message to help@mycompany.com."
    print("User Input:")
    print(user_input)

    print("\nExtracted JSON Response:")
    json_response = extract_email_to_json(user_input)
    print(json_response)