from affichage_gui.gui_manager import GuiManager
from interfaces_gui.phase_menu_gui import PhaseMenuGUI
from interfaces_gui.phase_exploration_gui import PhaseExplorationGUI
from interfaces_gui.phase_combat_gui import PhaseCombatGUI

def main():
    # Initialisation du moteur graphique
    gui = GuiManager()
    gui.init()

    # Initialisation des phases GUI
    phase_menu = PhaseMenuGUI()
    phase_exploration = PhaseExplorationGUI()
    phase_combat = PhaseCombatGUI()

    # Boucle principale du jeu (Chef d'orchestre)
    while gui.running:
        choix = phase_menu.afficher_menu_principal()
        
        if choix == "nouveau":
            hero = phase_menu.creer_hero()
            phase_exploration.reset()
            # Lancement de la boucle de jeu
            while gui.running:
                resultat = phase_exploration.afficher(hero)
                
                if isinstance(resultat, tuple) and resultat[0] == "combat":
                    monstre = resultat[1]
                    res_combat = phase_combat.afficher(hero, monstre)
                    
                    if res_combat == "victoire":
                        # Retour à l'exploration (le loot est déjà géré dans phase_combat)
                        pass
                    elif res_combat == "fuite":
                        # Retour à l'exploration
                        pass
                    elif res_combat == "defaite":
                        # Game Over -> Retour menu principal
                        break
                        
                elif resultat == "menu":
                    break # Retour au menu principal
                elif resultat == "quitter":
                    gui.running = False
                    break
                    
        elif choix == "continuer":
            print("Continuer jeu (TODO)")
        elif choix == "quitter":
            break

if __name__ == "__main__":
    main()
