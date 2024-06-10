import requests
import json
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import os

# List of available models
available_models = ["llama3", "phi3", "aya", "mistral", "gemma", "mixtral", "llama2", "codegemma", "codestral"]

def generate_code_with_llama(prompt, model_version, url):
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

def load_config():
    config_path = 'config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    else:
        return {"api_url": "http://localhost:11434/api/generate"}

def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)

def open_model_selection():
    def on_select_model():
        selected_model = model_listbox.get(model_listbox.curselection())
        model_var.set(selected_model)
        model_selection_window.destroy()

    model_selection_window = tk.Toplevel(app)
    model_selection_window.title("Select Model")
    model_selection_window.configure(bg="#34495e")

    tk.Label(model_selection_window, text="Available Models", font=("Helvetica", 14), bg="#34495e", fg="#ecf0f1").pack(pady=10)
    model_listbox = tk.Listbox(model_selection_window, font=("Helvetica", 12), height=10, selectmode=tk.SINGLE, bg="#2c3e50", fg="#ecf0f1", selectbackground="#3498db")
    for model in available_models:
        model_listbox.insert(tk.END, model)
    model_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    tk.Button(model_selection_window, text="Select", command=on_select_model, font=("Helvetica", 12), bg="#3498db", fg="#ecf0f1").pack(pady=10)

def on_generate_code():
    model_version = model_var.get()
    prompt = prompt_entry.get("1.0", tk.END).strip()

    if not model_version or not prompt:
        messagebox.showwarning("Input Error", "Please select a model and enter a prompt.")
        return

    def run_generation():
        progress_bar.start()
        response_text = generate_code_with_llama(prompt, model_version, config['api_url'])
        progress_bar.stop()
        if response_text:
            generated_code = parse_generated_code(response_text)
            if generated_code:
                code_only = filter_code_from_response(generated_code)
                code_display.delete("1.0", tk.END)
                code_display.insert(tk.END, code_only)
                save_button.config(state=tk.NORMAL)

    threading.Thread(target=run_generation).start()

def on_save_code():
    code = code_display.get("1.0", tk.END).strip()
    if code:
        filename = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if filename:
            save_code_to_file(code, filename)

app = tk.Tk()
app.title("LLaMA Code Generator")
app.geometry("600x700")
app.configure(bg="#2c3e50")

config = load_config()

# Configure styles
style = ttk.Style(app)
style.theme_use("clam")
style.configure("TFrame", background="#2c3e50")
style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Helvetica", 12))
style.configure("TButton", background="#3498db", foreground="#ecf0f1", font=("Helvetica", 12))
style.configure("TText", font=("Courier New", 12), background="#34495e", foreground="#ecf0f1")
style.configure("TProgressbar", background="#3498db")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

tk.Label(frame, text="Select LLaMA Model Version:", foreground="#ecf0f1").grid(row=0, column=0, pady=5, sticky=tk.W)
model_var = tk.StringVar()
ttk.Button(frame, text="Select Model", command=open_model_selection).grid(row=1, column=0, pady=5, sticky=tk.W)
model_selected_label = ttk.Label(frame, textvariable=model_var)
model_selected_label.grid(row=2, column=0, pady=5, sticky=tk.W)

tk.Label(frame, text="Enter your prompt:", foreground="#ecf0f1").grid(row=3, column=0, pady=5, sticky=tk.W)
prompt_entry = tk.Text(frame, height=10, width=50, font=("Courier New", 12), wrap=tk.WORD, background="#34495e", foreground="#ecf0f1", insertbackground="#ecf0f1")
prompt_entry.grid(row=4, column=0, pady=5)

generate_button = ttk.Button(frame, text="Generate Code", command=on_generate_code)
generate_button.grid(row=5, column=0, pady=10, sticky=tk.W)

progress_bar = ttk.Progressbar(frame, mode='indeterminate')
progress_bar.grid(row=6, column=0, pady=10, sticky=(tk.W, tk.E))

code_display = tk.Text(frame, height=15, width=50, font=("Courier New", 12), wrap=tk.WORD, background="#34495e", foreground="#ecf0f1", insertbackground="#ecf0f1")
code_display.grid(row=7, column=0, pady=5)

save_button = ttk.Button(frame, text="Save Code to File", command=on_save_code, state=tk.DISABLED)
save_button.grid(row=8, column=0, pady=5, sticky=tk.W)

app.mainloop()
