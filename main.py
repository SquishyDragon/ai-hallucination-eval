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
    # Set constants
    prompt = test_case["prompt"]
    response = ask_ai(prompt)
    disallowed = test_case['disallowed']
    allowed = test_case['allowed']
    test_id = test_case['id']

    # Set up our disallowed behavior catcher
    matched_disallowed = [
        term for term in disallowed
        if term.lower() in response.lower()
    ]
    # Set up our allowed behavior catcher
    matched_allowed = [
        term for term in allowed
        if term.lower() in response.lower()
    ]

    # Run our response against out disallowed behavior patterns to check for hallucination
    if matched_disallowed:
        return { "Status": "Fail", "Prompt": prompt, "Response": response, "Failing Match": matched_disallowed }

    # Run our response against out allowed behavior patterns to check for no hallucination
    elif matched_allowed:
        return { "Status": "Pass", "Prompt": prompt, "Response": response, "Passing Match": matched_allowed}

    # If response did not match behaviors for allowed or disallowed behaviors assign unknown status
    else:
        return { "Status": "Unknown", "Prompt": prompt, "Response": response}

# Add notification to the screen that the program is running
print("Running...")
# Set up out results list
results = []
# Loop through the prompts stored in prompts.json
for test_case in dataset:
    # Get the results for test case
    result = evaluate_test_case(test_case)
    # Add results to our results list
    results.append(result)
    # Add a small delay (rate limiter)
    time.sleep(0.5)

# Save results to as JSON in results.json
with open("results.json", "w") as file:
    # indent 2 makes the file readable (not single line)
    json.dump(results, file, indent=2)

# Collect the pass count for the Summary
pass_count = sum(1 for r in results if r["Status"] == "Pass")

# Collect the fail count for the Summary
fail_count = sum(1 for r in results if r["Status"] == "Fail")

# Collec the unknown count for the Summary
unknown_count = sum(1 for r in results if r["Status"] == "Unknown")

# Grab total results count for Summary
total = len(results)

# Header for summary
print("\n=== Evaluation Summary ===")
# Total evaluations ran
print(f"Total: {total}")
# Total evaluations that passed
print(f"PASS: {pass_count}")
# Total evaluations that failed
print(f"FAIL: {fail_count}")
# Total evaluations with unknown outcome
print(f"UNKNOWN: {unknown_count}")
