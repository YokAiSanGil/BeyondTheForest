from personnages.Hermit_NPC.Hermit_Brain import generate_summary

class HermitSummarizer:
    def __init__(self, memory_system):
        self.memory_system = memory_system

    def summarize_session(self):
        """
        Récupère l'historique récent, génère un résumé et met à jour la mémoire.
        """
        # Récupérer l'historique brut de la session
        history = self.memory_system.memory.get("history", [])
        if not history:
            return

        # On ne résume que s'il y a eu des échanges récents
        conversation_text = ""
        for msg in history:
            role = "Player" if msg["role"] == "user" else "The Hermit"
            conversation_text += f"{role}: {msg['content']}\n"

        # Générer le résumé
        new_summary_part = generate_summary(conversation_text)
        
        if not new_summary_part:
            return

        # Mettre à jour le résumé global
        current_summary = self.memory_system.get_summary()
        
        # Si le résumé devient trop long, on pourrait demander au LLM de le re-condenser
        # Pour l'instant, on ajoute simplement à la suite
        if current_summary:
            updated_summary = f"{current_summary}\n[New Encounter]: {new_summary_part}"
        else:
            updated_summary = f"[First Encounter]: {new_summary_part}"
            
        self.memory_system.update_summary(updated_summary)
