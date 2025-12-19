from affichage_gui.gui_manager import GuiManager
from interfaces_gui.phase_menu_gui import PhaseMenuGUI
from interfaces_gui.phase_exploration_gui import PhaseExplorationGUI
from interfaces_gui.phase_combat_gui import PhaseCombatGUI
from interfaces_gui.phase_npc_gui import PhaseNPCGUI
from personnages.monstre import creer_boss_hermite

def main():
    # Initialisation du moteur graphique
    gui = GuiManager()
    gui.init()

    # Initialisation des phases GUI
    phase_menu = PhaseMenuGUI()
    phase_exploration = PhaseExplorationGUI()
    phase_combat = PhaseCombatGUI()
    phase_npc = PhaseNPCGUI()

    # Boucle principale du jeu (Chef d'orchestre)
    while gui.running:
        resultat_menu = phase_menu.afficher_menu_principal()
        choix = resultat_menu[0]
        hero = None
        
        npc_memories = {}
        world_state = {}

        if choix == "nouveau":
            hero = phase_menu.creer_hero()
        elif choix == "continuer":
            res = resultat_menu[1]
            if isinstance(res, tuple):
                hero, npc_memories, world_state = res
            else:
                hero = res
        elif choix == "quitter":
            break
            
        if hero:
            phase_exploration.reset(npc_memories, world_state)
            # Lancement de la boucle de jeu
            while gui.running:
                resultat = phase_exploration.afficher(hero)
                
                if isinstance(resultat, tuple) and resultat[0] == "combat":
                    monstre = resultat[1]
                    res_combat = phase_combat.afficher(hero, monstre, npc_memories, world_state)
                    
                    if res_combat == "victoire":
                        # Retour à l'exploration (le loot est déjà géré dans phase_combat)
                        pass
                    elif res_combat == "fuite":
                        # Retour à l'exploration
                        pass
                    elif res_combat == "defaite":
                        # Game Over -> Retour menu principal
                        break
                
                elif resultat == "npc":
                    # Lancement de la phase NPC
                    phase_npc.start(npc_memories, world_state, hero)
                    res_npc_loop = None
                    
                    while gui.running:
                        # Events
                        events = gui.get_events()
                        res_npc = phase_npc.handle_events(events)
                        
                        if res_npc == "exploration":
                            res_npc_loop = "exploration"
                            break
                            
                        # Update
                        res_update = phase_npc.update()
                        if res_update == "combat_boss":
                            res_npc_loop = "combat_boss"
                            break
                        
                        # Draw
                        phase_npc.draw(gui.screen)
                        gui.update_display()
                    
                    if res_npc_loop == "combat_boss":
                        # Lancement du combat de boss
                        boss = creer_boss_hermite()
                        res_combat = phase_combat.afficher(hero, boss, npc_memories, world_state)
                        
                        if res_combat == "defaite":
                            break # Game Over
                        # Si victoire (improbable), on retourne à l'exploration ou fin du jeu
                        
                elif resultat == "menu":
                    break # Retour au menu principal
                elif resultat == "quitter":
                    gui.running = False
                    break

if __name__ == "__main__":
    main()
