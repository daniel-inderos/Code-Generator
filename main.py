import requests
import json
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import os
from functools import partial
from ttkbootstrap import Style, PRIMARY, INFO, SUCCESS, WARNING, DANGER

# Constants
CONFIG_PATH = 'config.json'
AVAILABLE_LOCAL_MODELS = ["llama3", "aya", "mistral", "gemma", "gemma2", "mixtral", "llama2", "codegemma", "codestral"]
AVAILABLE_OPENAI_MODELS = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"]

class CodeGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Code Generator")
        self.master.geometry("800x900")
        
        self.style = Style(theme="darkly")
        self.master.configure(bg=self.style.colors.bg)

        self.config = self.load_config()
        self.setup_ui()

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as config_file:
                return json.load(config_file)
        return {"api_url": "http://localhost:11434/api/generate", "api_key": "", "use_openai": False}

    def save_config(self):
        with open(CONFIG_PATH, 'w') as config_file:
            json.dump(self.config, config_file)

    def setup_ui(self):
        main_frame = ttk.Frame(self.master, padding="20 20 20 0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Code Generator", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # API Settings Frame
        api_frame = ttk.LabelFrame(main_frame, text="API Settings", padding="10")
        api_frame.pack(fill=tk.X, pady=(0, 20))

        self.use_openai_var = tk.BooleanVar(value=self.config['use_openai'])
        ttk.Checkbutton(api_frame, text="Use OpenAI", variable=self.use_openai_var, command=self.on_toggle_openai, style='Switch.TCheckbutton').pack(anchor=tk.W)

        self.use_local_var = tk.BooleanVar(value=not self.config['use_openai'])
        self.use_local_checkbutton = ttk.Checkbutton(api_frame, text="Use Local Models", variable=self.use_local_var, command=self.on_toggle_local, style='Switch.TCheckbutton')
        self.use_local_checkbutton.pack(anchor=tk.W)

        api_key_frame = ttk.Frame(api_frame)
        api_key_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(api_key_frame, text="OpenAI API Key:").pack(side=tk.LEFT)
        self.api_key_entry = ttk.Entry(api_key_frame, show='*', width=40)
        self.api_key_entry.pack(side=tk.LEFT, padx=(10, 10))
        self.api_key_entry.insert(0, self.config['api_key'])
        self.api_key_save_button = ttk.Button(api_key_frame, text="Save API Key", command=self.on_save_api_key, style='Outline.TButton')
        self.api_key_save_button.pack(side=tk.LEFT)

        # Model Selection Frame
        model_frame = ttk.LabelFrame(main_frame, text="Model Selection", padding="10")
        model_frame.pack(fill=tk.X, pady=(0, 20))

        self.model_var = tk.StringVar()
        ttk.Label(model_frame, text="Selected Model:").pack(side=tk.LEFT)
        self.model_selected_label = ttk.Label(model_frame, textvariable=self.model_var, font=("Helvetica", 12, "bold"))
        self.model_selected_label.pack(side=tk.LEFT, padx=(10, 20))
        ttk.Button(model_frame, text="Select Model", command=self.open_model_selection, style='Outline.TButton').pack(side=tk.LEFT)

        # Prompt Entry Frame
        prompt_frame = ttk.LabelFrame(main_frame, text="Enter your prompt", padding="10")
        prompt_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.prompt_entry = tk.Text(prompt_frame, height=5, wrap=tk.WORD, font=("Courier New", 12))
        self.prompt_entry.pack(fill=tk.BOTH, expand=True)

        # Action Buttons Frame
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 20))

        self.generate_button = ttk.Button(action_frame, text="Generate Code", command=self.on_generate_code, style='Accent.TButton')
        self.generate_button.pack(side=tk.LEFT)

        self.save_button = ttk.Button(action_frame, text="Save Code to File", command=self.on_save_code, state=tk.DISABLED, style='Outline.TButton')
        self.save_button.pack(side=tk.LEFT, padx=(10, 0))

        self.progress_bar = ttk.Progressbar(action_frame, mode='indeterminate', length=200)
        self.progress_bar.pack(side=tk.RIGHT)

        # Code Display Frame
        code_frame = ttk.LabelFrame(main_frame, text="Generated Code", padding="10")
        code_frame.pack(fill=tk.BOTH, expand=True)

        self.code_display = tk.Text(code_frame, height=15, wrap=tk.NONE, font=("Courier New", 12))
        self.code_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        code_scrollbar = ttk.Scrollbar(code_frame, orient="vertical", command=self.code_display.yview)
        code_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.code_display.configure(yscrollcommand=code_scrollbar.set)

        # Status Bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.master, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.update_ui_state()

    def update_ui_state(self):
        openai_state = tk.NORMAL if self.config['use_openai'] else tk.DISABLED
        self.api_key_entry.config(state=openai_state)
        self.api_key_save_button.config(state=openai_state)
        local_state = tk.NORMAL if not self.config['use_openai'] else tk.DISABLED
        self.use_local_checkbutton.config(state=local_state)

    def on_toggle_openai(self):
        self.config['use_openai'] = self.use_openai_var.get()
        self.use_local_var.set(not self.config['use_openai'])
        self.update_ui_state()
        self.save_config()

    def on_toggle_local(self):
        self.config['use_openai'] = not self.use_local_var.get()
        self.use_openai_var.set(self.config['use_openai'])
        self.update_ui_state()
        self.save_config()

    def on_save_api_key(self):
        self.config['api_key'] = self.api_key_entry.get().strip()
        self.save_config()
        messagebox.showinfo("Success", "API key saved successfully.")

    def open_model_selection(self):
        model_selection_window = tk.Toplevel(self.master)
        model_selection_window.title("Select Model")
        model_selection_window.geometry("300x400")
        model_selection_window.configure(bg=self.style.colors.bg)

        ttk.Label(model_selection_window, text="Available Models", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        models = AVAILABLE_OPENAI_MODELS if self.config['use_openai'] else AVAILABLE_LOCAL_MODELS
        for model in models:
            ttk.Radiobutton(model_selection_window, text=model, value=model, variable=self.model_var).pack(anchor=tk.W, padx=20, pady=5)

        ttk.Button(model_selection_window, text="Select", command=model_selection_window.destroy, style='Accent.TButton').pack(pady=20)

    def on_generate_code(self):
        model_version = self.model_var.get()
        prompt = self.prompt_entry.get("1.0", tk.END).strip()

        if not model_version or not prompt:
            messagebox.showwarning("Input Error", "Please select a model and enter a prompt.")
            return

        self.generate_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.status_var.set("Generating code...")
        threading.Thread(target=self.run_generation, args=(model_version, prompt)).start()

    def run_generation(self, model_version, prompt):
        self.progress_bar.start()
        if self.config['use_openai']:
            response_text = self.generate_code_with_openai(prompt, model_version, self.config['api_key'])
        else:
            response_text = self.generate_code_with_llama(prompt, model_version, self.config['api_url'])
        self.progress_bar.stop()
        
        if response_text:
            code_only = self.filter_code_from_response(response_text)
            self.code_display.delete("1.0", tk.END)
            self.code_display.insert(tk.END, code_only)
            self.save_button.config(state=tk.NORMAL)
            self.status_var.set("Code generated successfully.")
        else:
            self.status_var.set("Failed to generate code.")
        
        self.generate_button.config(state=tk.NORMAL)

    def generate_code_with_llama(self, prompt, model_version, url):
        detailed_prompt = f"Provide only the HTML, CSS, and JavaScript code for a complete good-looking, single-file webpage. IMPORTANT: Do not include any introductory text, comments, or explanations. Do not include any formatting for the code, just the code as plain text: {prompt}"
        payload = {
            "model": model_version,
            "prompt": detailed_prompt
        }
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url, json=payload, headers=headers, stream=True)
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if 'response' in json_response:
                        full_response += json_response['response']
                    if json_response.get('done', False):
                        break
            
            return full_response.strip()
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to send request: {e}")
            return ""

    def generate_code_with_openai(self, prompt, model_version, api_key):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": model_version,
            "messages": [{"role": "system", "content": "Provide only the HTML, CSS, and JavaScript code for a complete single-file webpage. IMPORTANT: Do not include any introductory text, comments, or explanations."},
                         {"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to send request: {e}")
            return ""

    def filter_code_from_response(self, response):
        lines = response.split('\n')
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith('//')]
        return '\n'.join(code_lines)

    def on_save_code(self):
        code = self.code_display.get("1.0", tk.END).strip()
        if code:
            filename = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
            if filename:
                self.save_code_to_file(code, filename)

    def save_code_to_file(self, code, filename):
        if code.startswith("```"):
            code = code[3:]
        html_end_index = code.rfind('</html>')
        if html_end_index != -1:
            code = code[:html_end_index + 7]
        with open(filename, 'w') as file:
            file.write(code.strip())
        messagebox.showinfo("Success", f"Code saved to {filename}")
        self.status_var.set(f"Code saved to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()