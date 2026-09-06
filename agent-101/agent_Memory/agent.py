import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, TOOL_DESCRIPTIONS
from memory import ConversationMemory, Scratchpad

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT_TEMPLATE = """You are a ReAct agent with memory of past conversation.
You have access to these tools:
{tool_descriptions}

Relevant conversation history so far:
{conversation_context}

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
        stop=["Observation:"],
    )
    return response.choices[0].message.content


def parse_action(text):
    action_match = re.search(r"Action:\s*(\w+)", text)
    input_match = re.search(r"Action Input:\s*(.+)", text)
    if action_match and input_match:
        return action_match.group(1).strip(), input_match.group(1).strip()
    return None, None


def run_agent(question, conversation_memory, max_steps=6):
    scratchpad = Scratchpad()  # fresh scratchpad for THIS question only

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        tool_descriptions=TOOL_DESCRIPTIONS,
        conversation_context=conversation_memory.get_context_string(),
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    for step in range(max_steps):
        output = call_llm(messages)
        print(f"\n--- Step {step + 1} ---\n{output}")

        messages.append({"role": "assistant", "content": output})
        scratchpad.add_step("assistant", output)

        if "Final Answer:" in output:
            final_answer = output.split("Final Answer:")[-1].strip()
            conversation_memory.add_exchange(question, final_answer)
            return final_answer

        tool_name, tool_input = parse_action(output)
        if tool_name and tool_name in TOOLS:
            observation = TOOLS[tool_name](tool_input)
        else:
            observation = f"Error: unknown tool '{tool_name}'"

        print(f"Observation: {observation}")
        obs_message = f"Observation: {observation}"
        messages.append({"role": "user", "content": obs_message})
        scratchpad.add_step("user", obs_message)

    return "Max steps reached without final answer."


if __name__ == "__main__":
    memory = ConversationMemory()  # loads past history from disk if it exists

    print("Agent ready. Type 'exit' to quit.\n")
    while True:
        question = input("You: ")
        if question.strip().lower() == "exit":
            break
        answer = run_agent(question, memory)
        print(f"\n=== FINAL ANSWER ===\n{answer}\n")