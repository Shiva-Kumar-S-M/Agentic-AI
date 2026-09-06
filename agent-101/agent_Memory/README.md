# Day 2 — Agent with Conversation Memory + Scratchpad

Builds on Day 1's ReAct loop by separating two kinds of memory that get
conflated by beginners:

- **Scratchpad** — the Thought/Action/Observation trail for one question.
  Thrown away after each answer.
- **ConversationMemory** — the user/agent exchange history across the whole
  session, persisted to `conversation_history.json` on disk.

## What this teaches

- Durable state (conversation memory, saved to disk) vs. disposable state
  (scratchpad, rebuilt every question) — a distinction every agent framework
  makes under different names (e.g. LangGraph checkpoints vs. node-local
  state).
- Injecting summarized history into the system prompt, rather than replaying
  every raw tool call from past questions — keeps prompts small as
  conversations grow.
- An interactive REPL loop instead of a single hardcoded call.

## Setup

1. Copy `.env.example` to `.env`, add your Groq key.
2. `pip install -r requirements.txt`
3. `python agent.py`
4. Ask a few related questions in a row, then type `exit`.
5. Run `python agent.py` again — notice it can reference earlier answers,
   because `conversation_history.json` persisted them.

## Try this

- Ask: "What's the length of 'python'?" then follow with: "multiply that by 5."
  Watch whether the agent uses conversation memory correctly to know what
  "that" refers to.
- Delete `conversation_history.json` and restart — confirm the agent has no
  memory of the earlier session.

## Known limitations

- `get_context_string()` just dumps the last 5 exchanges as raw text — no
  summarization or relevance filtering. A future day tackles smarter memory
  (retrieval-based memory, summarizing old turns instead of keeping raw text).