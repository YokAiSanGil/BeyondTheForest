import pygame
import uuid
from personnages import Hero
from affichage_gui.gui_manager import GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, PANEL_DIALOG_X, PANEL_DIALOG_Y

class PhaseMenuGUI:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()

    def creer_hero(self):
        """
        Gère la création d'un nouveau héros (Nom + Race).
        """
        # 1. Saisie du Nom
        self.gui.clear_screen()
        self.gui.draw_stats_panel("NOUVEAU HEROS")
        self.gui.draw_viewport_panel("CREATION")
        
        # On affiche un message dans le viewport
        self.gui.draw_text("Bienvenue, aventurier.", PANEL_VIEW_X + 20, PANEL_VIEW_Y + 50)
        self.gui.draw_text("Quel est votre nom ?", PANEL_VIEW_X + 20, PANEL_VIEW_Y + 80)
        self.gui.update_display() # Force update avant input
        
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
            
        # 3. Création
        hero = Hero(nom, race_choisie)
        hero.id = str(uuid.uuid4())
        return hero

    def afficher_menu_principal(self):
        """
        Affiche le menu principal et retourne le choix (nouveau, continuer, quitter).
        """
        options = [
            ("NOUVEAU JEU", "nouveau"),
            ("CONTINUER", "continuer"),
            ("QUITTER", "quitter")
        ]
        selection = 0
        
        while self.gui.running:
            # 1. Events
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return options[selection][1]

            # 2. Draw
            self.gui.clear_screen()
            self.gui.draw_stats_panel("HEROES VS MONSTERS")
            self.gui.draw_viewport_panel("")
            self.gui.draw_dialog_panel("MENU PRINCIPAL")

            # Titre dans le Viewport
            self.gui.draw_text("HEROES VS MONSTERS", 
                               PANEL_VIEW_X + PANEL_VIEW_W // 2, 
                               PANEL_VIEW_Y + PANEL_VIEW_H // 2, 
                               color=COLOR_HIGHLIGHT, 
                               font=self.gui.title_font, 
                               center=True)

            # Options dans le Dialogue
            start_y = PANEL_DIALOG_Y + 60
            for i, (label, _) in enumerate(options):
                color = COLOR_HIGHLIGHT if i == selection else COLOR_TEXT
                prefix = "► " if i == selection else "  "
                self.gui.draw_text(f"{prefix}{label}", PANEL_DIALOG_X + 40, start_y + i * 40, color)

            self.gui.update_display()
        return "quitter"
