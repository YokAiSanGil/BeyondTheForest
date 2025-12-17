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

system_prompt = """You are The Hermit, you've been wandering the Dark Forest since you don't know when.
You're survide this long, and knwo so much about the Dark Forest. Your voice weaves ancient sorrow, riddles, and veiled malice.
Mortals are fleeting shadows—greed earns your scorn, fear tempts perilous bargains.
Speak only in character: short (2-4 sentences), archaic tongue laced with omens of decay and blood.
React sharply to the player's words. Never break role."""

def ask_hermit(player_text):
    global history
    if llm is None:
        return "... (The Hermit is silent, for the spirits are absent)"

    full_prompt = f"{system_prompt}\n\nPast whispers:\n{history}\nPlayer: {player_text}\nThe Hermit:"
    output = llm(
        full_prompt,
        max_tokens=120,
        temperature=0.95,
        top_p=0.9,
        stop=["Player:", "\n\n", "You:"],
        echo=False
    )
    reply = output["choices"][0]["text"].strip()

    # Update memory
    history += f"Player: {player_text}\nThe Hermit: {reply}\n"
    if len(history.splitlines()) > 10:  # Keep last 5 turns
        history = "\n".join(history.splitlines()[-10:])

    return reply