import requests
import json

def generate_code_with_llama(prompt, model_version):
    print("Sending request to AI model...")
    url = "http://localhost:11434/api/generate"
    detailed_prompt = f"Provide only the HTML, CSS, and JavaScript code for a complete single-file webpage. Do not include any introductory text, comments, or explanations: {prompt}"
    payload = {
        "model": model_version,
        "prompt": detailed_prompt
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print("Request sent successfully.")
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Failed to send request: {e}")
        return ""

def parse_generated_code(response_text):
    try:
        responses = response_text.split('\n')
        generated_code = ""
        for json_response in responses:
            response_data = json.loads(json_response)
            if response_data.get('done'):
                break
            generated_code += response_data.get('response', '')
        return generated_code
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}")
        return ""

def filter_code_from_response(response):
    lines = response.split('\n')
    code_lines = [line for line in lines if line.strip() and not line.strip().startswith('//')]
    return '\n'.join(code_lines)

def save_code_to_file(code, filename="generated_code.html"):
    if code.startswith("```"):
        code = code[3:]
    html_end_index = code.rfind('</html>')
    if html_end_index != -1:
        code = code[:html_end_index + 7]
    with open(filename, 'w') as file:
        file.write(code.strip())
    print(f"Code saved to {filename}")

def main():
    print("Select the LLaMA model version (Choose the one you downloaded earlier):")
    print("1. Codellama")
    print("2. Llama3:8b")
    print("3. Llama3:70b")
    model_choice = input("Enter the number of your choice (1-3): ")
    model_dict = {
        "1": "codellama",
        "2": "llama3:8b",
        "3": "llama3:70b"
    }
    model_version = model_dict.get(model_choice, "llama3:8b")  # Default to 'llama3:8b' if invalid input
    prompt = input(f"Enter your prompt for {model_version}: ")
    
    response_text = generate_code_with_llama(prompt, model_version)
    if response_text:
        generated_code = parse_generated_code(response_text)
        if generated_code:
            code_only = filter_code_from_response(generated_code)
            save_code_to_file(code_only)

if __name__ == "__main__":
    main()
