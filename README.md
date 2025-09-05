Multi-Language Code Assistant
A Streamlit-based web application that leverages Ollama's Mistral model to generate, explain, fix, and test code across multiple programming languages.

Features
Multi-Language Support: Python, Java, JavaScript, TypeScript, C, C++, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, HTML, CSS, SQL, Bash

Code Generation: Generate code from natural language descriptions

Code Explanation: Get step-by-step explanations of existing code

Code Fixing: Identify and fix bugs in your code

Test Generation: Generate unit tests for your code

Clean Output: Always get clean, properly formatted code without explanations

Local Processing: Runs entirely on your local machine with Ollama

Installation
Prerequisites
Python 3.8+ installed on your system

Ollama installed and running

Mistral model pulled in Ollama

Install Ollama
bash
# On macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# On Windows
# Download from https://ollama.ai/download
Pull Mistral Model
bash
ollama pull mistral
Install Python Dependencies
bash
pip install streamlit requests
Project Structure
text
code-assistant/
├── app.py              # Streamlit web application
├── ollama_helper.py    # Ollama integration and utilities
└── README.md          # This file
Usage
Running the Application
Start Ollama (if not already running):

bash
ollama serve
Run the Streamlit app:

bash
streamlit run app.py
Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

Using the Application
Select Task: Choose from Generate Code, Explain Code, Fix Code, or Generate Tests

Choose Language: Select your target programming language

Input:

For code generation: Enter a natural language description

For other tasks: Paste your existing code

Run: Click "Run Task" to process your request

🛠️ Supported Languages
Language	Extension	Status
Python	.py	 Full support
Java	.java	 Full support
JavaScript	.js	 Full support
TypeScript	.ts	 Full support
C	.c	 Full support
C++	.cpp	 Full support
Go	.go	 Full support
Rust	.rs	 Full support
Ruby	.rb	 Full support
PHP	.php	Full support
Swift	.swift	Full support
Kotlin	.kt	Full support
Scala	.scala	Full support
HTML	.html	Full support
CSS	.css	Full support
SQL	.sql	Full support
Bash	.sh	Full support
Examples
Code Generation
Input: "Create a function that reverses a string"
Language: Python
Output: Clean Python code without explanations

Code Explanation
Input: Existing code snippet
Output: Detailed step-by-step explanation

Code Fixing
Input: Buggy code
Output: Corrected code with bugs fixed

Test Generation
Input: Existing function
Output: Unit tests for the function

Configuration
Default Settings
Model: mistral

Ollama API: http://localhost:11434

Default Language: Python

Customization
You can modify these settings in the sidebar of the web application or directly in the code:

Change default model in DEFAULT_MODEL variable

Modify API endpoint in DEFAULT_API variable

Add new languages in LANGUAGE_EXTENSIONS and CODE_START_PATTERNS

🔧 Troubleshooting
Common Issues
Ollama not running:

bash
# Start Ollama service
ollama serve
Model not found:

bash
# Pull the required model
ollama pull mistral
Port already in use:

bash
# Run on different port
streamlit run app.py --server.port 8502
Import errors:

bash
# Install missing packages
pip install streamlit requests
Performance Tips
Use simpler prompts for faster responses

For large codebases, process smaller chunks

Ensure adequate system resources for Ollama

Contributing
Feel free to contribute by:

Adding support for more programming languages

Improving the code detection algorithms

Enhancing the UI/UX

Adding new features

License
This project is open source and available under the MIT License.

Acknowledgments
Ollama for providing the local LLM infrastructure

Mistral AI for the powerful language model

Streamlit for the easy-to-use web framework

Support
If you encounter any issues or have questions:

Check the troubleshooting section above

Ensure Ollama is properly installed and running

Verify the Mistral model is downloaded

Check that all Python dependencies are installed

For additional help, please open an issue in the project repository.

Note: This application runs entirely on your local machine. No code or data is sent to external servers, ensuring complete privacy and security.