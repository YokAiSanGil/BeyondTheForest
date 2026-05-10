import logging
from display.gui_manager import GuiManager
from interfaces_gui.phase_menu_gui import PhaseMenuGUI
from interfaces_gui.phase_exploration_gui import PhaseExplorationGUI
from interfaces_gui.phase_combat_gui import PhaseCombatGUI
from interfaces_gui.phase_npc_gui import PhaseNPCGUI
from characters.monster import create_hermit_boss

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)

def main():
    # Initialise the graphics engine
    gui = GuiManager()
    gui.init()

    # Initialise GUI phases
    phase_menu = PhaseMenuGUI()
    phase_exploration = PhaseExplorationGUI()
    phase_combat = PhaseCombatGUI()
    phase_npc = PhaseNPCGUI()

    # Main game loop (orchestrator)
    while gui.running:
        menu_result = phase_menu.show_main_menu()
        choice = menu_result[0]
        hero = None

        npc_memories = {}
        world_state = {}

        if choice == "new":
            hero = phase_menu.create_hero()
        elif choice == "continue":
            result = menu_result[1]
            if isinstance(result, tuple):
                hero, npc_memories, world_state = result
            else:
                hero = result
        elif choice == "quit":
            break

        if hero:
            phase_exploration.reset(npc_memories, world_state)
            # Launch the game loop
            while gui.running:
                result = phase_exploration.show(hero)

                if isinstance(result, tuple) and result[0] == "combat":
                    monster = result[1]
                    combat_result = phase_combat.show(hero, monster, npc_memories, world_state)

                    if combat_result == "victory":
                        # Return to exploration (loot already handled in phase_combat)
                        pass
                    elif combat_result == "flee":
                        # Return to exploration
                        pass
                    elif combat_result == "defeat":
                        # Game Over -> Return to main menu
                        break

                elif result == "npc":
                    # Launch NPC phase
                    phase_npc.start(npc_memories, world_state, hero)
                    npc_result = None

                    while gui.running:
                        # Events
                        events = gui.get_events()
                        res_npc = phase_npc.handle_events(events)

                        if res_npc == "exploration":
                            npc_result = "exploration"
                            break

                        # Update
                        res_update = phase_npc.update()
                        if res_update == "boss_combat":
                            npc_result = "boss_combat"
                            break

                        # Draw
                        phase_npc.draw(gui.screen)
                        gui.update_display()

                    if npc_result == "boss_combat":
                        # Launch boss combat
                        boss = create_hermit_boss()
                        combat_result = phase_combat.show(hero, boss, npc_memories, world_state)

                        if combat_result == "defeat":
                            break  # Game Over
                        # If victory (unlikely), return to exploration or end game

                elif result == "menu":
                    break  # Return to main menu
                elif result == "quit":
                    gui.running = False
                    break

if __name__ == "__main__":
    main()
