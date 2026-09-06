
# Day 1 — Bare-Metal ReAct Agent

A from-scratch implementation of the ReAct (Reason + Act) agent loop, built
with no agent framework — just raw Python and the Groq API.

## What this teaches

- An "agent" is not code that runs itself. The LLM only emits text describing
  what it wants to do; Python parses that text, executes the real action, and
  feeds the result back in.
- Agent "memory" is just a growing list of messages, replayed to a stateless
  LLM on every call.
- `stop=["Observation:"]` prevents the model from hallucinating a fake tool
  result instead of waiting for the real one.
- Regex-based parsing is fragile by design here — motivates why later
  projects move to structured output / function calling.

## Setup

1. Get a free key from console.groq.com → API Keys → Create API Key.
2. Copy `.env.example` to `.env` and paste your key in.
3. `pip install -r requirements.txt`
4. `python agent.py`

## Example run

    --- Step 1 ---
    Thought: I need to find the number of letters in "artificial" before multiplying by 12.
    Action: get_word_length
    Action Input: artificial
    Observation: 10
    --- Step 2 ---
    Thought: I now know the answer
    Final Answer: 120

## Known limitations (explored more in later days)

- Regex parsing breaks if the model deviates from the exact format.
- The model sometimes skips tools it "should" use.
- No handling yet for zero-tool questions or unknown tools.