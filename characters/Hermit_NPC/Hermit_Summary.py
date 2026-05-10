from characters.Hermit_NPC.Hermit_Brain import generate_summary

class HermitSummarizer:
    def __init__(self, memory_system):
        self.memory_system = memory_system

    def summarize_session(self, callback=None):
        """
        Retrieve recent history, generate a summary, and update memory.
        callback: Function to call once the summary is done (e.g. save game).
        """
        # Retrieve raw session history
        history = self.memory_system.memory.get("history", [])
        if not history:
            print("DEBUG: No history to summarize.")
            return

        # Only summarise if there have been recent exchanges
        conversation_text = ""
        for msg in history:
            role = "Player" if msg["role"] == "user" else "The Hermit"
            conversation_text += f"{role}: {msg['content']}\n"

        print("DEBUG: Generating summary...")
        # Generate the summary
        current_summary = self.memory_system.get_summary()

        # Merge the previous summary with the new conversation
        updated_summary = generate_summary(conversation_text, current_summary)

        if updated_summary:
            print(f"DEBUG: Summary generated: {updated_summary[:50]}...")
            self.memory_system.update_summary(updated_summary)
            # Clear the raw history, keeping only the summary in the save file
            self.memory_system.clear_history()

            if callback:
                print("DEBUG: Calling save callback...")
                callback()
        else:
            print("DEBUG: Summary generation returned empty string.")
