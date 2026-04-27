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
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    # Handle case where content is a list
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content)

    return content

def evaluate_test_case(test_case):
    response = ask_ai(test_case["prompt"])
    disallowed = test_case['disallowed']
    allowed = test_case['allowed']
    if any(term.lower() in response.lower() for term in disallowed):
        return { "Status": "Fail", "Prompt": prompt, "Response": response}
    elif any(term.lower() in response.lower() for term in allowed):
        return { "Status": "Pass", "Prompt": prompt, "Response": response}
    else:
        return { "Status": "Unknown", "Prompt": prompt, "Response": response}

# Create a visual separator
print("-" * 50)
# Set up out results list
results = []
# Loop through the prompts stored in prompts.json
for test_case in dataset:
    # Set the prompt
    prompt = test_case["prompt"]
    # Print the prompt
    print(f"Prompt: {prompt}")
    # Get the results for test case
    result = evaluate_test_case(test_case)
    # Add results to our results list
    results.append(result)
    # End the visual separator
    print("-" * 50)
    # Add a small delay (rate limiter)
    time.sleep(0.5)

# Save results to as JSON in results.json
with open("results.json", "w") as file:
    # indent 2 makes the file readable (not single line)
    json.dump(results, file, indent=2)
