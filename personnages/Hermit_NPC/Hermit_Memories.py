import time

class HermitMemorySystem:
    def __init__(self, memory_dict):
        """
        Initialise le système de mémoire avec le dictionnaire de sauvegarde du héros.
        memory_dict: référence vers le dictionnaire 'npc_memories' de la sauvegarde.
        """
        self.memory = memory_dict
        
        # Initialisation de la structure si vide
        if "history" not in self.memory:
            self.memory["history"] = [] # Liste de tuples [user_text, npc_text, timestamp]
        if "summary" not in self.memory:
            self.memory["summary"] = "" # Résumé à long terme
        if "facts" not in self.memory:
            self.memory["facts"] = [] # Faits marquants (ex: "Player killed the Dragon")

    def add_interaction(self, user_text, npc_text):
        """Ajoute une interaction à la mémoire à court terme."""
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
        
        # Limite l'historique brut pour éviter de surcharger le fichier de sauvegarde
        # On garde les 20 derniers échanges (40 messages)
        if len(self.memory["history"]) > 40:
            self.memory["history"] = self.memory["history"][-40:]

    def get_context_window(self, max_turns=5):
        """
        Récupère les derniers échanges pour le prompt du LLM.
        Retourne une chaîne formatée.
        """
        history = self.memory["history"]
        # On prend les 2*max_turns derniers messages
        recent = history[-(max_turns*2):]
        
        context_str = ""
        for msg in recent:
            role = "Player" if msg["role"] == "user" else "The Hermit"
            context_str += f"{role}: {msg['content']}\n"
            
        return context_str

    def get_summary(self):
        """Retourne le résumé à long terme (si existant)."""
        return self.memory.get("summary", "")

    def update_summary(self, new_summary):
        """Met à jour le résumé (pourrait être appelé par un processus de 'dreaming' ou de compression)."""
        self.memory["summary"] = new_summary

    def add_fact(self, fact):
        """Ajoute un fait marquant."""
        if fact not in self.memory["facts"]:
            self.memory["facts"].append(fact)

    def get_facts_string(self):
        """Retourne les faits sous forme de liste à puces."""
        if not self.memory["facts"]:
            return ""
        return "Known facts:\n" + "\n".join([f"- {f}" for f in self.memory["facts"]])
