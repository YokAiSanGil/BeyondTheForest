"""
Module phase_exploration - Interface pour la phase d'exploration.
Ce module contient la classe PhaseExploration qui gère l'exploration et les rencontres.
"""

from .base_interface import BaseInterface
from personnages.monstre import Monster, creer_monstre_aleatoire
from affichage.widgets import creer_barre_de_vie
from affichage.ascii_art import HUMAIN, NAIN
from affichage.menu_anime import MenuAnime
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
    


    def explorer(self):
        """
        Lance l'exploration et détermine le type d'événement.
        """
        if not self.hero:
            return "menu"
            
        # Lancer un dé pour déterminer l'événement
        resultat_exploration = De.lancer()
        
        if resultat_exploration == 1:
            return self.rencontrer_monstre()
        elif resultat_exploration == 2:
            return self.trouver_tresor()
        else:
            # Plus de chances d'avoir des messages d'exploration (4-6 sur 6)
            self.afficher_message_exploration()
            # ✨ IMPORTANT : Retourner "exploration" pour continuer la boucle
            return "exploration"

    def afficher_message_exploration(self):
        """
        Affiche un message d'exploration avec le menu en dessous.
        """
        # ✨ AFFICHER LE MESSAGE PUIS LE MENU EN DESSOUS
        self.nettoyer_ecran()
        
        # Afficher le message d'exploration
        self.message_exploration_aleatoire()
        
        # ✨ NE PAS RETOURNER IMMÉDIATEMENT - Le menu s'affichera après

    def message_exploration_aleatoire(self):
        """
        Affiche un message d'exploration aléatoire.
        """
        messages = [
            "Vous avancez prudemment dans la forêt...",
            "Les arbres murmurent des secrets anciens...",
            "Vos pas résonnent sur le sol moussu...",
            "Une brise mystérieuse caresse votre visage...",
            "Vous sentez une présence dans l'ombre...",
            "La forêt semble vivante, chaque bruit attire votre attention...",
            "Vous entendez le chant des oiseaux au loin...",
            "Un léger brouillard enveloppe les arbres...",
            "Vous marchez sur un tapis de feuilles mortes...",
            "Un craquement dans les buissons vous fait sursauter...",
            "Vous avez l'impression d'être observé...",
            "Un sanglier passe à proximité.",
            "Vous continuez à avancer, le cœur battant...",
            "Un sanglier passe à proximité, vous avez le ventre qui gargouille...",
            "Des chants portés par le vent traversent la forêt obscure.",
            "Vous avez l'impression d'être déjà passé par ici...",
            "Un bruit étrange attire votre attention...",
            "Vous entendez le murmure d'une rivière au loin...",
            "L'odeur de la terre humide remplit vos narines...",
            "Vous entendez le bruit de vos propres pas sur les feuilles mortes...",
            "Une toile d'araignée scintille de rosée dans un rayon de soleil...",
            "Un papillon coloré volette devant vous avant de disparaître...",
            "Vous remarquez des traces de pas dans la terre meuble...",
            "Le vent fait danser les feuilles au-dessus de votre tête...",
            "Une branche craque quelque part derrière vous...",
            "L'écho de vos pas se perd dans l'immensité de la forêt..."
        ]
        
        # Ajouter des messages personnalisés avec le nom du héros si disponible
        if self.hero:
            messages.extend([
                f"{self.hero.nom} scrute les alentours avec attention...",
                f"{self.hero.nom} ressent une étrange énergie dans l'air...",
                f"{self.hero.nom} remarque de curieuses empreintes dans la boue...",
                f"{self.hero.nom} s'arrête un instant pour écouter...",
                f"{self.hero.nom} contourne prudemment un buisson épineux..."
            ])
        
        message = random.choice(messages)
        print(f"\n🌲 {message}")
        
        # Parfois, ajouter une seconde chance de trouver quelque chose
        chance_seconde = De.lancer()
        if chance_seconde == 6:  # 1 chance sur 6
            self.petit_bonus()
    
    def petit_bonus(self):
        """
        Petit bonus occasionnel lors de l'exploration.
        """
        if not self.hero:
            return
            
        bonus = De.lancer()
        if bonus <= 3:
            # Petit bonus d'or
            or_bonus = De.lancer()
            self.hero.gold += or_bonus
            print(f"✨ Bonus ! +{or_bonus} or trouvé en fouillant.")
        else:
            # Message d'ambiance sans récompense
            messages_bonus = [
                "Vous trouvez un champignon coloré, mais vous préférez ne pas y toucher.",
                "Une luciole brille un instant puis disparaît.",
                "Vous entendez un hibou au loin."
            ]
            import random
            print(f"{random.choice(messages_bonus)}")

    def proposer_action(self):
        """
        Propose les actions d'exploration au joueur avec un menu horizontal simple.
        """
        # Options du menu
        options = [
            ("EXPLORER", "explorer"),
            ("SAC", "sac"),
            ("QUITTER", "quitter")
        ]
        
        # ✨ NE PAS NETTOYER L'ÉCRAN ICI si un message vient d'être affiché
        # L'écran a déjà été nettoyé dans afficher_message_exploration()
        
        print()  # Ligne vide entre le message et le menu
        
        # Créer et utiliser le menu horizontal simple
        menu = MenuAnime.style_exploration()
        resultat = menu.afficher("", options)
        
        if resultat == "explorer":
            return self.explorer()
        elif resultat == "sac":
            self.nettoyer_ecran()
            print("🎒 Fonctionnalité du sac à venir...")
            self.attendre_utilisateur()
            return "exploration"
        elif resultat == "quitter":
            return "menu"
        else:
            return "exploration"

    def rencontrer_monstre(self):
        """
        Le héros rencontre un monstre hostile.
        """
        if not self.hero:
            return "menu"
            
        # Créer un monstre aléatoire
        self.monstre_rencontre = creer_monstre_aleatoire()
        self.nettoyer_ecran()
        # ✨ PLUS D'ATTENTE ! Retour direct au combat
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
        if not self.hero:
            return "exploration"
            
        quantite_or = De.lancer() * 2
        self.hero.gold += quantite_or
        
        # ✨ PAS D'INTERFACE, JUSTE LE MESSAGE SANS ATTENTE
        self.nettoyer_ecran()
        print(f"💰 {self.hero.nom} trouve {quantite_or} pièces d'or !")
        print(f"   (Total: {self.hero.gold} or)")
        
        # ✨ PLUS D'ATTENTE ! Retour direct à l'exploration
        return "exploration"
    
    def trouver_cuir(self):
        """
        Le héros trouve du cuir.
        """
        if not self.hero:
            return "exploration"
            
        quantite_cuir = De.lancer()
        self.hero.cuir += quantite_cuir
        
        # ✨ PAS D'INTERFACE, JUSTE LE MESSAGE SANS ATTENTE
        self.nettoyer_ecran()
        print(f"🦌 {self.hero.nom} trouve {quantite_cuir} unité(s) de cuir de qualité !")
        print(f"   (Total: {self.hero.cuir} cuir)")
        
        # ✨ PLUS D'ATTENTE ! Retour direct à l'exploration
        return "exploration"

    def afficher(self, hero):
        """
        Point d'entrée principal pour la phase d'exploration.
        """
        self.hero = hero  # ✨ IMPORTANT : Assigner le héros
    
        # Boucle d'exploration continue
        while True:
            resultat = self.proposer_action()
            
            if resultat == "exploration":
                # Continue l'exploration - reste dans la boucle
                continue
            else:
                # Retourne le résultat (combat, menu, soin)
                return resultat
    
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

