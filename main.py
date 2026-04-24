from prompts import test_prompts
from dotenv import load_dotenv
from openai import OpenAI
import time
import os

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to recieve AI response
def ask_ai(prompt):
    #  Grab the response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Create a visual serperator
print("-" * 50)

# Loop through the promtps stored in prompts.py
for prompt in test_prompts:
    # Print the prompt
    print("Prompt: " + prompt)
    # print the response
    print("Response: " + ask_ai(prompt))
    # End the visual seperator
    print("-" * 50)
    # Add a small delay (rate limiter)
    time.sleep(0.5)
