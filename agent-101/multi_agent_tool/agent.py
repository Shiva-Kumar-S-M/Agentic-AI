import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, TOOL_DESCRIPTIONS

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = f"""You are a ReAct agent with access to multiple tools:
{TOOL_DESCRIPTIONS}

Pick ONLY the tool that matches the task. Do not use a tool if the question
doesn't need one — if you already know the answer, skip straight to Final Answer.

Follow this exact format, one step at a time:

Thought: reason about what to do next, including WHY you picked this tool
Action: tool_name
Action Input: the input to the tool

When you have the final answer, instead output:
Thought: I now know the answer
Final Answer: <answer>

Only ever output ONE Thought/Action/Action Input block, then STOP and wait for the Observation.
Never make up an Observation yourself.
"""


def call_llm(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        stop=["Observation:"],
    )
    return response.choices[0].message.content


def parse_action(text):
    action_match = re.search(r"Action:\s*(\w+)", text)
    input_match = re.search(r"Action Input:\s*(.+)", text)
    if action_match and input_match:
        return action_match.group(1).strip(), input_match.group(1).strip()
    return None, None


def run_agent(question, max_steps=6):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(max_steps):
        output = call_llm(messages)
        print(f"\n--- Step {step + 1} ---\n{output}")
        messages.append({"role": "assistant", "content": output})

        if "Final Answer:" in output:
            return output.split("Final Answer:")[-1].strip()

        tool_name, tool_input = parse_action(output)

        # --- Routing validation: check the tool actually exists BEFORE calling it ---
        if tool_name in TOOLS:
            try:
                observation = TOOLS[tool_name](tool_input)
            except Exception as e:
                observation = f"Error running '{tool_name}': {e}"
        else:
            observation = (
                f"Error: '{tool_name}' is not a valid tool. "
                f"Valid tools are: {list(TOOLS.keys())}"
            )

        print(f"Observation: {observation}")
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    return "Max steps reached without final answer."


if __name__ == "__main__":
    test_questions = [
        "What's the current time?",
        "Read the notes.txt file and tell me the budget.",
        "What is 45 times 12?",
        "What's the capital of Japan?",  # no tool needed — tests routing restraint
    ]

    for q in test_questions:
        print(f"\n{'=' * 50}\nQUESTION: {q}\n{'=' * 50}")
        answer = run_agent(q)
        print(f"\n=== FINAL ANSWER === {answer}")