import requests
import json

def generate_code_with_llama(prompt, model_version):
    print("Sending request to AI model...")
    url = "http://localhost:11434/api/generate"
    detailed_prompt = f"Generate a complete single-file HTML webpage that includes embedded CSS and JavaScript (if necessary) directly within the file. The page should follow the specifications provided by the user without any additional comments or narrative explanations.: {prompt}"
    payload = {
        "model": model_version,
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
    prompt = input(f"Enter your prompt for {model_dict[model_choice]}: ")
    model_version = model_dict.get(model_choice, "llama3:8b")  # Default to 'llama3:8b' if invalid input
    generated_code = generate_code_with_llama(prompt, model_version)
    if generated_code:
        code_only = filter_code_from_response(generated_code)
        save_code_to_file(code_only)

if __name__ == "__main__":
    main()
