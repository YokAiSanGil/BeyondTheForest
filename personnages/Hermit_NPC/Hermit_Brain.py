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

    # Construction du contexte
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
        # Fallback sur la mémoire globale volatile si pas de système de mémoire
        context_str = history

    # Construction du prompt dynamique
    current_system_prompt = f"{system_prompt}\nYou are speaking to {hero_name}.\n{lore_str}"
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

def generate_summary(conversation_text):
    """Génère un résumé de la conversation donnée."""
    if llm is None:
        return ""
    
    prompt = f"""Analyze the following conversation between a Player and The Hermit.
Summarize the key events and what The Hermit learned about the Player.
Keep it concise (2-3 sentences).

Conversation:
{conversation_text}

Summary:"""

    output = llm(
        prompt,
        max_tokens=150,
        temperature=0.6, # Plus bas pour être factuel
        stop=["Conversation:"],
        echo=False
    )
    return output["choices"][0]["text"].strip()
