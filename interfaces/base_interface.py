"""
Module base_interface - Classe de base pour toutes les interfaces.
Ce module contient la classe abstraite BaseInterface dont héritent toutes les phases du jeu.
"""

from abc import ABC, abstractmethod
from menu_anime import MenuAnime
from utils.outils import clear_screen, ecrire_lentement, suivant


class BaseInterface(ABC):
    """
    Classe de base abstraite pour toutes les interfaces du jeu.
    Définit les méthodes communes et l'architecture de base.
    """
    
    def __init__(self):
        self.menu = None
        self.result = None
    
    @abstractmethod
    def afficher(self, *args, **kwargs):
        """
        Méthode abstraite pour afficher l'interface.
        Doit être implémentée par chaque classe fille.
        """
        pass
    
    @abstractmethod
    def traiter_action(self, action, *args, **kwargs):
        """
        Méthode abstraite pour traiter les actions utilisateur.
        Doit être implémentée par chaque classe fille.
        """
        pass
    
    def initialiser_menu(self, **kwargs):
        """
        Initialise un menu avec les paramètres donnés.
        """
        self.menu = MenuAnime(**kwargs)
        return self.menu
    
    def nettoyer_ecran(self):
        """Nettoie l'écran."""
        clear_screen()
    
    def ecrire_message(self, message, vitesse=None):
        """Affiche un message avec effet de saisie."""
        if vitesse is not None:
            ecrire_lentement(message, vitesse)
        else:
            ecrire_lentement(message)
    
    def attendre_utilisateur(self):
        """Attend que l'utilisateur appuie sur Entrée."""
        suivant()
