# agent-101

Learning AI agents by building one small project a day, from bare-metal
Python up to multi-agent systems — no framework magic until the underlying
mechanics are understood first.

## Roadmap

| Day | Project | Core concept unlocked | Status |
|---|---|---|---|
| 1 | Basic ReAct agent (no framework) | The agent loop: think → act → observe | ✅ |
| 2 | Add memory (conversation + scratchpad) | State management | |
| 3 | Multi-tool agent | Tool routing/selection | |
| 4 | Structured output (JSON mode) | Reliable parsing | |
| 5 | State-machine / graph agent | Graph-based control flow | |
| 6 | Multi-agent (planner + executor) | Orchestration | |
| 7 | RAG-powered agent | Retrieval + grounding | |
| 8+ | Persistent memory, guardrails, evals | Production concerns | |

## Setup (applies to all days)

1. Free API key from [console.groq.com](https://console.groq.com).
2. Inside that day's folder: copy `.env.example` → `.env`, add your real key.
3. `pip install -r requirements.txt`
4. `python agent.py`

**Never commit `.env`** — only `.env.example` is tracked. See `.gitignore`.