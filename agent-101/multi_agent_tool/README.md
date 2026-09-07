# Day 3 — Multi-Tool Agent (Tool Routing)

Extends the ReAct loop to 4 tools instead of 2, focused on **tool routing** —
how the model picks the right tool, and how the harness recovers when it
picks wrong.

## What this teaches

- Tool routing: giving the model several real options and observing how
  reliably it matches task → tool.
- Self-correcting error messages: when an invalid tool is requested, the
  Observation tells the model exactly what tools ARE valid, so it can retry
  correctly instead of the loop failing silently.
- Tool-use restraint: the system prompt explicitly tells the model to skip
  tools entirely when it already knows the answer — tested with a
  general-knowledge question that needs no tool at all.
- Basic security hygiene for file-access tools: `os.path.basename()` blocks
  path traversal (`../../etc/passwd`-style attacks) even in a toy sandbox.

  ## Setup

1. Copy `.env.example` to `.env`, add your Groq key.
2. `pip install -r requirements.txt`
3. Make sure `sandbox_files/notes.txt` exists (see repo).
4. `python agent.py`

Runs 4 built-in test questions automatically, each exercising a different
tool (or none at all).

## Try this

- Add a 5th tool yourself (e.g. `reverse_string`) and see if the model
  routes to it correctly on the first try without any prompt changes.
- Deliberately ask something ambiguous ("tell me about the file") and watch
  whether it guesses a filename or asks appropriately — this exposes how
  much tool descriptions matter for routing accuracy.

## Known limitations

- Routing relies entirely on the model reading tool descriptions correctly
  — no schema validation on inputs yet (Day 4 introduces structured/JSON
  output partly to fix this).
- Still regex-parsed action format, same fragility as Days 1–2.