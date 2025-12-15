from affichage_gui.gui_manager import GuiManager
from interfaces_gui.phase_menu_gui import PhaseMenuGUI

def main():
    # Initialisation du moteur graphique
    gui = GuiManager()
    gui.init()

    # Initialisation des phases GUI
    phase_menu = PhaseMenuGUI()

    # Boucle principale du jeu (Chef d'orchestre)
    while gui.running:
        choix = phase_menu.afficher_menu_principal()
        
        if choix == "nouveau":
            hero = phase_menu.creer_hero()
            print(f"Héros créé : {hero.nom} ({hero.race})")
            # TODO: Lancer phase_exploration.afficher(hero)
        elif choix == "continuer":
            print("Continuer jeu (TODO)")
        elif choix == "quitter":
            break

if __name__ == "__main__":
    main()
