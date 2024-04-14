import requests
import json

def generate_code_with_llama(prompt):
    print("Sending request to LLaMA...")
    url = "http://localhost:11434/api/generate"
    detailed_prompt = f"Generate a complete single-file HTML webpage that includes CSS (and JavaScript if necessary) directly within the file. The page should meet the following specifications without any additional comments or narrative explanations: {prompt}"
    payload = {
        "model": "codellama",
        "prompt": detailed_prompt
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Request sent. Status code:", response.status_code)
        print("Raw response text:", response.text)  
    except Exception as e:
        print("Failed to send request:", e)
        return ""
    
    try:
        responses = response.text.strip().split('\n')
        generated_code = ""
        for json_response in responses:
            response_data = json.loads(json_response)
            if 'done' in response_data and response_data['done']:
                break
            generated_code += response_data.get('response', '')
        return generated_code
    except ValueError as e:
        print("JSON decoding failed:", e)
        return ""

        return ""

def filter_code_from_response(response):
    """
    Filter out only code from the response.
    This is a simple heuristic that might need adjustments based on actual output.
    """
    # Split the response by lines and filter out lines that are likely not code
    lines = response.split('\n')
    code_lines = [line for line in lines if line.strip() and not line.strip().startswith('//')]
    return '\n'.join(code_lines)

def save_code_to_file(code, filename="generated_code.html"):  # Changed to .html for appropriateness
    """
    Save the generated code to a file, removing triple backticks at the start and attempting to exclude any non-HTML content.
    """
    # Remove triple backticks at the start if present
    if code.startswith("```"):
        code = code[3:]

    # Attempt to isolate HTML content by only keeping everything up to the closing </html> tag
    html_end_index = code.rfind('</html>')
    if html_end_index != -1:
        # Include the length of '</html>' (7 characters) to keep the closing tag
        code = code[:html_end_index + 7]

    with open(filename, 'w') as file:
        file.write(code.strip())  # Use strip() to remove leading/trailing whitespace
    print(f"Code saved to {filename}")


def main():
    prompt = input("Enter your prompt for LLaMA 2: ")
    generated_code = generate_code_with_llama(prompt)
    if generated_code:
        # Filter out non-code parts from the response
        code_only = filter_code_from_response(generated_code)
        save_code_to_file(code_only)

if __name__ == "__main__":
    main()
