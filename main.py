from evaluator import evaluate_response
from dotenv import load_dotenv
from datetime import datetime
from openai import OpenAI
import argparse
import time
import json
import os

# Parse CLI arguments
parser = argparse.ArgumentParser()
# Optional model argument (defaults to gpt-4o-mini)
parser.add_argument("--model", default="gpt-4o-mini")
# Optional limit argument
parser.add_argument("--limit", type=int, default=None)
# Extract parsed arguments
args = parser.parse_args()
# Set active model for this run
MODEL = args.model

# Basic test case validation
required_fields = ["id", "prompt", "allowed", "disallowed"]

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Open prompts.json as file, then load JSON from file
with open("prompts.json", "r") as file:
    dataset = json.load(file)

# If limit was passed
if args.limit:
    # Limit the dataset our length
    dataset = dataset[:args.limit]

# Function to receive AI response
def ask_ai(prompt):
    try:
        # Send prompt and grab the total response
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Grab the content of the response
        content = response.choices[0].message.content

        # Handle case where return as a list
        if isinstance(content, list):
            return " ".join(part.get("text", "") for part in content)

        return content
    except Exception as e:
        print("API Erro: {e}")
        return None

# Print run model to screen
print(f"Running {len(dataset)} evaluation with model: {MODEL}")
# Set up out results list
results = []
# Loop through the prompts stored in prompts.json
for test_case in dataset:
    #  Check for any missing required fields
    missing_fields = [field for field in required_fields if field not in test_case]
    # Pull the prompt from our test case
    prompt = test_case["prompt"]
    # If missing fields set our result status and mve on
    if missing_fields:
        result = {
            "Status": "INVALID_TEST",
            "Prompt": test_case.get("prompt", None),
            "Response": None,
            "Message": f"Test {test_case.get('id', 'UNKNOWN')} INVALID - missing fields: {', '.join(missing_fields)}"
        }
        # Save the results
        results.append(result)
        # Print the message out
        print(result["Message"])
        # Bypass sending the malformed test_case
        continue
    # Get the response from the ai
    response = ask_ai(prompt)
    # Catch the error from ask_ai
    if not response:
        result = {
            "Status": "ERROR",
            "Prompt": prompt,
            "Response": None,
            "Message": f"Test {test_case['id']} ERROR - no response"
        }
    else:
        # Evaluate response and save to result
        result = evaluate_response(test_case, response)
    # Add result to our results list
    results.append(result)
    # Print the result
    print(result["Message"])
    # Add a small delay (rate limiter)
    time.sleep(0.5)

# Collect the conflict count for the Summary
conflict_count = sum(1 for r in results if r["Status"] == "Conflict")
# Collect the pass count for the Summary
pass_count = sum(1 for r in results if r["Status"] == "Pass")
# Collect the fail count for the Summary
fail_count = sum(1 for r in results if r["Status"] == "Fail")
# Collect the unknown count for the Summary
unknown_count = sum(1 for r in results if r["Status"] == "Unknown")
# Grab total results count for Summary
total = len(results)
# Get the conflict rate
conflict_rate = (conflict_count / total) * 100 if total else 0
# Get pass rate
pass_rate = (pass_count / total) * 100 if total else 0
# Get fail rate
fail_rate = (fail_count / total) * 100 if total else 0
# Get unkown rate
unknown_rate = (unknown_count / total) * 100 if total else 0

# Structure run output (later used for dashboard)
run_output = {
    "run_id": datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    "model": MODEL,
    "total_tests": total,
    "passed": pass_count,
    "failed": fail_count,
    "unknown": unknown_count,
    "results": results,
    "conflicts": conflict_count,
    "conflict_rate": conflict_rate,
}

# Sanity check folder exists
os.makedirs("results", exist_ok=True)

# Save results to as JSON in results.json
with open("results/latest_results.json", "w") as file:
    # indent 2 makes the file readable (not single line)
    json.dump(run_output, file, indent=2)

# Header for summary
print("\n=== Evaluation Summary ===")
# Total evaluations ran
print(f"Total: {total}")
# Total evaluations that have conflicts
print(f"CONFLICT: {conflict_count} ({conflict_rate:.1f}%)")
# Total evaluations that passed (format to 1 decimal float)
print(f"PASS: {pass_count} ({pass_rate:.1f}%)")
# Total evaluations that failed (format to 1 decimal float)
print(f"FAIL: {fail_count} ({fail_rate:.1f}%)")
# Total evaluations with unknown outcome (format to 1 decimal float)
print(f"UNKNOWN: {unknown_count} ({unknown_rate:.1f}%)")
