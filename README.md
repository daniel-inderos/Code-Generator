# Local Code Generator

## What is it?

The Local Code Generator leverages Ollama and a local AI model to automatically generate website code based on user prompts. The code is then saved to an HTML file.

## Requirements

- Ollama: to run the AI model. Available at [Ollama](https://ollama.com)
- Python: required to execute the script. Available at [Python](https://www.python.org)
- Additional Python libraries: `requests`, `tkinter`, `threading`

## How to Run

Follow these steps to get your website code generated:

1. **Install Python**: 
   - Download and install Python from [Python.org](https://www.python.org).

2. **Install Ollama**: 
   - Download and install Ollama from [Ollama.com](https://ollama.com).

3. **Set up Ollama**: 
   - Follow the instructions provided by Ollama after installation to properly set it up.

4. **Start Ollama**:
   - Open a terminal.
   - Execute the command: `ollama run` followed by the model you want to download and use (The model will start right after it is finished downloading).

5. **Install Required Python Libraries**:
   - Open a terminal or command prompt.
   - Run the following commands to install the necessary Python libraries:
     ```bash
     pip install requests
     pip install tk
     ```

6. **Download the Script**:
   - Download `main.py` from this GitHub repository.

7. **Run the Script**:
   - Open a new terminal window while leaving Ollama running.
   - Navigate to the directory where `main.py` is located.
   - Run `python main.py`.
   - A blue GUI should appear.

8. **Choose Your Model of Choice**:
   - Press the `Select Model` button, and a small window will open.
   - Choose your preferred model from the list. (More models will be added soon).
   - Click the white `Select` button below the model list.

9. **Input Your Prompt and Send it to the AI Model**:
   - In the prompt area labeled `Enter your prompt:`, enter what you want your website to be.
   - Click the `Generate Code` button.

10. **Wait for Generation**:
    - The code generation process will begin. This might take some time depending on the complexity of the prompt and the power of your computer.

11. **Save the Generated Code**:
    - After the code is generated, you will see it in a text block.
    - Click the `Save Code to File` button, then type the desired file name and choose the location where you want it to be saved.

## Additional Notes

- Make sure Ollama is running before executing the Python script.
- Ensure that you have a stable internet connection for downloading models and dependencies.
- The generated code will be a complete single-file HTML document including embedded CSS and JavaScript, ready for deployment.

## Recommended Models
- llama3
- codestral
- codegemma
- Gemma
- mistral
- codellama
