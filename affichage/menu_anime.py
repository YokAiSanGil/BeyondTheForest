"""
Module de menus animés pour Heroes vs Monsters.
"""
from utils.outils import clear_screen, cacher_curseur, afficher_curseur, lire_fleche_bloquant
from .ascii_art import OPENING, TITLE_SCREEN

def afficher_titre_simple():
    """Affiche le titre du jeu sans animation."""
    print(OPENING)
    print(TITLE_SCREEN)

def afficher_fenetre(contenu, largeur_min=20, marge=4, retourner_string=False):
    """
    Affiche un texte dans une fenêtre avec bordure.
    Si retourner_string=True, retourne la chaîne au lieu de l'afficher.
    """
    lignes = contenu.strip().split('\n')
    largeur_necessaire = max(len(ligne) for ligne in lignes) + marge if lignes else marge
    
    # Assurer une largeur minimale
    largeur_finale = max(largeur_necessaire, largeur_min)
    
    # Créer les bordures
    ligne_haut = "┌" + "─" * (largeur_finale - 1) + "┐"
    ligne_bas = "└" + "─" * (largeur_finale - 1) + "┘"
    
    resultat = [ligne_haut]
    
    # Afficher chaque ligne centrée dans la fenêtre
    for ligne in lignes:
        espace = ' ' * ((largeur_finale - len(ligne)) // 2)
        ligne_formatee = f"│{espace}{ligne}{' ' * (largeur_finale - len(ligne) - len(espace) - 1)}│"
        resultat.append(ligne_formatee)
    
    resultat.append(ligne_bas)
    
    if retourner_string:
        return '\n'.join(resultat)
    else:
        for ligne in resultat:
            print(ligne)

class MenuAnime:
    """
    Module pour créer et afficher des menus avec curseur animé.
    Permet différentes configurations d'affichage.
    """
    def __init__(self, 
                 instructions="↑↓ pour naviguer, Entrée pour sélectionner",
                 afficher_titre_jeu=True, 
                 conserver_ecran=False,
                 style_fenetre=True,
                 menu_horizontal=False):  # ✨ NOUVEAU PARAMÈTRE
        self.instructions = instructions
        self.afficher_titre_jeu = afficher_titre_jeu
        self.conserver_ecran = conserver_ecran
        self.style_fenetre = style_fenetre
        self.menu_horizontal = menu_horizontal  # ✨ NOUVEAU

    @classmethod
    def style_simple(cls):
        """Crée un menu minimaliste sans titre ni fenêtre."""
        return cls(afficher_titre_jeu=False, style_fenetre=False)

    @classmethod
    def style_combat(cls):
        """Crée un menu optimisé pour les combats."""
        return cls(instructions="", 
                afficher_titre_jeu=False, 
                conserver_ecran=False,  # Changé de True à False pour permettre la mise à jour
                style_fenetre=False)
    
    @classmethod
    def style_dialogue(cls):
        """Crée un menu optimisé pour les dialogues."""
        return cls(instructions="", 
                afficher_titre_jeu=False, 
                conserver_ecran=True,
                style_fenetre=True)
        
    @classmethod
    def style_exploration(cls):
        """Style spécialement conçu pour les menus d'exploration (horizontal)."""
        return cls(
            instructions="",  # ✨ PLUS D'INSTRUCTIONS
            afficher_titre_jeu=False,
            conserver_ecran=True,
            style_fenetre=False,
            menu_horizontal=True
        )

    def afficher(self, titre, options):
        """
        Affiche le menu et retourne l'option sélectionnée.
        """
        curseur = 0
        
        while True:
            # ✨ RAFRAÎCHISSEMENT POUR MENU HORIZONTAL
            if self.menu_horizontal:
                # Pour les menus horizontaux, on nettoie et réaffiche tout
                if not self.conserver_ecran:
                    clear_screen()
            else:
                # Comportement normal pour les menus verticaux
                if not self.conserver_ecran:
                    clear_screen()
                    
            # Afficher le titre du jeu seulement si demandé
            if self.afficher_titre_jeu:
                print(TITLE_SCREEN)
            
            if titre:
                print(titre)
            
            self._afficher_options_menu(options, curseur)
            
            nouveau_curseur, action = self._gerer_curseur_menu(curseur, options)
            
            if action == 'NAVIGATION':
                curseur = nouveau_curseur
            elif action == 'SELECTION':
                cacher_curseur()
                afficher_curseur()
                return options[curseur][1]
            elif action in ['ECHAP', 'INTERRUPT']:
                cacher_curseur()
                afficher_curseur()
                return None
            elif action == 'IGNORE':
                # Touche ignorée, on continue la boucle
                continue

    def _afficher_options_menu(self, options, curseur_actuel):
        """
        Affiche les options du menu (vertical ou horizontal selon le paramètre).
        """
        if self.menu_horizontal:
            self._afficher_options_horizontal(options, curseur_actuel)
        else:
            self._afficher_options_vertical(options, curseur_actuel)

    def _afficher_options_vertical(self, options, curseur_actuel):
        """
        Affiche les options du menu verticalement (comportement original).
        """
        for i, (texte, _) in enumerate(options):
            if i == curseur_actuel:
                print(f"  ▶ {texte}")
            else:
                print(f"    {texte}")
        print(f"\n{self.instructions}")

    def _afficher_options_horizontal(self, options, curseur_actuel):
        """
        Affiche les options du menu horizontalement avec curseur simple.
        """
        ligne_options = "    "
        for i, (texte, _) in enumerate(options):
            if i == curseur_actuel:
                ligne_options += f"▶ {texte}    "
            else:
                ligne_options += f"  {texte}    "
        
        print(ligne_options)
        # ✨ PLUS D'INSTRUCTIONS AFFICHÉES

    def _gerer_curseur_menu(self, curseur_actuel, options):
        """
        Gère la logique du curseur (vertical ou horizontal selon le paramètre).
        """
        cacher_curseur()
        
        try:
            touche = lire_fleche_bloquant()
            
            if self.menu_horizontal:
                # Navigation horizontale
                if touche == 'GAUCHE':
                    nouveau_curseur = (curseur_actuel - 1) % len(options)
                    return nouveau_curseur, 'NAVIGATION'
                elif touche == 'DROITE':
                    nouveau_curseur = (curseur_actuel + 1) % len(options)
                    return nouveau_curseur, 'NAVIGATION'
            else:
                # Navigation verticale (comportement original)
                if touche == 'HAUT':
                    nouveau_curseur = (curseur_actuel - 1) % len(options)
                    return nouveau_curseur, 'NAVIGATION'
                elif touche == 'BAS':
                    nouveau_curseur = (curseur_actuel + 1) % len(options)
                    return nouveau_curseur, 'NAVIGATION'
            
            # Touches communes (Entrée, Échap)
            if touche == 'ENTREE':
                afficher_curseur()
                return curseur_actuel, 'SELECTION'
            elif touche == 'ECHAP':
                afficher_curseur()
                return None, 'ECHAP'
            else:
                # Touche ignorée, on reste sur le même curseur
                return curseur_actuel, 'IGNORE'
                
        except KeyboardInterrupt:
            afficher_curseur()
            return None, 'INTERRUPT'