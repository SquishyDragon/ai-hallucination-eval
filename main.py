from dotenv import load_dotenv
from openai import OpenAI
import time
import json
import os

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Open prompts.json as file, then load JSON from file
with open("prompts.json", "r") as file:
    dataset = json.load(file)

# Function to receive AI response
def ask_ai(prompt):
    # Grab the response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Create a visual separator
print("-" * 50)

# Loop through the prompts stored in prompts.json
for test_case in dataset:
    # Set the prompt
    prompt = test_case["prompt"]
    # Print the prompt
    print(f"Prompt: {prompt}")
    # Set the response
    response = ask_ai(prompt)
    # Print the response
    print(f"Response: {response}")
    # End the visual separator
    print("-" * 50)
    # Add a small delay (rate limiter)
    time.sleep(0.5)
