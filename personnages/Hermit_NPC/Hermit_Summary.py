from personnages.Hermit_NPC.Hermit_Brain import generate_summary

class HermitSummarizer:
    def __init__(self, memory_system):
        self.memory_system = memory_system

    def summarize_session(self, callback=None):
        """
        Récupère l'historique récent, génère un résumé et met à jour la mémoire.
        callback: Fonction à appeler une fois le résumé terminé (ex: sauvegarde).
        """
        # Récupérer l'historique brut de la session
        history = self.memory_system.memory.get("history", [])
        if not history:
            print("DEBUG: No history to summarize.")
            return

        # On ne résume que s'il y a eu des échanges récents
        conversation_text = ""
        for msg in history:
            role = "Player" if msg["role"] == "user" else "The Hermit"
            conversation_text += f"{role}: {msg['content']}\n"

        print("DEBUG: Generating summary...")
        # Générer le résumé
        current_summary = self.memory_system.get_summary()
        
        # Fusionner l'ancien résumé et la nouvelle conversation
        updated_summary = generate_summary(conversation_text, current_summary)
        
        if updated_summary:
            print(f"DEBUG: Summary generated: {updated_summary[:50]}...")
            self.memory_system.update_summary(updated_summary)
            # On efface l'historique brut pour ne garder que le résumé dans la sauvegarde
            self.memory_system.clear_history()
            
            if callback:
                print("DEBUG: Calling save callback...")
                callback()
        else:
            print("DEBUG: Summary generation returned empty string.")
