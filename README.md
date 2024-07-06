# Code Generator

## What is it?

The Code Generator is a versatile tool that leverages either Ollama with a local AI model or OpenAI's API to automatically generate website code based on user prompts. The generated code is then saved to an HTML file.

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
   cd code-generator
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
     - Tick the box that says "Use OpenAI".
     - Enter your OpenAI API Key in the provided field.
     - Click "Save API Key".
   - For Ollama (local AI):
     - Ensure the "Use OpenAI" box is unchecked.
     - Open a separate terminal and start Ollama with your chosen model:
       ```
       ollama run <model_name>
       ```

3. **Select your model**:
   - Click the "Select Model" button.
   - Choose your preferred model from the list.
   - Click the "Select" button to confirm.

4. **Generate code**:
   - In the prompt area labeled "Enter your prompt:", describe the website you want to create.
   - Click the "Generate Code" button.
   - Wait for the generation process to complete. This may take some time depending on the complexity of the prompt and the chosen model.

5. **Save the generated code**:
   - After generation, the code will appear in the text block.
   - Click the "Save Code to File" button.
   - Choose a file name and location to save the HTML file.

## Recommended Models

### Ollama Models
- llama3
- codestral
- codegemma
- Gemma
- mistral
- codellama

### OpenAI Models
- gpt-4o
- gpt-4-turbo
- gpt-4
- gpt-3.5-turbo

## Additional Notes

- Ensure you have a stable internet connection for downloading models, dependencies, and when using OpenAI's API.
- The generated code will be a complete single-file HTML document including embedded CSS and JavaScript, ready for deployment.
- If you're using Ollama, make sure it's running with your chosen model before generating code.
- The application uses a modern, dark-themed UI for a pleasant user experience.

## Troubleshooting

- If the "Save Code to File" button is not visible, try resizing the application window to reveal all elements.
- For issues with local models, ensure Ollama is properly installed and running with the selected model.
- If you encounter any Python-related errors, verify that all dependencies are correctly installed using the provided `requirements.txt` file.

## Contributing

Contributions to improve the Code Generator are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
