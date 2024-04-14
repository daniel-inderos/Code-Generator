# Llama Code Generator

## What is it?

The Llama Code Generator leverages the Llama 2 AI model to automatically generate website code based on user prompts. The code is then saved to an HTML file.

## Requirements

- Ollama: to run the AI model. Available at [Ollama](https://ollama.com)
- Python: required to execute the script. Available at [Python](https://www.python.org)

## How to Run

Follow these steps to get your website code generated:

1. **Install Python**: Download and install Python from [Python.org](https://www.python.org).
2. **Install Ollama**: Download and install Ollama from [Ollama.com](https://ollama.com).
3. **Set up Ollama**: Follow the instructions provided by Ollama after installation to properly set it up.
4. **Start Ollama**:
   - Open a terminal.
   - Execute the command: `ollama run codellama`.
5. **Download the Script**:
   - Download `main.py` from this GitHub repository.
6. **Run the Script**:
   - Open a different terminal window.
   - Run `python main.py`.
7. **Input Your Prompt**:
   - When prompted with "Enter your prompt for LLaMA 2:", type your desired website specifics.
   - Press Enter.
8. **Wait for Generation**:
   - The code generation process will begin; this might take some time depending on the complexity of the prompt.
9. **Access Generated Code**:
   - Once completed, the `generated_code.html` file will be saved in the same directory where `main.py` is located.
