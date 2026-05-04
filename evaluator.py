def evaluate_response(test_case, response):
    # Set constants
    prompt = test_case['prompt']
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
    # Check for a conflict first
    if matched_allowed and matched_disallowed:
        message = (
        f"Test {test_id} CONFLICT based on both allowed and disallowed matches. "
        f"Allowed: {', '.join(matched_allowed)} | "
        f"Disallowed: {', '.join(matched_disallowed)}"
        )

        return {
            "Status": "Conflict",
            "Prompt": prompt,
            "Response": response,
            "Passing Match": matched_allowed,
            "Failing Match": matched_disallowed,
            "Message": message
        }
    # Run our response against out disallowed behavior patterns to check for hallucination
    elif matched_disallowed:
        message = f"Test {test_id} FAILED based on behavior match: {', '.join(matched_disallowed)}"
        return { "Status": "Fail", "Prompt": prompt, "Response": response, "Failing Match": matched_disallowed, "Message": message }

    # Run our response against out allowed behavior patterns to check for no hallucination
    elif matched_allowed:
        message = f'Test {test_id} PASSED based on behavior match of "{", ".join(matched_allowed)}"'
        return { "Status": "Pass", "Prompt": prompt, "Response": response, "Passing Match": matched_allowed, "Message": message }

    # If response did not match behaviors for allowed or disallowed behaviors assign unknown status
    else:
        message = f"Test {test_id} UNKOWN based on no behavior matches"
        return { "Status": "Unknown", "Prompt": prompt, "Response": response, "Message": message}
