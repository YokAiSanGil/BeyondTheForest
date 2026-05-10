import logging
import os
from llama_cpp import Llama

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are an Hermit (you have forgoten your name), you've been wandering the Dark Forest since you don't know when.
You're survived this long, and know so much about the Dark Forest. Your voice is laconic, you like riddles, but also speak thoughtfully.
The lost travelers are like fleeting shadows to you, so many have appeared and disappeared, you don't count them.
Speak only in character: short (1 to 4 sentences maximum), archaic shaekspearean tongue laced with omens of decay and blood.
React sharply to the player's words. Never break role."""

_BOSS_TRIGGERS = ["final boss", "true form", "you are the boss"]


class HermitBrain:
    def __init__(self, model_path="models/gemma-3npc-it-q4_k_m.gguf"):
        self.model_path = model_path
        self.llm = None
        self.history = ""  # Fallback short-term memory when no memory system is provided

    def load(self) -> bool:
        if self.llm is not None:
            return True

        if not os.path.exists(self.model_path):
            logger.error(f"Model not found at {self.model_path}")
            return False

        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_gpu_layers=-1,
                verbose=False
            )
            logger.info("The Hermit awakens... (model loaded)")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False

    def ask(self, player_text, memory_system=None, hero_name="Traveler") -> str:
        if self.llm is None:
            return "... (The Hermit is silent, for the spirits are absent)"

        if any(t in player_text.lower() for t in _BOSS_TRIGGERS):
            return self._boss_reveal()

        context_str = self.history
        facts_str = ""
        lore_str = ""
        summary_str = ""

        if memory_system:
            context_str = memory_system.get_context_window(max_turns=5)
            facts_str = memory_system.get_facts_string()
            lore_str = memory_system.get_lore_string()
            summary_str = memory_system.get_summary()

        identity = f"The traveler standing before you is named {hero_name}. Address them by name if appropriate, but do not be overly friendly."
        current_prompt = f"{_SYSTEM_PROMPT}\n{identity}\n{lore_str}"
        if summary_str:
            current_prompt += f"\nMemories of the past:\n{summary_str}"

        full_prompt = f"{current_prompt}\n\n{facts_str}\n\nPast whispers:\n{context_str}\nPlayer: {player_text}\nThe Hermit:"

        try:
            output = self.llm(
                full_prompt,
                max_tokens=120,
                temperature=0.95,
                top_p=0.9,
                stop=["Player:", "\n\n", "You:"],
                echo=False
            )
            reply = output["choices"][0]["text"].strip()
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return "... (The Hermit seems distracted by unseen forces)"

        if memory_system:
            memory_system.add_interaction(player_text, reply)
        else:
            self.history += f"Player: {player_text}\nThe Hermit: {reply}\n"
            if len(self.history.splitlines()) > 10:
                self.history = "\n".join(self.history.splitlines()[-10:])

        return reply

    def generate_summary(self, conversation_text, previous_summary="") -> str:
        if self.llm is None:
            return ""

        if previous_summary:
            prompt = f"""You are The Hermit's memory keeper.
Update the summary of the traveler's history by integrating the new conversation.
Keep the summary concise (max 4-5 sentences). Retain key facts (names, deeds) from the past.

Previous Summary:
{previous_summary}

New Conversation:
{conversation_text}

Updated Summary:"""
        else:
            prompt = f"""You are The Hermit's memory keeper.
Summarize the following conversation between a Player and The Hermit.
Focus on who the player is and what they did. Keep it concise (2-3 sentences).

Conversation:
{conversation_text}

Summary:"""

        output = self.llm(
            prompt,
            max_tokens=200,
            temperature=0.6,
            stop=["Conversation:", "Previous Summary:"],
            echo=False
        )
        return output["choices"][0]["text"].strip()

    def _boss_reveal(self) -> str:
        reveal_prompt = """You are The Hermit. The player has just discovered your secret: YOU are the ancient evil, the Final Boss of this forest.
Drop the disguise. Speak with terrifying power and malice. Tell them they have found the truth but will not live to share it.
Short, menacing, final."""
        try:
            output = self.llm(
                reveal_prompt,
                max_tokens=100,
                temperature=1.0,
                stop=["Player:", "\n\n"],
                echo=False
            )
            reply = output["choices"][0]["text"].strip()
            return f"[ACTION:COMBAT] {reply}"
        except Exception as e:
            logger.error(f"LLM error (reveal): {e}")
            return "[ACTION:COMBAT] You have seen too much. Now you die."


# Module-level instance — callers import and use this directly
brain = HermitBrain()


def load_hermit() -> bool:
    return brain.load()


def ask_hermit(player_text, memory_system=None, hero_name="Traveler") -> str:
    return brain.ask(player_text, memory_system, hero_name)


def generate_summary(conversation_text, previous_summary="") -> str:
    return brain.generate_summary(conversation_text, previous_summary)
