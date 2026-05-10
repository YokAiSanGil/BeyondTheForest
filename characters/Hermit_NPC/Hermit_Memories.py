import time
import json
import logging
import os

logger = logging.getLogger(__name__)

class HermitMemorySystem:
    def __init__(self, memory_dict):
        """
        Initialise the memory system with the hero's save dictionary.
        memory_dict: reference to the 'npc_memories' dictionary from the save file.
        """
        self.memory = memory_dict
        self.lore = self.load_lore()

        # Initialise structure if empty
        if "history" not in self.memory:
            self.memory["history"] = []  # List of entries [user_text, npc_text, timestamp]
        if "summary" not in self.memory:
            self.memory["summary"] = ""  # Long-term summary
        if "facts" not in self.memory:
            self.memory["facts"] = []  # Notable facts (e.g. "Player killed the Dragon")

    def load_lore(self):
        """Load static knowledge from the JSON file."""
        try:
            # Go up 3 levels: characters/Hermit_NPC/ -> root
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            lore_path = os.path.join(base_path, "assets", "TheHermit", "lore.json")
            if os.path.exists(lore_path):
                with open(lore_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading lore: {e}")
        return {}

    def get_lore_string(self):
        """Format the lore for the system prompt."""
        if not self.lore:
            return ""

        lore_str = "Ancient Knowledge:\n"
        if "world_history" in self.lore:
            lore_str += "\n".join(self.lore["world_history"]) + "\n"
        if "hermit_identity" in self.lore:
            lore_str += "\n".join(self.lore["hermit_identity"]) + "\n"
        return lore_str

    def add_interaction(self, user_text, npc_text):
        """Add an interaction to short-term memory."""
        timestamp = time.time()
        self.memory["history"].append({
            "role": "user",
            "content": user_text,
            "timestamp": timestamp
        })
        self.memory["history"].append({
            "role": "assistant",
            "content": npc_text,
            "timestamp": timestamp
        })

        # Limit raw history to avoid bloating the save file
        # Keep the last 20 exchanges (40 messages)
        if len(self.memory["history"]) > 40:
            self.memory["history"] = self.memory["history"][-40:]

    def get_context_window(self, max_turns=5):
        """
        Retrieve the most recent exchanges for the LLM prompt.
        Returns a formatted string.
        """
        history = self.memory["history"]
        # Take the last 2*max_turns messages
        recent = history[-(max_turns*2):]

        context_str = ""
        for msg in recent:
            role = "Player" if msg["role"] == "user" else "The Hermit"
            context_str += f"{role}: {msg['content']}\n"

        return context_str

    def get_summary(self):
        """Return the long-term summary (if it exists)."""
        return self.memory.get("summary", "")

    def update_summary(self, new_summary):
        """Update the summary (could be called by a 'dreaming' or compression process)."""
        self.memory["summary"] = new_summary

    def clear_history(self):
        """Clear the conversation history (after summarising)."""
        self.memory["history"] = []

    def add_fact(self, fact):
        """Add a notable fact."""
        if fact not in self.memory["facts"]:
            self.memory["facts"].append(fact)

    def get_facts_string(self):
        """Return facts as a bulleted list."""
        if not self.memory["facts"]:
            return ""
        return "Known facts:\n" + "\n".join([f"- {f}" for f in self.memory["facts"]])
