import json
import os


class ConversationMemory:
    """
    Holds the long-term conversation history (user <-> agent),
    separate from any single question's scratchpad reasoning.
    Can persist to disk so memory survives across script runs.
    """

    def __init__(self, filepath="conversation_history.json"):
        self.filepath = filepath
        self.history = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.history, f, indent=2)

    def add_exchange(self, user_question, final_answer):
        self.history.append({"user": user_question, "agent": final_answer})
        self.save()

    def get_context_string(self, max_exchanges=5):
        """
        Returns the last N exchanges formatted as plain text,
        to be injected into the system prompt so the agent has
        conversational context without replaying every raw tool step.
        """
        recent = self.history[-max_exchanges:]
        if not recent:
            return "No previous conversation."
        lines = []
        for exchange in recent:
            lines.append(f"User asked: {exchange['user']}")
            lines.append(f"You answered: {exchange['agent']}")
        return "\n".join(lines)


class Scratchpad:
    """
    Holds the Thought/Action/Observation trail for ONE question only.
    Reset every time a new question starts — this is intentionally
    throwaway, unlike ConversationMemory.
    """

    def __init__(self):
        self.steps = []

    def add_step(self, role, content):
        self.steps.append({"role": role, "content": content})

    def get_messages(self):
        return self.steps

    def reset(self):
        self.steps = []