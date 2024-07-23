# Code Generator

## What is it?
The Code Generator is a versatile GUI application that leverages either local AI models through Ollama or OpenAI's API to automatically generate code based on user prompts. It supports multiple programming languages and can create complete websites or standalone code snippets.

## Features
- Support for both local AI models (via Ollama) and OpenAI's API
- Multiple programming language support (HTML/CSS/JS, Python, Java, C++, JavaScript, SQL)
- User-friendly GUI with dark theme
- Code syntax highlighting
- Easy model selection
- Progress indication during code generation
- Option to save generated code to file

## Requirements
- Python 3.7+: required to execute the script. Available at [Python](https://www.python.org)
- Additional Python libraries: See `requirements.txt`
- Ollama (optional): to run local AI models. Available at [Ollama](https://ollama.com)
- OpenAI API key (optional): for using OpenAI models

## Installation
1. **Install Python**: 
   - Download and install Python 3.7 or later from [Python.org](https://www.python.org).
2. **Clone the repository or download the script**:
   ```
   git clone https://github.com/daniel-inderos/Code-Generator.git
   cd Code-Generator
   ```
   Or download `main.py` and `requirements.txt` from this GitHub repository.
3. **Install Required Python Libraries**:
   - Open a terminal or command prompt in the project directory.
   - Run the following command to install the necessary Python libraries:
     ```bash
     pip install -r requirements.txt
     ```
4. **(Optional) Install Ollama**: 
   - If you plan to use local AI models, download and install Ollama from [Ollama.com](https://ollama.com).
   - Follow the instructions provided by Ollama after installation to properly set it up.

## How to Run
1. **Start the application**:
   - Open a terminal window.
   - Navigate to the directory containing `main.py`.
   - Run `python main.py`.
   - The Code Generator GUI should appear.

2. **Choose your AI provider**:
   - For OpenAI:
     - Check the "Use OpenAI" box.
     - Enter your OpenAI API Key in the provided field.
     - Click "Save API Key".
   - For Ollama (local AI):
     - Ensure the "Use OpenAI" box is unchecked.
     - The "Use Local Models" option should be automatically checked.
     - Open a separate terminal and start Ollama with your chosen model:
       ```
       ollama run <model_name>
       ```

3. **Select your model**:
   - Click the "Select Model" button.
   - Choose your preferred model from the list.
   - Click the "Select" button to confirm.

4. **Choose code type**:
   - Select the desired programming language or code type from the dropdown menu.

5. **Generate code**:
   - In the prompt area labeled "Enter your prompt:", describe the code you want to create.
   - Click the "Generate Code" button.
   - Wait for the generation process to complete. Progress will be indicated by the progress bar.

6. **Save the generated code**:
   - After generation, the code will appear in the text block with syntax highlighting.
   - Click the "Save Code to File" button.
   - Choose a file name and location to save the code file.

## Supported Code Types
- Website (HTML/CSS/JS)
- Python
- Java
- C++
- JavaScript
- SQL

## Available Models
### Local Models (Ollama)
- llama3.1
- llama3
- mistral
- gemma2
- mixtral
- codegemma
- codestral
- mistral-nemo

### OpenAI Models
- gpt-4o
- gpt-4o-mini

## Additional Notes
- The application uses a modern, dark-themed UI for a pleasant user experience.
- Generated code is displayed with syntax highlighting for better readability.
- The application saves your API settings in a `config.json` file for convenience.
- You can switch between OpenAI and local models at any time.

## Troubleshooting
- If any UI elements are not visible, try resizing the application window.
- For issues with local models, ensure Ollama is properly installed and running with the selected model.
- If you encounter any Python-related errors, verify that all dependencies are correctly installed using the provided `requirements.txt` file.
- If the code generation seems stuck, check your internet connection and ensure the chosen AI provider (Ollama or OpenAI) is accessible.

## Contributing
Contributions to improve the Code Generator are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
