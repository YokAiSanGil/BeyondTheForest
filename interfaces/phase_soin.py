"""
Module phase_soin - Interface pour la phase de soin/repos.
Ce module contient la classe PhaseSoin qui gère l'interface de repos et de soin.
"""

from .base_interface import BaseInterface
from affichage.widgets import creer_barre_de_vie
from affichage.ascii_art import HUMAIN, NAIN
from menu_anime import MenuAnime
from utils.outils import clear_screen, ecrire_lentement, suivant


class PhaseSoin(BaseInterface):
    """
    Classe pour gérer l'interface de soin et de repos.
    Permet au héros de récupérer ses points de vie entre les combats.
    """
    
    def __init__(self):
        super().__init__()
        self.hero = None
    
    def afficher_interface_soin(self, hero):
        """
        Affiche l'interface de soin principale.
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
    
    def proposer_soin(self):
        """
        Propose le menu de soin si le héros a besoin de se soigner.
        """
        if self.hero.points_de_vie < self.hero.points_de_vie_max:
            self.ecrire_message(f"{self.hero.nom} prend un moment pour se soigner...")
            self.attendre_utilisateur()
            self.nettoyer_ecran()
            
            options_soin = [
                ("SE REPOSER (Récupère tous les PV)", "repos"), 
                ("CONTINUER L'AVENTURE", "continuer")
            ]
            menu = MenuAnime.style_simple()
            choix = menu.afficher("Que voulez-vous faire ?", options_soin)
            
            if choix == "repos":
                self.effectuer_repos()
            else:
                self.continuer_blesse()
        else:
            self.hero_en_forme()
    
    def effectuer_repos(self):
        """
        Effectue le repos complet du héros.
        """
        self.nettoyer_ecran()
        self.ecrire_message(f"{self.hero.nom} se repose paisiblement...")
        self.attendre_utilisateur()
        self.nettoyer_ecran()
        
        ancien_pv = self.hero.points_de_vie
        self.hero.se_reposer()
        pv_recuperes = self.hero.points_de_vie - ancien_pv
        
        self.ecrire_message(f"✨ {self.hero.nom} récupère {pv_recuperes} PV !")
        self.attendre_utilisateur()
        self.nettoyer_ecran()
        
        nouvelle_barre = creer_barre_de_vie(self.hero.points_de_vie, self.hero.points_de_vie_max)
        print(f"{self.hero.nom} le {self.hero.race}")
        print(f"PV: {nouvelle_barre}")
        print("\n💚 Complètement restauré !")
        self.attendre_utilisateur()
    
    def continuer_blesse(self):
        """
        Le héros décide de continuer malgré ses blessures.
        """
        self.nettoyer_ecran()
        self.ecrire_message(f"{self.hero.nom} décide de continuer malgré ses blessures...")
        self.attendre_utilisateur()
    
    def hero_en_forme(self):
        """
        Le héros est déjà en pleine forme.
        """
        self.ecrire_message(f"{self.hero.nom} est en pleine forme !")
        self.attendre_utilisateur()
        self.nettoyer_ecran()
        self.ecrire_message("Prêt pour de nouvelles aventures !")
        self.attendre_utilisateur()
    
    def finaliser_soin(self):
        """
        Finalise la phase de soin et prépare le retour à l'exploration.
        """
        self.nettoyer_ecran()
        self.ecrire_message(f"{self.hero.nom} reprend son exploration...")
        self.attendre_utilisateur()
    
    def afficher(self, hero):
        """
        Point d'entrée principal pour la phase de soin.
        """
        self.afficher_interface_soin(hero)
        self.proposer_soin()
        self.finaliser_soin()
        return "exploration"
    
    def traiter_action(self, action, *args, **kwargs):
        """
        Traite les actions de la phase de soin.
        """
        if action == "repos":
            self.effectuer_repos()
        elif action == "continuer":
            self.continuer_blesse()
        return "exploration"
