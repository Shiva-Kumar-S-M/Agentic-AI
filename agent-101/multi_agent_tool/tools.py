import os
import datetime


def calculator(expression: str) -> str:
    """Evaluates a basic math expression safely."""
    try:
        allowed = "0123456789+-*/(). "
        if not all(c in allowed for c in expression):
            return "Error: invalid characters in expression"
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


def get_word_length(word: str) -> str:
    """Returns the length of a word."""
    return str(len(word))


def get_current_time(_: str = "") -> str:
    """Returns the current date and time. Input is ignored."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_local_file(filename: str) -> str:
    """Reads a text file from the local 'sandbox_files' folder."""
    safe_dir = os.path.join(os.path.dirname(__file__), "sandbox_files")
    filepath = os.path.join(safe_dir, os.path.basename(filename))  # prevent path traversal
    if not os.path.exists(filepath):
        return f"Error: file '{filename}' not found in sandbox_files/"
    with open(filepath, "r") as f:
        return f.read()


TOOLS = {
    "calculator": calculator,
    "get_word_length": get_word_length,
    "get_current_time": get_current_time,
    "read_local_file": read_local_file,
}

TOOL_DESCRIPTIONS = """
- calculator(expression: str): evaluates math like "12*7+3"
- get_word_length(word: str): returns number of letters in a word
- get_current_time(): returns today's date and time (input ignored, pass empty string)
- read_local_file(filename: str): reads a .txt file from the sandbox_files folder
"""