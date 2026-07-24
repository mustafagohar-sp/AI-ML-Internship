from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT
import os
import json

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
try:
    with open("history.json", "r") as file:
        messages = json.load(file)

except (FileNotFoundError, json.JSONDecodeError):
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

    # Handle /student command
    if user_input.startswith("/student"):

        parts = user_input.split()

        if len(parts) != 3:
            print("Usage: /student <name> <marks>")
            continue

        name = parts[1]

        try:
            marks = int(parts[2])
        except ValueError:
            print("Marks must be a number.")
            continue

        if marks >= 90:
            grade = "A"
        elif marks >= 80:
            grade = "B"
        elif marks >= 70:
            grade = "C"
        elif marks >= 60:
            grade = "D"
        else:
            grade = "F"

        student = {
            "name": name,
            "marks": marks,
            "grade": grade
        }

        print(json.dumps(student, indent=4))
        continue

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

    with open("history.json", "w") as file:
        json.dump(messages, file, indent=4)