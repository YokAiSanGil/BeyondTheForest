import pygame
import uuid
from personnages import Hero
from affichage_gui.gui_manager import COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_DIALOG_X, PANEL_DIALOG_Y

class CharacterCreation:
    def __init__(self, gui, assets):
        self.gui = gui
        self.assets = assets

    def run(self):
        """Gère la création d'un nouveau héros."""
        # 1. Saisie du Nom
        self.gui.clear_screen()
        self.gui.draw_background_image(self.assets.title_bg)
            
        self.gui.draw_stats_panel("NOUVEAU HEROS")
        self.gui.draw_viewport_panel("CREATION")
        
        self.gui.draw_text("Bienvenue, aventurier.", PANEL_VIEW_X + 20, PANEL_VIEW_Y + 50)
        self.gui.draw_text("Quel est votre nom ?", PANEL_VIEW_X + 20, PANEL_VIEW_Y + 80)
        self.gui.update_display()
        
        nom = self.gui.input_text("Entrez votre nom :", PANEL_DIALOG_X + 40, PANEL_DIALOG_Y + 40)
        
        # 2. Choix de la Race
        options_race = [("HUMAIN (+1 Force/Endu)", "Humain"), ("NAIN (+2 Endu)", "Nain")]
        selection = 0
        
        race_choisie = None
        while race_choisie is None and self.gui.running:
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % len(options_race)
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % len(options_race)
                    elif event.key == pygame.K_RETURN:
                        race_choisie = options_race[selection][1]

            self.gui.clear_screen()
            self.gui.draw_background_image(self.assets.title_bg)
                
            self.gui.draw_stats_panel(nom.upper())
            self.gui.draw_viewport_panel("CHOIX DE LA RACE")
            self.gui.draw_dialog_panel("SELECTION")
            
            self.gui.draw_text(f"Enchanté, {nom}.", PANEL_VIEW_X + 20, PANEL_VIEW_Y + 50)
            self.gui.draw_text("Choisissez votre forme :", PANEL_VIEW_X + 20, PANEL_VIEW_Y + 80)

            start_y = PANEL_DIALOG_Y + 60
            for i, (label, _) in enumerate(options_race):
                color = COLOR_HIGHLIGHT if i == selection else COLOR_TEXT
                prefix = "► " if i == selection else "  "
                self.gui.draw_text(f"{prefix}{label}", PANEL_DIALOG_X + 40, start_y + i * 40, color)
            
            self.gui.update_display()
            
        hero = Hero(nom, race_choisie)
        hero.id = str(uuid.uuid4())
        return hero
