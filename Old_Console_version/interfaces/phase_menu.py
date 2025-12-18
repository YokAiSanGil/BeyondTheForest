"""
Module phase_menu - Interface pour les menus principaux et la création de héros.
Ce module contient la classe PhaseMenu qui gère tous les menus du jeu.
"""

import uuid
from .base_interface import BaseInterface
from personnages import Hero
from sauvegarde.gestion_sauvegarde import sauvegarder_partie, lister_sauvegardes, charger_partie
from affichage.ascii_art import OPENING, TITLE_SCREEN, NAIN, HUMAIN
from affichage.animations import ligne_par_ligne
from affichage.menu_anime import MenuAnime, afficher_fenetre, afficher_titre_simple
from Old_Console_version.utils.outils import clear_screen, ecrire_lentement, suivant, pause
  # gestion_sauvegarde import consolidated above


class PhaseMenu(BaseInterface):
    """
    Classe pour gérer tous les menus du jeu :
    - Menu principal
    - Création de héros
    - Écran d'intro
    - Menu de confirmation de sortie
    """
    
    def __init__(self):
        super().__init__()
    
    def afficher_ecran_intro(self):
        """
        Affiche l'art ascii de l'intro tout stylé du jeu.
        """
        self.nettoyer_ecran()
        ligne_par_ligne(OPENING, 0.1)
        pause(2)
        print(TITLE_SCREEN)
        self.attendre_utilisateur()
    
    def afficher_menu_principal(self):
        """
        Affiche le menu principal et retourne le choix de l'utilisateur.
        """
        options = [
            ("NOUVEAU JEU", "nouveau"),
            ("CONTINUER", "continuer"),
            ("QUITTER", "quitter")
        ]
        # Menu principal horizontal minimal avec OPTIONS
        menu = MenuAnime()
        choix = menu.afficher("", options)
        if choix == "options":
            # Sous-menu Options du menu principal
            submenu = [
                ("TABLEAU", "tableau"),
                ("LIST_JOUER", "list_jouer"),
                ("EFFACER SAV", "effacer_sav"),
                ("RETOUR", "retour"),
                ("QUITTER", "quitter")
            ]
            sous = MenuAnime().afficher("OPTIONS", submenu)
            if sous == "tableau":
                self.nettoyer_ecran()
                print("📊 Tableau non disponible...")
                self.attendre_utilisateur()
                return self.afficher_menu_principal()
            elif sous == "list_jouer":
                self.nettoyer_ecran()
                print("📋 Liste des joueurs non disponible...")
                self.attendre_utilisateur()
                return self.afficher_menu_principal()
            elif sous == "effacer_sav":
                # Effacer le fichier de sauvegarde
                import os
                from sauvegarde.gestion_sauvegarde import SAUVEGARDE_PATH
                if os.path.exists(SAUVEGARDE_PATH): os.remove(SAUVEGARDE_PATH)
                self.nettoyer_ecran()
                print("🗑️  Sauvegarde effacée !")
                self.attendre_utilisateur()
                return self.afficher_menu_principal()
            elif sous == "retour":
                return self.afficher_menu_principal()
            elif sous == "quitter":
                return "quitter"
            else:
                return self.afficher_menu_principal()
        return choix
    
    def continuer_jeu(self):
        """
        Charge et propose de reprendre une partie sauvegardée.
        """
        self.nettoyer_ecran()
        saves = lister_sauvegardes()
        if not saves:
            self.ecrire_message("Aucune sauvegarde trouvée.")
            self.attendre_utilisateur()
            return None
        # Sélection d'un héros sauvegardé
        # saves est une liste de dicts {'nom': ..., 'id': ...}
        options_heroes = [(s['nom'], s['id'] if s['id'] else s['nom']) for s in saves]
        
        choix_id = MenuAnime().afficher("HÉROS SAUVEGARDÉS", options_heroes)
        if not choix_id:
            return None
        hero, monstres_vaincus = charger_partie(choix_id)
        # Afficher les statistiques de la partie sélectionnée
        stats_contenu = f"""
{hero.nom} le {hero.race}

PV       : {hero.points_de_vie}/{hero.points_de_vie_max}
Or       : {hero.gold}
Cuir     : {hero.cuir}
Victoires: {monstres_vaincus}
Morts    : {hero.morts}
"""
        afficher_fenetre(stats_contenu, largeur_min=30, marge=4)
        # Confirmation pour charger
        options_conf = [("OUI, reprendre", True), ("NON, abandonner", False)]
        confirmer = MenuAnime().afficher("CHARGER PARTIE ?", options_conf)
        if confirmer:
            return hero, monstres_vaincus
        return None
    
    def confirmer_quitter(self):
        """
        Affiche le menu de confirmation pour quitter le jeu.
        """
        options_quitter = [
            ("Oui, quitter le jeu", "oui"),
            ("Non, continuer l'aventure", "non")
        ]
        menu = MenuAnime()
        confirmer = menu.afficher("Voulez-vous vraiment quitter ?", options_quitter)
        
        if confirmer == "oui":
            self.nettoyer_ecran()
            message_fin = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║                Merci d'avoir joué !                  ║
║                                                      ║
║         À bientôt dans Heroes Vs Monsters !          ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""
            print(message_fin)
            self.ecrire_message("Au revoir, brave aventurier...")
            exit()
        else:
            return False
    
    def creer_hero(self):
        """
        Gère la création d'un nouveau héros.
        """
        self.nettoyer_ecran()
        self.ecrire_message("Bienvenue, brave aventurier !")
        self.ecrire_message("Quel est votre nom ?")
        nom = input("► ")
        # Vérifier que le nom n'est pas vide
        while not nom.strip():
            print("Vous devez avoir un nom, brave Hero ...")
            nom = input("► ")
        # Empêcher les doublons de noms
        existing_saves = lister_sauvegardes()
        existing_names = [s['nom'] for s in existing_saves]
        while nom in existing_names:
            print(f"Le nom '{nom}' est déjà utilisé. Choisissez un autre nom.")
            nom = input("► ")

        self.nettoyer_ecran()
        self.ecrire_message(f"Enchanté, {nom} !")
        self.ecrire_message("Votre forme actuelle est une ame perdue.")
        self.ecrire_message("...", 0.9)
        
        pause(1)
        self.nettoyer_ecran()
        options_race = [
            ("HUMAIN (+1 Force, +1 Endurance)", "Humain"),
            ("NAIN (+2 Endurance)", "Nain")
        ]
        menu = MenuAnime()
        race = menu.afficher(f"Choisissez une nouvelle forme physique.", options_race)

        if race is None:
            return self.creer_hero()  # Récursion en cas d'annulation
        
        hero = Hero(nom, race)
        hero.id = str(uuid.uuid4())
        self.nettoyer_ecran()
        self.ecrire_message('... vous possédez une nouvelle forme ...', 0.07)
        self.ecrire_message(f"{hero.nom}, la forêt vous appelle.", 0.07)
        self.ecrire_message("...", 0.9)
        pause(1)
        self.nettoyer_ecran()

        ASCII = NAIN if hero.race == "Nain" else HUMAIN
        ligne_par_ligne(ASCII, 0.2)
        pause(1)
        # Préparer nom affiché en majuscules (éviter None.upper())
        nom_affiche = hero.nom.upper() if hero.nom else ""
        stats_contenu = f"""
{nom_affiche} {('le ' if hero.race == "Nain" else "l'")}{hero.race.upper()}

Endurance     : {hero.endurance}
Force         : {hero.force}
Points de Vie : {hero.points_de_vie}
Or            : {hero.gold}
Cuir          : {hero.cuir}
"""
        afficher_fenetre(stats_contenu, largeur_min=30, marge=4)
        self.attendre_utilisateur()
        # Sauvegarde automatique de la nouvelle partie
        sauvegarder_partie(hero, 0)
        return hero
    
    def afficher_stats_finales(self, hero, monstres_vaincus):
        """
        Affiche les statistiques finales de la partie.
        """
        self.nettoyer_ecran()
        stats_finales = f"""
STATISTIQUES FINALES
Héros            : {hero.nom} le {hero.race}
Monstres vaincus : {monstres_vaincus}
Or collecté      : {hero.gold}
Cuir collecté    : {hero.cuir}
PV restants      : {hero.points_de_vie}
Merci d'avoir joué !
"""
        print(stats_finales)
        self.attendre_utilisateur()
    
    def afficher(self, type_menu, *args, **kwargs):
        """
        Point d'entrée principal pour afficher différents types de menus.
        """
        if type_menu == "intro":
            return self.afficher_ecran_intro()
        elif type_menu == "principal":
            return self.afficher_menu_principal()
        elif type_menu == "creer_hero":
            return self.creer_hero()
        elif type_menu == "continuer":
            return self.continuer_jeu()
        elif type_menu == "quitter":
            return self.confirmer_quitter()
        elif type_menu == "stats_finales":
            hero, monstres_vaincus = args
            return self.afficher_stats_finales(hero, monstres_vaincus)
        else:
            raise ValueError(f"Type de menu inconnu : {type_menu}")
    
    def traiter_action(self, action, *args, **kwargs):
        """
        Traite les actions du menu principal.
        """
        if action == "nouveau":
            return self.creer_hero()
        elif action == "continuer":
            return self.continuer_jeu()
        elif action == "quitter":
            return self.confirmer_quitter()
        elif action is None:  # Échap pressé
            return self.confirmer_quitter()
        else:
            return None
