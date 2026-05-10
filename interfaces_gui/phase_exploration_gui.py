import pygame
import random
import os
from display.gui_manager import GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W, PANEL_LOG_X, PANEL_LOG_W
from utils.dice import Die
from interfaces_gui.utils import handle_menu_navigation, load_and_scale_image, typewriter_effect
from characters.monster import create_random_monster
from saves.save_manager import save_game
from interfaces_gui.exploration_events import get_exploration_event
from interfaces_gui.dice_roll_screen import DiceRollScreen

class PhaseExplorationGUI:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()
        self.hero = None
        self.message_log = []
        self.first_visit = True
        self.exploration_images = []
        self.current_image = None
        self.npc_memories = {}
        self.world_state = {}
        self._load_exploration_images()

    def _load_exploration_images(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_dir = os.path.join(base_dir, "assets", "Exploration")

        target_w = PANEL_VIEW_W - 40
        target_h = PANEL_VIEW_H - 60

        if os.path.exists(img_dir):
            for filename in os.listdir(img_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    path = os.path.join(img_dir, filename)
                    # keep_ratio=False to fill the entire frame
                    img = load_and_scale_image(path, target_w, target_h, keep_ratio=False)
                    if img:
                        self.exploration_images.append(img)

        if self.exploration_images:
            self.current_image = random.choice(self.exploration_images)

    def reset(self, npc_memories=None, world_state=None):
        self.first_visit = True
        if self.exploration_images:
            self.current_image = random.choice(self.exploration_images)
        self.npc_memories = npc_memories if npc_memories is not None else {}
        self.world_state = world_state if world_state is not None else {}

    def show(self, hero):
        """
        Main exploration loop.
        Returns ("combat", monster), "menu" or "quit".
        """
        # Clear previous events to avoid ghost clicks (e.g. Enter still held after combat)
        pygame.event.clear()

        self.hero = hero

        # Reset logs and play intro animation
        self.message_log = []
        if self.first_visit:
            msg = "You begin your exploration..."
            self.first_visit = False
        else:
            msg = "You continue your exploration..."

        self.add_log(msg, typewriter=True, show_menu=False, skippable=False)

        options = [("EXPLORE", "explore"), ("REST", "rest"), ("MENU", "menu")]
        selection = 0

        while self.gui.running:
            # 1. Events
            for event in self.gui.get_events():
                selection, confirmed = handle_menu_navigation(event, selection, len(options))

                if confirmed:
                    action = options[selection][1]
                    if action == "explore":
                        result = self.explore()
                        if isinstance(result, tuple) and result[0] == "combat":
                            return result
                        elif result == "npc":
                            return "npc"
                    elif action == "rest":
                        result = self.do_rest()
                        if isinstance(result, tuple) and result[0] == "combat":
                            return result
                    elif action == "menu":
                        return "menu"

            # 2. Draw
            self._draw_interface(selection, options)
        return "quit"

    def add_log(self, message, typewriter=True, show_menu=True, skippable=True):
        """Add a message to the log, with optional typewriter effect."""
        if not typewriter:
            self.message_log.append(message)
            if len(self.message_log) > 10:
                self.message_log.pop(0)
            return

        # Use the centralised function
        # Create a lambda for the draw callback that includes the show_menu argument
        draw_callback = lambda: self._draw_interface(show_menu=show_menu)

        typewriter_effect(
            self.gui,
            self.message_log,
            message,
            draw_callback,
            skippable=skippable
        )

    def _draw_interface(self, selection=0, options=None, show_menu=True):
        """Helper to redraw the interface during animations."""
        if options is None:
            options = [("EXPLORE", "explore"), ("REST", "rest"), ("MENU", "menu")]

        self.gui.clear_screen()
        self.gui.draw_stats_panel(hero=self.hero)
        self.gui.draw_viewport_panel("DARK FOREST")

        # Viewport
        rect_forest = pygame.Rect(PANEL_VIEW_X + 20, PANEL_VIEW_Y + 40, PANEL_VIEW_W - 40, PANEL_VIEW_H - 60)
        if self.current_image:
            self.gui.screen.blit(self.current_image, (PANEL_VIEW_X + 20, PANEL_VIEW_Y + 40))
        else:
            pygame.draw.rect(self.gui.screen, (10, 30, 10), rect_forest)
            self.gui.draw_text("...", PANEL_VIEW_X + 100, PANEL_VIEW_Y + 150, (50, 100, 50), font=self.gui.title_font)

        # Unified bottom interface (Standard Mode)
        # If show_menu is False, pass None for options
        display_options = options if show_menu else None

        self.gui.draw_bottom_interface(
            menu_options=display_options,
            selected_index=selection,
            logs=self.message_log,
            input_mode=False,
            panel_title="EXPLORATION"
        )

        self.gui.update_display()

    def explore(self):
        """Exploration logic"""
        # Check debug setting for forced Hermit encounter
        if getattr(self.gui.config, "debug_force_hermit", False):
            self.add_log("[DEBUG] The Hermit awaits...", typewriter=True)
            pygame.time.wait(500)
            return "npc"

        roll = Die.roll()

        # Combat: 2 and 4
        if roll in [2, 4]:
            self.add_log("[!] A suspicious noise approaches!", typewriter=True)
            # Small delay to read
            pygame.time.wait(500)

            # Wait for player to release keys to avoid looping
            pygame.event.clear()

            monster = create_random_monster()
            return "combat", monster

        # Hermit: 6
        elif roll == 6:
            # Hermit encounter
            self.add_log("[?] A silhouette emerges from the mist...", typewriter=True)
            pygame.time.wait(500)
            return "npc"

        # Exploration: 1, 3, 5
        else:
            # Change ambience image only when exploring without incident
            # And with 30% probability to avoid changing too often
            if self.exploration_images and random.random() < 0.3:
                self.current_image = random.choice(self.exploration_images)

            msg, bonus = get_exploration_event(self.hero)
            if 'gold' in bonus:
                self.hero.gold += bonus['gold']

            self.add_log(msg, typewriter=True)
            return "exploration"

    def do_rest(self) -> tuple | None:
        roll = DiceRollScreen().show(title="RESTING...", hero=self.hero)

        ambush_chances = {1: 0.60, 2: 0.30, 3: 0.30, 4: 0.10, 5: 0.10, 6: 0.0}
        ambush_chance = ambush_chances[roll]

        if ambush_chance > 0 and random.random() < ambush_chance:
            self.add_log("[!] You are ambushed in your sleep!", typewriter=True)
            pygame.event.clear()
            return "combat", create_random_monster()

        if self.hero.hp < self.hero.max_hp:
            heal = self.hero.max_hp // 2
            self.hero.hp = min(self.hero.hp + heal, self.hero.max_hp)
            self.add_log(f"You rest and recover +{heal} HP.")
        else:
            self.add_log("You are already at full health.")

        save_game(self.hero, 0, self.npc_memories, self.world_state)
        self.add_log("Game saved.")
        return None
