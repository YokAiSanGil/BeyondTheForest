"""
Module phase_combat - Interface pour la phase de combat.
Ce module contient la classe PhaseCombat qui gère toute l'interface de combat.
"""

from typing import Optional, Literal
from .base_interface import BaseInterface
from personnages import frapper, fuir, depecer
from personnages.hero import Hero
from personnages.monstre import Monster
from affichage.widgets import creer_barre_de_vie, combiner_blocs_ascii, afficher_journal_combat
from affichage.ascii_art import HUMAIN, NAIN, WOLF, ORC, DRAGONNET
from affichage.menu_anime import MenuAnime, afficher_fenetre
from utils.music import battle_music, stop_music
from utils.outils import clear_screen, ecrire_lentement, suivant


class PhaseCombat(BaseInterface):
    """
    Classe pour gérer l'interface de combat.
    Gère l'affichage du combat, les actions du joueur et les statistiques.
    """
    
    def __init__(self):
        super().__init__()
        self.hero: Optional[Hero] = None
        self.monstre: Optional[Monster] = None
        self.menu_combat: Optional[MenuAnime] = None

    def initialiser_combat(self, hero: Hero, monstre: Monster):
        """
        Initialise le combat entre le héros et le monstre avec affichage spectaculaire.
        """
        self.hero = hero
        self.monstre = monstre
        
        # Démarrer la musique
        battle_music()
        self.nettoyer_ecran()
        
        # Créer l'interface complète de combat
        interface_combat = self.creer_interface_combat_complete()
        
        # Afficher l'interface ligne par ligne avec effet
        self.afficher_interface_ligne_par_ligne(interface_combat)
        
        # Message simple après l'affichage
        print(f"\nUn {monstre.race} apparaît, préparez-vous !")
        
        # Attendre un moment pour l'effet dramatique
        import time
        time.sleep(2)
        
        self.attendre_utilisateur()

    def creer_interface_combat_complete(self):
        """
        Crée l'interface complète de combat (héros + monstre + barres de vie).
        """
        if not self.hero or not self.monstre:
            raise ValueError("Combat non initialisé correctement")
            
        # Préparation de l'affichage
        art_hero = HUMAIN if self.hero.race == "Humain" else NAIN
        info_hero = f"{self.hero.nom} le {self.hero.race}\n{creer_barre_de_vie(self.hero.points_de_vie, self.hero.points_de_vie_max)}"
        bloc_hero = f"{art_hero}\n{info_hero}"
        
        race_monstre_lower = self.monstre.race.lower().strip()
        if race_monstre_lower == "loup": 
            art_monstre = WOLF
        elif race_monstre_lower == "orque": 
            art_monstre = ORC
        else: 
            art_monstre = DRAGONNET
        
        info_monstre = f"{self.monstre.race}\n{creer_barre_de_vie(self.monstre.points_de_vie, self.monstre.points_de_vie_max)}"
        bloc_monstre = f"{info_monstre}\n{art_monstre}"
        
        combat_info = combiner_blocs_ascii(bloc_hero, bloc_monstre, espacement=15)
        ligne_separation = "=" * 80
        
        return f"{combat_info}\n{ligne_separation}"

    def afficher_interface_ligne_par_ligne(self, interface_complete):
        """
        Affiche l'interface complète de combat ligne par ligne pour un effet dramatique.
        """
        import time
        
        lignes_interface = interface_complete.split('\n')
        for ligne in lignes_interface:
            print(ligne)
            # Petit délai pour l'effet ligne par ligne
            time.sleep(0.1)  # Plus rapide pour l'interface complète

    def afficher_interface_combat(self):
        """
        Affiche l'interface principale du combat (version normale, sans effet).
        """
        if not self.hero or not self.monstre:
            raise ValueError("Combat non initialisé correctement")
            
        self.nettoyer_ecran()
        interface_combat = self.creer_interface_combat_complete()
        print(interface_combat)
    
    def afficher_menu_actions(self):
        """
        Affiche le menu des actions possibles et retourne le choix du joueur.
        """
        # ✨ VÉRIFICATION CORRIGÉE
        if not self.hero or not self.monstre:
            raise ValueError("Combat non initialisé correctement")
            
        # Afficher l'interface de combat
        self.afficher_interface_combat()
        
        # Créer le menu d'actions
        menu = MenuAnime.style_simple()
        options = [
            ("Attaquer", "attaquer"),
            ("Fuir", "fuir"),
            ("Statistiques", "stats")
        ]
        
        return menu.afficher("", options)
    
    def afficher_stats_combat(self):
        """
        Affiche les statistiques détaillées du héros et du monstre.
        """
        if not self.hero or not self.monstre:
            raise ValueError("Combat non initialisé correctement")
            
        self.nettoyer_ecran()

        # --- Préparation du bloc du Héros ---
        art_hero = HUMAIN if self.hero.race == "Humain" else NAIN
        
        # Contenu textuel des stats du héros
        stats_hero_contenu = f"""
{self.hero.nom.upper()} - {self.hero.race.upper()}
- - - - - - - - - - - - - - -
Endurance   : {self.hero.endurance}
Force       : {self.hero.force}
PV          : {self.hero.points_de_vie}/{self.hero.points_de_vie_max}
Or          : {self.hero.gold}
Cuir        : {self.hero.cuir}
"""

        # Utilisation d'afficher_fenetre en mode "retour de chaîne"
        cadre_hero = afficher_fenetre(stats_hero_contenu, largeur_min=25, marge=4, retourner_string=True)
        
        # Combinaison du cadre et de l'art ASCII
        bloc_hero_final = combiner_blocs_ascii(cadre_hero, art_hero, espacement=5)

        # --- Préparation du bloc du Monstre ---
        stats_monstre_contenu = f"""
{self.monstre.race.upper()}
- - - - - - - - - - - - - - -
Endurance   : {self.monstre.endurance}
Force       : {self.monstre.force}
PV          : {self.monstre.points_de_vie}/{self.monstre.points_de_vie_max}
"""

        # --- Affichage final ---
        print("STATISTIQUES DÉTAILLÉES\n")
        print(bloc_hero_final)
        print("\n")
        afficher_fenetre(stats_monstre_contenu, largeur_min=25, marge=4)  # Utilisation normale

        print("\nAppuyez sur Entrée pour revenir au combat...")
        self.attendre_utilisateur()
    
    def traiter_attaque(self):
        """
        Traite l'action d'attaque du héros.
        """
        if not self.hero or not self.monstre:
            raise ValueError("Combat non initialisé correctement")
            
        messages_attaque, degats_attaque = frapper(self.hero, self.monstre)
        
        # Afficher l'intention d'attaquer
        afficher_journal_combat(self.hero, self.monstre, messages_attaque[:1])
        
        # Appliquer les dégâts et afficher le résultat
        self.monstre.points_de_vie -= degats_attaque
        if len(messages_attaque) > 1:
            afficher_journal_combat(self.hero, self.monstre, messages_attaque[1:])

        # Contre-attaque du monstre si il est encore vivant
        if self.monstre.est_vivant() and self.hero.est_vivant():
            messages_contre, degats_contre = frapper(self.monstre, self.hero)
            
            # Afficher l'intention de la contre-attaque
            afficher_journal_combat(self.hero, self.monstre, messages_contre[:1])

            # Appliquer les dégâts et afficher le résultat
            self.hero.points_de_vie -= degats_contre
            if len(messages_contre) > 1:
                afficher_journal_combat(self.hero, self.monstre, messages_contre[1:])
    
    def traiter_fuite(self):
        """
        Traite l'action de fuite du héros.
        Retourne True si la fuite réussit, False sinon.
        """
        if not self.hero or not self.monstre:
            raise ValueError("Combat non initialisé correctement")
            
        succes_fuite, messages_fuite, degats_fuite = fuir(self.hero, self.monstre)
        
        if not succes_fuite:
            afficher_journal_combat(self.hero, self.monstre, messages_fuite[:1])  # Message de tentative
            self.hero.points_de_vie -= degats_fuite
            afficher_journal_combat(self.hero, self.monstre, messages_fuite[1:])  # Messages de contre-attaque
            return False
        else:
            afficher_journal_combat(self.hero, self.monstre, messages_fuite)
            return True
    
    def traiter_confirmation_abandon(self):
        """
        Traite la demande d'abandon du combat (Echap).
        Retourne True si l'utilisateur confirme l'abandon, False sinon.
        """
        if not self.menu_combat:
            raise ValueError("Combat non initialisé correctement")
            
        options_confirmer = [("Oui, abandonner le combat", "oui"), ("Non, continuer à combattre", "non")]
        confirmer = self.menu_combat.afficher("Voulez-vous vraiment abandonner ?", options_confirmer)
        return confirmer == "oui"
    
    def traiter_fin_combat(self):
        """
        Traite la fin du combat (victoire ou défaite).
        Retourne le résultat du combat.
        """
        if not self.hero or not self.monstre:
            raise ValueError("Combat non initialisé correctement")
            
        stop_music()
        
        if self.hero.est_vivant():
            messages_fin_combat = [f"Le {self.monstre.race} est vaincu !", f"{self.hero.nom} remporte la victoire !"]
            afficher_journal_combat(self.hero, self.monstre, messages_fin_combat)
            
            # Dépouiller le monstre
            messages_depouillement = depecer(self.hero, self.monstre)
            if messages_depouillement:
                afficher_journal_combat(self.hero, self.monstre, messages_depouillement)
            
            return "victoire"
        else:
            messages_fin_combat = [f"{self.hero.nom} est vaincu...", "GAME OVER"]
            afficher_journal_combat(self.hero, self.monstre, messages_fin_combat)
            return "defaite"
    
    def afficher(self, hero: Hero, monstre: Monster) -> Literal["victoire", "defaite", "fuite", "abandon"]:
        """
        Point d'entrée principal pour la phase de combat.
        """
        # ✨ INITIALISER D'ABORD LE COMBAT
        self.initialiser_combat(hero, monstre)
        
        # ✨ PAS BESOIN DE RÉINITIALISER - déjà fait dans initialiser_combat()
        
        while self.hero and self.monstre and self.hero.est_vivant() and self.monstre.est_vivant():
            action = self.afficher_menu_actions()
            resultat = self.traiter_action(action)
            
            if resultat in ["fuite", "abandon"]:
                stop_music()
                return resultat
            
            if action != "stats":
                self.traiter_tour_monstre()
    
        # Combat terminé (victoire ou défaite)
        return self.traiter_fin_combat()
    
    def traiter_action(self, action) -> Optional[Literal["fuite", "abandon"]]:
        """
        Traite l'action choisie par le joueur.
        """
        if action == "attaquer":
            self.traiter_attaque()
            
        elif action == "fuir":
            if self.traiter_fuite():
                stop_music()
                return "fuite"
            
        elif action == "stats":
            self.afficher_stats_combat()
            
        elif action is None:  # L'utilisateur a appuyé sur Echap
            if self.traiter_confirmation_abandon():
                stop_music()
                return "abandon"
        
        return None  # Continue le combat
