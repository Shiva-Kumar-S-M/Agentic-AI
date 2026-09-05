import math

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

TOOLS = {
    "calculator": calculator,
    "get_word_length": get_word_length,
}

TOOL_DESCRIPTIONS = """
- calculator(expression: str): evaluates math like "12*7+3"
- get_word_length(word: str): returns number of letters in a word
"""