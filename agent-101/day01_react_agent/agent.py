import os
import re
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, TOOL_DESCRIPTIONS

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = f"""You are a ReAct agent. You have access to these tools:
{TOOL_DESCRIPTIONS}

Follow this exact format, one step at a time:

Thought: reason about what to do next
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
        stop=["Observation:"]  # critical: stop before model hallucinates the tool result
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
        print(f"\n--- Step {step+1} ---\n{output}")
        messages.append({"role": "assistant", "content": output})

        if "Final Answer:" in output:
            return output.split("Final Answer:")[-1].strip()

        tool_name, tool_input = parse_action(output)
        if tool_name and tool_name in TOOLS:
            observation = TOOLS[tool_name](tool_input)
        else:
            observation = f"Error: unknown tool '{tool_name}'"

        print(f"Observation: {observation}")
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    return "Max steps reached without final answer."

if __name__ == "__main__":
    result = run_agent("What is the length of the word 'python' plus the length of the word 'agent', all multiplied by 3?")
    print(f"\n=== FINAL ANSWER ===\n{result}")