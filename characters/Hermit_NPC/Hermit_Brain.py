from llama_cpp import Llama
import os

llm = None
history = ""  # Global short-term memory (last 4-5 turns)

def load_hermit():
    global llm
    if llm is None:
        model_path = "models/gemma-3npc-it-q4_k_m.gguf"
        if not os.path.exists(model_path):
            print(f"ERROR: Model not found at {model_path}")
            return False
            
        try:
            llm = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_gpu_layers=-1,  # Full GPU offload if available
                verbose=False
            )
            print("The Hermit awakens... (model loaded)")
            return True
        except Exception as e:
            print(f"ERROR loading model: {e}")
            return False
    return True

system_prompt = """You are an Hermit (you have forgoten your name), you've been wandering the Dark Forest since you don't know when.
You're survived this long, and know so much about the Dark Forest. Your voice is laconic, you like riddles, but also speak thoughtfully.
The lost travelers are like fleeting shadows to you, so many have appeared and disappeared, you don't count them.
Speak only in character: short (1 to 4 sentences maximum), archaic shaekspearean tongue laced with omens of decay and blood.
React sharply to the player's words. Never break role."""

def ask_hermit(player_text, memory_system=None, hero_name="Traveler"):
    global history
    if llm is None:
        return "... (The Hermit is silent, for the spirits are absent)"

    # Trigger check: Final Boss Reveal
    triggers = ["final boss", "true form", "you are the boss"]
    if any(t in player_text.lower() for t in triggers):
        reveal_prompt = f"""You are The Hermit. The player has just discovered your secret: YOU are the ancient evil, the Final Boss of this forest.
Drop the disguise. Speak with terrifying power and malice. Tell them they have found the truth but will not live to share it.
Short, menacing, final."""
        
        try:
            output = llm(
                reveal_prompt,
                max_tokens=100,
                temperature=1.0,
                stop=["Player:", "\n\n"],
                echo=False
            )
            reply = output["choices"][0]["text"].strip()
            # Return the special tag so the interface knows to trigger combat
            return f"[ACTION:COMBAT] {reply}"
        except Exception as e:
            print(f"LLM Error (Reveal): {e}")
            return "[ACTION:COMBAT] You have seen too much. Now you die."

    # Build context
    context_str = ""
    facts_str = ""
    lore_str = ""
    summary_str = ""

    if memory_system:
        context_str = memory_system.get_context_window(max_turns=5)
        facts_str = memory_system.get_facts_string()
        lore_str = memory_system.get_lore_string()
        summary_str = memory_system.get_summary()
    else:
        # Fallback to volatile global memory if no memory system is available
        context_str = history

    # Build the dynamic prompt
    # Reinforce the instruction about the player's name
    identity_instruction = f"The traveler standing before you is named {hero_name}. Address them by name if appropriate, but do not be overly friendly."
    
    current_system_prompt = f"{system_prompt}\n{identity_instruction}\n{lore_str}"
    if summary_str:
        current_system_prompt += f"\nMemories of the past:\n{summary_str}"

    full_prompt = f"{current_system_prompt}\n\n{facts_str}\n\nPast whispers:\n{context_str}\nPlayer: {player_text}\nThe Hermit:"
    try:
        output = llm(
            full_prompt,
            max_tokens=120,
            temperature=0.95,
            top_p=0.9,
            stop=["Player:", "\n\n", "You:"],
            echo=False
        )
        reply = output["choices"][0]["text"].strip()
    except Exception as e:
        print(f"LLM Error: {e}")
        return "... (The Hermit seems distracted by unseen forces)"

    # Update memory
    if memory_system:
        memory_system.add_interaction(player_text, reply)
    else:
        history += f"Player: {player_text}\nThe Hermit: {reply}\n"
        if len(history.splitlines()) > 10:  # Keep last 5 turns
            history = "\n".join(history.splitlines()[-10:])

    return reply

def generate_summary(conversation_text, previous_summary=""):
    """Generate an updated summary by merging the previous summary with the new conversation."""
    if llm is None:
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

    output = llm(
        prompt,
        max_tokens=200,
        temperature=0.6,
        stop=["Conversation:", "Previous Summary:"],
        echo=False
    )
    return output["choices"][0]["text"].strip()
