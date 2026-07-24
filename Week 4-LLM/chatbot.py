from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
# print(f"API Key Loaded: {api_key is not None}")
# print(api_key[:15] + "..." if api_key else "No key")



client = OpenAI(
    api_key = api_key,
    base_url = "https://openrouter.ai/api/v1"
)

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=[
            {
                "role" : "system",
                "content" : SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("\nAssistant:", response.choices[0].message.content)