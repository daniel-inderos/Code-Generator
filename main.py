import requests
import json
import tkinter as tk
from tkinter import messagebox, filedialog

def generate_code_with_llama(prompt, model_version):
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
        return response.text.strip()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to send request: {e}")
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
        messagebox.showerror("Error", f"Failed to decode JSON response: {e}")
        return ""

def filter_code_from_response(response):
    lines = response.split('\n')
    code_lines = [line for line in lines if line.strip() and not line.strip().startswith('//')]
    return '\n'.join(code_lines)

def save_code_to_file(code, filename):
    if code.startswith("```"):
        code = code[3:]
    html_end_index = code.rfind('</html>')
    if html_end_index != -1:
        code = code[:html_end_index + 7]
    with open(filename, 'w') as file:
        file.write(code.strip())
    messagebox.showinfo("Success", f"Code saved to {filename}")

def on_generate_code():
    model_choice = model_var.get()
    model_dict = {
        "Codellama": "codellama",
        "Llama3:8b": "llama3:8b",
        "Llama3:70b": "llama3:70b"
    }
    model_version = model_dict.get(model_choice)
    prompt = prompt_entry.get("1.0", tk.END).strip()

    if not model_version or not prompt:
        messagebox.showwarning("Input Error", "Please select a model and enter a prompt.")
        return

    response_text = generate_code_with_llama(prompt, model_version)
    if response_text:
        generated_code = parse_generated_code(response_text)
        if generated_code:
            code_only = filter_code_from_response(generated_code)
            filename = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
            if filename:
                save_code_to_file(code_only, filename)

app = tk.Tk()
app.title("LLaMA Code Generator")

model_var = tk.StringVar(value="Codellama")

tk.Label(app, text="Select LLaMA Model Version:").pack(pady=5)
models = ["Codellama", "Llama3:8b", "Llama3:70b"]
for model in models:
    tk.Radiobutton(app, text=model, variable=model_var, value=model).pack(anchor=tk.W)

tk.Label(app, text="Enter your prompt:").pack(pady=5)
prompt_entry = tk.Text(app, height=10, width=50)
prompt_entry.pack(pady=5)

tk.Button(app, text="Generate Code", command=on_generate_code).pack(pady=20)

app.mainloop()
