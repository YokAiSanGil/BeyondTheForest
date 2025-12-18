"""
Module outils.
Ce module contient des fonctions utilitaires pour le jeu.
"""
import os
import time
import sys


#os.system('cls')

"""
####---------------Outils d'interface----------------####
"""


def clear_screen():
    """
    Efface l'écran de la console.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def pause(sec):
    """
    Met en pause l'exécution du programme pendant un certain nombre de secondes.
    """
    time.sleep(sec)


def suivant():
    """
    Affiche un message pour continuer et attend que l'utilisateur appuie sur Entrée.
    """
    input(f"[ENTER] ► ")


def ligne_par_ligne(texte, vitesse=0.1):
    """
    Affiche le texte ligne par ligne avec une pause optionnelle.
    texte : str
    vitesse : float, temps en secondes entre chaque ligne (défaut 0.1)
    """
    for ligne in texte.splitlines():
        print(ligne)
        time.sleep(vitesse)
    


def ecrire_lentement(texte, vitesse=0.05):
    """
    Simule l'écriture lettre par lettre comme dans Dragon Quest.
    """
    for char in texte:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(vitesse)
    print()


def cacher_curseur():
    """
    Cache le curseur de la console.
    """
    print("\033[?25l", end='')


def afficher_curseur():
    """
    Affiche le curseur de la console.
    """
    print("\033[?25h", end='')


def lire_fleche_bloquant():
    """
    Lit les touches fléchées en mode bloquant.
    """
    if os.name == 'nt':  # Windows
        import msvcrt
        while True:
            key = msvcrt.getch()
            if key == b'\xe0':  # Touche spéciale
                key = msvcrt.getch()
                if key == b'H':
                    return 'HAUT'
                elif key == b'P':
                    return 'BAS'
                elif key == b'K':
                    return 'GAUCHE'
                elif key == b'M':
                    return 'DROITE'
            elif key == b'\r':
                return 'ENTREE'
            elif key == b'\x1b':
                return 'ECHAP'
    else:  # Linux/Mac
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                key = sys.stdin.read(1)
                if key == '\x1b':
                    key += sys.stdin.read(2)
                    if key == '\x1b[A':
                        return 'HAUT'
                    elif key == '\x1b[B':
                        return 'BAS'
                    elif key == '\x1b[C':
                        return 'DROITE'
                    elif key == '\x1b[D':
                        return 'GAUCHE'
                elif key == '\r':
                    return 'ENTREE'
                elif key == '\x1b':
                    return 'ECHAP'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)





"""
####------------------outils de jeu--------------------####
"""



def modificateur(valeur):
    """Calcule le modificateur selon la force/endurance."""
    if valeur < 5:
        return -1
    elif valeur < 10:
        return 0
    elif valeur < 15:
        return 1
    else:
        return 2
