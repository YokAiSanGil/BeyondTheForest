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
    Menu horizontal unique pour tout le jeu.
    """
    def __init__(self):
        # Toujours horizontal minimaliste
        self.instructions = ""
        self.afficher_titre_jeu = False
        self.conserver_ecran = False
        self.style_fenetre = False
        self.menu_horizontal = True

    @classmethod
    def style_simple(cls):
        """Alias pour le style horizontal par défaut."""
        return cls()


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