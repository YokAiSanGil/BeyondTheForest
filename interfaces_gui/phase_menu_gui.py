import pygame
import uuid
from personnages import Hero
from affichage_gui.gui_manager import GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, PANEL_DIALOG_X, PANEL_DIALOG_Y, SCREEN_WIDTH, SCREEN_HEIGHT
from affichage.ascii_art import TITLE_SCREEN
from sauvegarde.gestion_sauvegarde import charger_partie, lister_sauvegardes

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
        Affiche l'écran titre puis le menu principal.
        Retourne (choix, data).
        """
        # 1. Écran Titre (Attente Entrée)
        attente_entree = True
        blink_timer = 0
        
        while attente_entree and self.gui.running:
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        attente_entree = False
            
            self.gui.clear_screen()
            
            # Dessiner le titre ASCII
            lines = TITLE_SCREEN.strip().split('\n')
            start_y = 50
            for i, line in enumerate(lines):
                # Centrage horizontal manuel (approx)
                text_w = len(line) * 10 
                x = (SCREEN_WIDTH - text_w) // 2
                self.gui.draw_text(line, x, start_y + i * 15, COLOR_HIGHLIGHT)
            
            # Clignotement "PRESS ENTER"
            blink_timer += 1
            if (blink_timer // 30) % 2 == 0:
                self.gui.draw_text("PRESS ENTER", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, center=True)
                
            self.gui.update_display()
            
        if not self.gui.running:
            return "quitter", None

        # 2. Menu Principal
        options = [
            ("NOUVEAU JEU", "nouveau"),
            ("CONTINUER", "continuer"),
            ("QUITTER", "quitter")
        ]
        selection = 0
        
        while self.gui.running:
            # Events
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        choix = options[selection][1]
                        if choix == "continuer":
                            hero = self.gerer_continuer()
                            if hero:
                                return "continuer", hero
                        else:
                            return choix, None

            # Draw
            self.gui.clear_screen()
            
            # Redessiner le titre (statique, plus sombre)
            lines = TITLE_SCREEN.strip().split('\n')
            start_y = 50
            for i, line in enumerate(lines):
                text_w = len(line) * 10
                x = (SCREEN_WIDTH - text_w) // 2
                self.gui.draw_text(line, x, start_y + i * 15, (80, 80, 100))

            # Menu à la place de "Press Enter"
            menu_y = SCREEN_HEIGHT - 200
            for i, (label, _) in enumerate(options):
                color = COLOR_HIGHLIGHT if i == selection else COLOR_TEXT
                prefix = "► " if i == selection else "  "
                self.gui.draw_text(f"{prefix}{label}", SCREEN_WIDTH // 2 - 100, menu_y + i * 40, color)

            self.gui.update_display()
            
        return "quitter", None

    def gerer_continuer(self):
        saves = lister_sauvegardes()
        if not saves:
            # Afficher message "Pas de sauvegarde"
            self.gui.clear_screen()
            
            # Redessiner le titre (statique, plus sombre)
            lines = TITLE_SCREEN.strip().split('\n')
            start_y = 50
            for i, line in enumerate(lines):
                text_w = len(line) * 10
                x = (SCREEN_WIDTH - text_w) // 2
                self.gui.draw_text(line, x, start_y + i * 15, (80, 80, 100))

            self.gui.draw_text("AUCUNE SAUVEGARDE TROUVEE", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, (255, 50, 50), center=True)
            self.gui.update_display()
            pygame.time.wait(1500)
            return None
        
        # Préparer les options : liste des sauvegardes + Retour
        options = []
        for s in saves:
            options.append((f"{s['nom']}", s['id']))
        options.append(("RETOUR", None))
        
        selection = 0
        
        while self.gui.running:
            # Events
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        choix_id = options[selection][1]
                        if choix_id is None:
                            return None # Retour
                        else:
                            hero, _ = charger_partie(choix_id)
                            return hero
                    elif event.key == pygame.K_ESCAPE:
                        return None

            # Draw
            self.gui.clear_screen()
            
            # Redessiner le titre (statique, plus sombre)
            lines = TITLE_SCREEN.strip().split('\n')
            start_y = 50
            for i, line in enumerate(lines):
                text_w = len(line) * 10
                x = (SCREEN_WIDTH - text_w) // 2
                self.gui.draw_text(line, x, start_y + i * 15, (80, 80, 100))

            self.gui.draw_text("CHOISIR UNE SAUVEGARDE", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 250, COLOR_TEXT, center=True)

            # Menu list centered
            menu_y = SCREEN_HEIGHT - 200
            for i, (label, _) in enumerate(options):
                color = COLOR_HIGHLIGHT if i == selection else COLOR_TEXT
                prefix = "► " if i == selection else "  "
                self.gui.draw_text(f"{prefix}{label}", SCREEN_WIDTH // 2 - 100, menu_y + i * 40, color)
                
            self.gui.update_display()
            
        return None
