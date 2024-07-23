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
AVAILABLE_LOCAL_MODELS = ["llama3.1", "llama3", "mistral", "gemma2", "mixtral", "codegemma", "codestral", "mistral-nemo"]
AVAILABLE_OPENAI_MODELS = ["gpt-4o", "gpt-4o-mini"]
CODE_TYPES = {
        "prompt": "Provide only the HTML, CSS, and JavaScript code for a complete single-file webpage. IMPORTANT: Do not include any introductory text, comments, or explanations.",
        "extension": ".html"
    },
    "Python": {
        "prompt": "Provide only the Python code for the following task. IMPORTANT: Do not include any introductory text, comments, or explanations.",
        "extension": ".py"
    },
    "Java": {
        "prompt": "Provide only the Java code for the following task. IMPORTANT: Do not include any introductory text, comments, or explanations.",
        "extension": ".java"
    },
    "C++": {
        "prompt": "Provide only the C++ code for the following task. IMPORTANT: Do not include any introductory text, comments, or explanations.",
        "extension": ".cpp"
    },
    "JavaScript": {
        "prompt": "Provide only the JavaScript code for the following task. IMPORTANT: Do not include any introductory text, comments, or explanations.",
        "extension": ".js"
    },
    "SQL": {
        "prompt": "Provide only the SQL code for the following task. IMPORTANT: Do not include any introductory text, comments, or explanations.",
        "extension": ".sql"
    }
}

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

        # Model and Code Type Selection Frame
        selection_frame = ttk.LabelFrame(main_frame, text="Model and Code Type Selection", padding="10")
        selection_frame.pack(fill=tk.X, pady=(0, 20))

        model_frame = ttk.Frame(selection_frame)
        model_frame.pack(fill=tk.X, pady=(0, 10))
        self.model_var = tk.StringVar()
        ttk.Label(model_frame, text="Selected Model:").pack(side=tk.LEFT)
        self.model_selected_label = ttk.Label(model_frame, textvariable=self.model_var, font=("Helvetica", 12, "bold"))
        self.model_selected_label.pack(side=tk.LEFT, padx=(10, 20))
        ttk.Button(model_frame, text="Select Model", command=self.open_model_selection, style='Outline.TButton').pack(side=tk.LEFT)

        code_type_frame = ttk.Frame(selection_frame)
        code_type_frame.pack(fill=tk.X)
        ttk.Label(code_type_frame, text="Code Type:").pack(side=tk.LEFT)
        self.code_type_var = tk.StringVar(value=list(CODE_TYPES.keys())[0])
        code_type_dropdown = ttk.Combobox(code_type_frame, textvariable=self.code_type_var, values=list(CODE_TYPES.keys()), state="readonly")
        code_type_dropdown.pack(side=tk.LEFT, padx=(10, 0))
        code_type_dropdown.bind("<<ComboboxSelected>>", self.on_code_type_change)

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
            ttk.Radiobutton(model_selection_window, text=model, value=model, variable=self.model_var, style='Toolbutton').pack(anchor=tk.W, padx=20, pady=5)

        ttk.Button(model_selection_window, text="Select", command=model_selection_window.destroy, style='Accent.TButton').pack(pady=10)

    def on_code_type_change(self, event):
        self.save_button.config(state=tk.DISABLED)
        self.code_display.delete(1.0, tk.END)

    def on_generate_code(self):
        prompt = self.prompt_entry.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt.")
            return

        code_type = self.code_type_var.get()
        model = self.model_var.get()
        if not model:
            messagebox.showwarning("Warning", "Please select a model.")
            return

        self.status_var.set("Generating code...")
        self.progress_bar.start()
        self.generate_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)

        threading.Thread(target=self.generate_code_thread, args=(prompt, code_type, model)).start()

    def generate_code_thread(self, prompt, code_type, model):
        code_type_info = CODE_TYPES[code_type]
        prompt = f"{code_type_info['prompt']} {prompt}"
        
        payload = {
            "prompt": prompt,
            "model": model,
            "api_key": self.config['api_key'] if self.config['use_openai'] else None
        }
        
        try:
            response = requests.post(self.config['api_url'], json=payload, stream=True)
            response.raise_for_status()
            
            generated_code = ""
            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line)
                        generated_code += json_response.get("response", "")
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse JSON: {e}")
                        print(f"Problematic line: {line}")
            
            filtered_code = self.filter_code_from_response(generated_code, code_type)
            
            self.master.after(0, self.display_generated_code, filtered_code)
        except requests.RequestException as e:
            self.master.after(0, messagebox.showerror, "Error", f"Failed to generate code: {str(e)}")
        finally:
            self.master.after(0, self.reset_ui_state)


    def filter_code_from_response(self, response, code_type):
        if code_type == "Website (HTML/CSS/JS)":
            return response  # Assume the response is a complete HTML file.
        lines = response.split("\n")
        code_lines = []
        for line in lines:
            if not line.strip().startswith("#"):  # Filter out comments.
                code_lines.append(line)
        return "\n".join(code_lines)

    def display_generated_code(self, code):
        self.code_display.delete(1.0, tk.END)
        self.code_display.insert(tk.END, code)
        self.save_button.config(state=tk.NORMAL)

    def on_save_code(self):
        code_type = self.code_type_var.get()
        extension = CODE_TYPES[code_type]["extension"]
        file_path = filedialog.asksaveasfilename(defaultextension=extension, filetypes=[(f"{code_type} files", f"*{extension}"), ("All files", "*.*")])
        if file_path:
            code = self.code_display.get("1.0", tk.END).strip()
            try:
                with open(file_path, "w") as file:
                    file.write(code)
                messagebox.showinfo("Success", f"Code saved successfully to {file_path}.")
            except IOError as e:
                messagebox.showerror("Error", f"Failed to save code: {str(e)}")

    def reset_ui_state(self):
        self.status_var.set("Ready")
        self.progress_bar.stop()
        self.generate_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()
