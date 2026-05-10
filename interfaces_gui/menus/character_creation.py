import pygame
import uuid
from characters import Hero
from display.gui_manager import COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_DIALOG_X, PANEL_DIALOG_Y

class CharacterCreation:
    def __init__(self, gui, assets):
        self.gui = gui
        self.assets = assets

    def run(self):
        """Handles the creation of a new hero."""
        # 1. Name input
        self.gui.clear_screen()
        self.gui.draw_background_image(self.assets.title_bg)

        self.gui.draw_stats_panel("NEW HERO")
        self.gui.draw_viewport_panel("CREATION")

        self.gui.draw_text("Welcome, adventurer.", PANEL_VIEW_X + 20, PANEL_VIEW_Y + 50)
        self.gui.draw_text("What is your name?", PANEL_VIEW_X + 20, PANEL_VIEW_Y + 80)

        name = self.gui.input_text("Enter your name:", PANEL_DIALOG_X + 40, PANEL_DIALOG_Y + 40)

        # 2. Race selection
        race_options = [("HUMAN (+1 Strength/Endurance)", "Human"), ("DWARF (+2 Endurance)", "Dwarf")]
        selection = 0

        chosen_race = None
        while chosen_race is None and self.gui.running:
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % len(race_options)
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % len(race_options)
                    elif event.key == pygame.K_RETURN:
                        chosen_race = race_options[selection][1]

            self.gui.clear_screen()
            self.gui.draw_background_image(self.assets.title_bg)

            self.gui.draw_stats_panel(name.upper())
            self.gui.draw_viewport_panel("CHOOSE YOUR RACE")
            self.gui.draw_dialog_panel("SELECTION")

            self.gui.draw_text(f"Well met, {name}.", PANEL_VIEW_X + 20, PANEL_VIEW_Y + 50)
            self.gui.draw_text("Choose your form:", PANEL_VIEW_X + 20, PANEL_VIEW_Y + 80)

            start_y = PANEL_DIALOG_Y + 60
            for i, (label, _) in enumerate(race_options):
                color = COLOR_HIGHLIGHT if i == selection else COLOR_TEXT
                prefix = "► " if i == selection else "  "
                self.gui.draw_text(f"{prefix}{label}", PANEL_DIALOG_X + 40, start_y + i * 40, color)

            self.gui.update_display()

        hero = Hero(name, chosen_race)
        hero.id = str(uuid.uuid4())
        return hero
