import pygame
import time
from display.gui_manager import GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W, PANEL_LOG_X, PANEL_LOG_W
from utils.dice import Die
from interfaces_gui.utils import handle_menu_navigation, load_and_scale_image, typewriter_effect, wait_for_enter
from characters import attack, flee, loot
from saves.save_manager import save_game, delete_save

class PhaseCombatGUI:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()
        self.hero = None
        self.monster = None
        self.monster_surface = None
        self.combat_log = []

    def show(self, hero, monster, npc_memories=None, world_state=None):
        """
        Main combat loop.
        Returns "victory", "defeat" or "flee".
        """
        self.hero = hero
        self.monster = monster
        self.npc_memories = npc_memories if npc_memories is not None else {}
        self.world_state = world_state if world_state is not None else {}
        self.combat_log = []

        # Load and process the monster image
        self.monster_surface = None
        if hasattr(monster, 'image_path'):
            if monster.race == "The True Hermit":
                # The boss fills the entire viewport panel
                self.monster_surface = load_and_scale_image(monster.image_path, PANEL_VIEW_W, PANEL_VIEW_H, keep_ratio=False)
            else:
                self.monster_surface = load_and_scale_image(monster.image_path, 350, 350)

        # Cinematic intro
        self.typewriter_log(f"A wild {monster.race} appears!", show_menu=False, wait_input=False)

        options = [("ATTACK", "attack"), ("FLEE", "flee")]
        selection = 0

        # Combat loop
        while self.gui.running:
            # 1. Events
            action_chosen = None
            for event in self.gui.get_events():
                selection, confirmed = handle_menu_navigation(event, selection, len(options))

                if confirmed:
                    action_chosen = options[selection][1]

            # 2. Turn logic (if action chosen)
            if action_chosen:
                if action_chosen == "attack":
                    result = self.combat_turn()
                    if result:
                        return result
                elif action_chosen == "flee":
                    success, messages, damage = flee(self.hero, self.monster)
                    for msg in messages:
                        self.typewriter_log(msg)

                    if success:
                        return "flee"
                    else:
                        self.hero.hp -= damage
                        if self.hero.hp <= 0:
                            return "defeat"

            # 3. Draw
            self.draw_interface(selection, options)

        return "quit"

    def draw_interface(self, selection=0, options=[], show_menu=True):
        self.gui.clear_screen()
        self.gui.draw_stats_panel(hero=self.hero)
        # Remove automatic title to draw it ourselves with the HP bar
        self.gui.draw_viewport_panel(None)

        self.draw_monster()

        # Unified bottom interface (Standard Mode)
        display_options = options if show_menu else None

        self.gui.draw_bottom_interface(
            menu_options=display_options,
            selected_index=selection,
            logs=self.combat_log,
            input_mode=False,
            panel_title="COMBAT"
        )

        self.gui.update_display()

    def typewriter_log(self, message, show_menu=True, wait_input=True):
        # Use the centralised function
        draw_callback = lambda: self.draw_interface(show_menu=show_menu)

        typewriter_effect(
            self.gui,
            self.combat_log,
            message,
            draw_callback,
            speed=20,
            skippable=True
        )

        if wait_input:
            wait_for_enter(self.gui)

    def add_log(self, message):
        self.combat_log.append(message)
        if len(self.combat_log) > 10:
            self.combat_log.pop(0)

    def draw_monster(self):
        # 1. Header: Name + HP bar (outside the panel, above)
        header_y = PANEL_VIEW_Y - 25
        name_x = PANEL_VIEW_X

        # Monster name
        name_text = self.monster.race.upper()
        self.gui.draw_text(name_text, name_x, header_y, color=COLOR_TEXT)

        # Calculate bar position (to the right of the name)
        font = self.gui.font
        name_width = font.size(name_text)[0]

        bar_x = name_x + name_width + 20
        bar_y = header_y + 5  # Slightly lower to centre with the text
        bar_w = 200
        bar_h = 12

        # Draw HP bar
        ratio = max(0, self.monster.hp / self.monster.max_hp)
        # Background (dark)
        pygame.draw.rect(self.gui.screen, (50, 50, 0), (bar_x, bar_y, bar_w, bar_h))
        # HP (Gold / Highlight)
        pygame.draw.rect(self.gui.screen, COLOR_HIGHLIGHT, (bar_x, bar_y, bar_w * ratio, bar_h))
        # Thin border for the bar
        pygame.draw.rect(self.gui.screen, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 1)

        # 2. Monster Image (centred in the remaining space)
        cx = PANEL_VIEW_X + PANEL_VIEW_W // 2
        cy = PANEL_VIEW_Y + PANEL_VIEW_H // 2

        if self.monster_surface:
            rect = self.monster_surface.get_rect(center=(cx, cy))
            self.gui.screen.blit(self.monster_surface, rect)
        else:
            # Fallback text
            self.gui.draw_text(f"{self.monster.race}", cx, cy, (255, 100, 100), center=True)

    def combat_turn(self):
        """Execute a full combat turn (Hero attacks, then Monster attacks if alive)"""

        # 1. Hero attacks
        msgs, damage = attack(self.hero, self.monster)
        for msg in msgs:
            self.typewriter_log(msg)

        # Apply damage AFTER messages
        self.monster.hp -= damage
        self.draw_interface()  # Refresh to show HP dropping

        if self.monster.hp <= 0:
            self.typewriter_log(f"The {self.monster.race} is defeated!")

            # Loot
            msgs_loot = loot(self.hero, self.monster)
            for msg in msgs_loot:
                self.typewriter_log(msg)

            # Auto-save after victory
            save_game(self.hero, 0, self.npc_memories, self.world_state)
            self.typewriter_log("Game saved.")

            return "victory"

        # 2. Monster attacks
        if self.monster.is_alive():
            msgs_monster, damage_monster = attack(self.monster, self.hero)
            for msg in msgs_monster:
                self.typewriter_log(msg)

            self.hero.hp -= damage_monster
            self.draw_interface()

        if self.hero.hp <= 0:
            self.typewriter_log("You are dead...")
            # Delete save (Permadeath)
            delete_save(self.hero.id)
            self.typewriter_log("Save deleted.")
            return "defeat"

        return None
