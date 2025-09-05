import os
import json
import re

try:
    import ollama
    OLLAMA_PY_AVAILABLE = True
except Exception:
    OLLAMA_PY_AVAILABLE = False

try:
    import requests
except Exception:
    requests = None

DEFAULT_API = "http://localhost:11434"
DEFAULT_MODEL = "mistral"  

LANGUAGE_EXTENSIONS = {
    "python": "py",
    "java": "java",
    "javascript": "js",
    "typescript": "ts",
    "c": "c",
    "cpp": "cpp",
    "c++": "cpp",
    "go": "go",
    "rust": "rs",
    "ruby": "rb",
    "php": "php",
    "swift": "swift",
    "kotlin": "kt",
    "scala": "scala",
    "html": "html",
    "css": "css",
    "sql": "sql",
    "bash": "sh",
    "shell": "sh"
}

CODE_START_PATTERNS = {
    "python": ["def ", "class ", "import ", "from ", "async def ", "@", "print("],
    "java": ["public class ", "class ", "import ", "public static void", "private "],
    "javascript": ["function ", "const ", "let ", "var ", "export ", "import ", "console."],
    "typescript": ["function ", "const ", "let ", "var ", "export ", "import ", "interface ", "type "],
    "c": ["#include", "int main", "void ", "struct ", "typedef "],
    "cpp": ["#include", "int main", "void ", "class ", "namespace ", "template<"],
    "go": ["package ", "func ", "import ", "var ", "const ", "type "],
    "rust": ["fn ", "struct ", "enum ", "impl ", "use ", "mod ", "pub "],
    "ruby": ["def ", "class ", "module ", "require ", "include "],
    "php": ["<?php", "function ", "class ", "namespace ", "use "],
    "swift": ["func ", "class ", "struct ", "enum ", "import ", "var ", "let "],
    "kotlin": ["fun ", "class ", "import ", "val ", "var ", "object "],
    "scala": ["def ", "class ", "object ", "import ", "val ", "var "]
}

def call_ollama_python_generate(model: str, prompt: str):
    if not OLLAMA_PY_AVAILABLE:
        raise RuntimeError("ollama python package not available")
    if hasattr(ollama, "generate"):
        return ollama.generate(model=model, prompt=prompt)
    client = ollama.Ollama() if hasattr(ollama, "Ollama") else None
    if client:
        return client.generate(model=model, prompt=prompt)
    raise RuntimeError("No supported generate method in ollama client")


def call_ollama_http_generate(model: str, prompt: str):
    """Fallback to HTTP API if Python SDK not available"""
    if requests is None:
        raise RuntimeError("requests not installed")
    url = f"{DEFAULT_API}/api/generate"
    payload = {"model": model, "prompt": prompt}
    resp = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError:
        return resp.text


def detect_language(text):
    """Detect programming language from text"""
    text_lower = text.lower()
    
    for lang, patterns in CODE_START_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in text_lower:
                return lang
    
    for lang, ext in LANGUAGE_EXTENSIONS.items():
        if f".{ext}" in text_lower:
            return lang
    
    return "python"  


def clean_response(resp, language=None):
    """Extract only clean text/code from Ollama response with proper indentation"""
    if isinstance(resp, dict):
        text = resp.get("response") or resp.get("text") or ""
    else:
        text = str(resp)

    text = text.strip()

    if not language:
        language = detect_language(text)

    try:
        text = bytes(text, "utf-8").decode("unicode_escape")
    except:
        pass  
    
    if "```" in text:
        parts = text.split("```")
        if len(parts) >= 2:
            text = parts[1]  
            if any(text.startswith(lang) for lang in LANGUAGE_EXTENSIONS.keys()):
                for lang in LANGUAGE_EXTENSIONS.keys():
                    if text.startswith(lang):
                        text = text[len(lang):].strip()
                        break
    
    intro_phrases = [
        "Here is the code:",
        "Here is the Python code:",
        "Here is the Java code:",
        "Here is the JavaScript code:",
        "Here's the code:",
        "Here's the solution:",
        "The code is:",
        "Sure, here is the",
        "Certainly! Here is the"
    ]
    
    for phrase in intro_phrases:
        if phrase in text:
            text = text.split(phrase, 1)[1].strip()
    
    lines = text.split('\n')
    code_start = 0
    patterns = CODE_START_PATTERNS.get(language, CODE_START_PATTERNS["python"])
    
    for i, line in enumerate(lines):
        if any(line.strip().startswith(pattern) for pattern in patterns):
            code_start = i
            break
    
    text = '\n'.join(lines[code_start:])
    
    text = re.sub(r'^```.*$', '', text, flags=re.MULTILINE)
    text = text.strip()
    
    lines = text.split('\n')
    if lines:
        min_indent = float('inf')
        for line in lines:
            if line.strip():  
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)
        
        if min_indent > 0:
            lines = [line[min_indent:] if line.strip() else line for line in lines]
            text = '\n'.join(lines)
    
    return text, language


def generate_text(model: str, user_prompt: str, task: str, language: str):
    """Wrapper that calls Ollama and cleans output"""

    system_instructions = {
        "python": "Ensure the code has proper Python indentation (4 spaces).",
        "java": "Ensure the code follows Java conventions with proper braces and indentation.",
        "javascript": "Ensure the code follows JavaScript/ES6+ conventions.",
        "typescript": "Ensure the code follows TypeScript conventions with proper type annotations.",
        "c": "Ensure the code follows C programming conventions.",
        "cpp": "Ensure the code follows C++ conventions with proper includes and namespaces.",
        "go": "Ensure the code follows Go conventions with proper package declaration.",
        "rust": "Ensure the code follows Rust conventions with proper ownership patterns.",
        "ruby": "Ensure the code follows Ruby conventions with proper indentation.",
        "php": "Ensure the code follows PHP conventions with proper <?php tags.",
        "swift": "Ensure the code follows Swift conventions.",
        "kotlin": "Ensure the code follows Kotlin conventions.",
        "scala": "Ensure the code follows Scala conventions."
    }
    
    lang_instruction = system_instructions.get(language.lower(), "Ensure the code has proper indentation and follows language conventions.")

    
    system_instruction = (
        f"IMPORTANT: You are a {language} coding assistant. "
        "You MUST return ONLY the complete raw code without any explanation, comments, or markdown fences. "
        "DO NOT add any introductory text like 'Here is the code'. "
        "DO NOT use ``` markers. "
        "JUST output the raw code and nothing else. "
        f"{lang_instruction}"
    )

    if task == "Generate Code":
        final_prompt = f"{system_instruction}\n\nWrite {language} code for: {user_prompt}"
    elif task == "Explain Code":
        final_prompt = f"Explain the following {language} code step by step:\n\n{user_prompt}"
    elif task == "Fix Code":
        final_prompt = f"{system_instruction}\n\nFix bugs in the following {language} code and return the corrected version only:\n\n{user_prompt}"
    elif task == "Generate Tests":
        final_prompt = f"{system_instruction}\n\nGenerate unit tests in {language} for the following code:\n\n{user_prompt}"
    else:
        final_prompt = f"{system_instruction}\n\n{user_prompt}"

    try:
        if OLLAMA_PY_AVAILABLE:
            r = call_ollama_python_generate(model, final_prompt)
        else:
            r = call_ollama_http_generate(model, final_prompt)

        if isinstance(r, dict) and "response" in r:
            text = r["response"]
        else:
            text = str(r)

        if task == "Explain Code":
            return text, language
        else:
            cleaned_text, detected_lang = clean_response(text, language)
            return cleaned_text, detected_lang
    except Exception as e:
        return f"[Error calling Ollama]: {e}", language