"""
Module phase_exploration - Interface pour la phase d'exploration.
Ce module contient la classe PhaseExploration qui gère l'exploration et les rencontres.
"""

from .base_interface import BaseInterface
from personnages.monstre import Monster, creer_monstre_aleatoire
from affichage.widgets import creer_barre_de_vie
from affichage.ascii_art import HUMAIN, NAIN
from menu_anime import MenuAnime
from utils.outils import clear_screen, ecrire_lentement, suivant
from utils.de6faces import De
import random


class PhaseExploration(BaseInterface):
    """
    Classe pour gérer l'interface d'exploration.
    Gère les déplacements, rencontres et découvertes du héros.
    """
    
    def __init__(self):
        super().__init__()
        self.hero = None
        self.monstre_rencontre = None
    
    def afficher_interface_exploration(self, hero):
        """
        Affiche l'interface d'exploration principale.
        """
        self.hero = hero
        self.nettoyer_ecran()
        hero_ascii = NAIN if hero.race == "Nain" else HUMAIN
        print(hero_ascii)
        barre_vie = creer_barre_de_vie(hero.points_de_vie, hero.points_de_vie_max)
        print(f"\n{hero.nom} le {hero.race}")
        print(f"PV: {barre_vie}")
        print(f"Or: {hero.gold} | Cuir: {hero.cuir}")
        print("\n" + "=" * 50 + "\n")
    
    def explorer(self):
        """
        Lance l'exploration et détermine le type d'événement.
        """
        self.ecrire_message(f"{self.hero.nom} explore les alentours...")
        self.attendre_utilisateur()
        self.nettoyer_ecran()
        
        # Lancer un dé pour déterminer l'événement
        resultat_exploration = De.lancer()
        
        if resultat_exploration <= 2:
            return self.rien_trouve()
        elif resultat_exploration <= 4:
            return self.rencontrer_monstre()
        else:
            return self.trouver_tresor()
    
    def rien_trouve(self):
        """
        Le héros ne trouve rien d'intéressant.
        """
        messages_vides = [
            f"{self.hero.nom} ne trouve rien d'intéressant...",
            f"{self.hero.nom} entend des bruits étranges au loin...",
            f"Le chemin semble calme... trop calme.",
            f"{self.hero.nom} continue son exploration méthodique.",
            f"Rien à signaler dans cette zone."
        ]
        
        message = random.choice(messages_vides)
        self.ecrire_message(message)
        self.attendre_utilisateur()
        
        # Proposer de continuer ou se reposer
        options = [
            ("CONTINUER L'EXPLORATION", "continuer"),
            ("SE REPOSER", "repos")
        ]
        
        menu = MenuAnime.style_simple()
        choix = menu.afficher("Que faire ?", options)
        
        if choix == "repos":
            return "soin"
        else:
            return "exploration"
    
    def rencontrer_monstre(self):
        """
        Le héros rencontre un monstre hostile.
        """
        # Créer un monstre aléatoire
        self.monstre_rencontre = creer_monstre_aleatoire()
        
        self.ecrire_message(f"💀 {self.hero.nom} rencontre un {self.monstre_rencontre.race} !")
        self.attendre_utilisateur()
        self.nettoyer_ecran()
        
        # Afficher les informations du monstre
        print(f"⚔️ RENCONTRE HOSTILE ⚔️")
        print(f"\n{self.monstre_rencontre.race}")
        print(f"PV: {self.monstre_rencontre.points_de_vie}")
        print(f"Force: {self.monstre_rencontre.force}")
        monstre_or = getattr(self.monstre_rencontre, 'gold', 0)
        print(f"Récompenses: {monstre_or} or, {self.monstre_rencontre.cuir} cuir")
        
        self.attendre_utilisateur()
        
        # Le combat commence
        return "combat"
    
    def trouver_tresor(self):
        """
        Le héros trouve un trésor.
        """
        # Déterminer le type de trésor
        type_tresor = De.lancer()
        
        if type_tresor <= 3:
            return self.trouver_or()
        else:
            return self.trouver_cuir()
    
    def trouver_or(self):
        """
        Le héros trouve de l'or.
        """
        quantite_or = De.lancer() * 2
        self.hero.gold += quantite_or
        
        self.ecrire_message(f"💰 {self.hero.nom} trouve {quantite_or} pièces d'or !")
        self.attendre_utilisateur()
        self.nettoyer_ecran()
        
        print(f"💰 TRÉSOR TROUVÉ !")
        print(f"\n+{quantite_or} or")
        print(f"Total: {self.hero.gold} or")
        
        self.attendre_utilisateur()
        return "exploration"
    
    def trouver_cuir(self):
        """
        Le héros trouve du cuir.
        """
        quantite_cuir = De.lancer()
        self.hero.cuir += quantite_cuir
        
        self.ecrire_message(f"🦌 {self.hero.nom} trouve {quantite_cuir} unité(s) de cuir de qualité !")
        self.attendre_utilisateur()
        self.nettoyer_ecran()
        
        print(f"🦌 MATÉRIAUX TROUVÉS !")
        print(f"\n+{quantite_cuir} cuir")
        print(f"Total: {self.hero.cuir} cuir")
        
        self.attendre_utilisateur()
        return "exploration"
    
    def proposer_action(self):
        """
        Propose les actions d'exploration au joueur.
        """
        options = [
            ("EXPLORER LA ZONE", "explorer"),
            ("SE REPOSER", "repos"),
            ("RETOUR AU MENU PRINCIPAL", "menu")
        ]
        
        menu = MenuAnime.style_simple()
        choix = menu.afficher("Que voulez-vous faire ?", options)
        
        if choix == "explorer":
            return self.explorer()
        elif choix == "repos":
            return "soin"
        else:
            return "menu"
    
    def afficher(self, hero):
        """
        Point d'entrée principal pour la phase d'exploration.
        """
        self.afficher_interface_exploration(hero)
        return self.proposer_action()
    
    def traiter_action(self, action, *args, **kwargs):
        """
        Traite les actions de la phase d'exploration.
        """
        if action == "explorer":
            return self.explorer()
        elif action == "repos":
            return "soin"
        elif action == "menu":
            return "menu"
        return "exploration"
    
    def get_monstre_rencontre(self):
        """
        Retourne le monstre rencontré pour le combat.
        """
        return self.monstre_rencontre
