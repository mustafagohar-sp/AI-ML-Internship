from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

# Create OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Initialize conversation history with the system prompt
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

# Chat loop
while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Store user's message
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Send the entire conversation history
    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=messages
    )

    # Get assistant response
    assistant_reply = response.choices[0].message.content

    # Display response
    print("\nAssistant:", assistant_reply)

    # Store assistant response
    messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )