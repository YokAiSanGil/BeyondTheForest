import pygame
from affichage_gui.gui_manager import COLOR_HIGHLIGHT, COLOR_TEXT, SCREEN_WIDTH, SCREEN_HEIGHT
from affichage_gui.config import GameConfig

class TitleScreen:
    def __init__(self, gui, assets, save_load_menu):
        self.gui = gui
        self.assets = assets
        self.save_load_menu = save_load_menu
        
        # CONFIGURATION
        self.PRESS_ENTER_Y_OFFSET = 30  # Ajustez cette valeur pour monter/descendre le texte
        self.MENU_START_Y = SCREEN_HEIGHT // 2 + 100 # Position Y de départ du menu (et de PRESS ENTER)

    def run(self):
        """Affiche l'écran titre puis le menu principal."""
        # 1. Écran Titre (Attente Entrée)
        if not self._wait_for_enter():
            return "quitter", None

        # 2. Menu Principal
        return self._main_menu_loop()

    def _wait_for_enter(self):
        attente_entree = True
        blink_timer = 0
        
        while attente_entree and self.gui.running:
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        attente_entree = False
            
            self.gui.clear_screen()
            self.gui.draw_background_image(self.assets.title_bg)
            
            if self.assets.title_surface:
                title_x = SCREEN_WIDTH - self.assets.title_surface.get_width() - 50
                self.gui.screen.blit(self.assets.title_surface, (title_x, 50))
                
                blink_timer += 1
                if (blink_timer // 30) % 2 == 0:
                    center_x = title_x + self.assets.title_surface.get_width() // 2
                    # Alignement avec le menu (même hauteur que le premier élément)
                    font_h = self.gui.font.get_height()
                    y_pos = self.MENU_START_Y + font_h // 2
                    self.gui.draw_text("PRESS ENTER", center_x, y_pos, center=True)
            else:
                blink_timer += 1
                if (blink_timer // 30) % 2 == 0:
                    self.gui.draw_text("PRESS ENTER", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200, center=True)
                
            self.gui.update_display()
            
        return self.gui.running

    def _main_menu_loop(self):
        options = [
            ("NOUVEAU JEU", "nouveau"),
            ("CONTINUER", "continuer"),
            ("OPTIONS", "options"),
            ("QUITTER", "quitter")
        ]
        selection = 0
        
        while self.gui.running:
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        choix = options[selection][1]
                        if choix == "continuer":
                            hero = self.save_load_menu.run()
                            if hero:
                                return "continuer", hero
                        elif choix == "options":
                            self._options_menu_loop()
                        else:
                            return choix, None

            self.gui.clear_screen()
            self.gui.draw_background_image(self.assets.title_bg)
            
            if self.assets.title_surface:
                title_x = SCREEN_WIDTH - self.assets.title_surface.get_width() - 50
                self.gui.screen.blit(self.assets.title_surface, (title_x, 50))

            menu_right_margin = 50
            menu_y = self.MENU_START_Y
            
            for i, (label, _) in enumerate(options):
                color = COLOR_HIGHLIGHT if i == selection else COLOR_TEXT
                prefix = "► " if i == selection else ""
                text_str = f"{prefix}{label}"
                
                text_surf = self.gui.font.render(text_str, True, color)
                text_w = text_surf.get_width()
                x = SCREEN_WIDTH - text_w - menu_right_margin
                
                self.gui.screen.blit(text_surf, (x, menu_y + i * 40))

            self.gui.update_display()

    def _options_menu_loop(self):
        config = GameConfig()
        options = ["enable_scanlines", "enable_flicker", "debug_force_hermit"]
        labels = {
            "enable_scanlines": "SCANLINES",
            "enable_flicker": "FLICKER",
            "debug_force_hermit": "FORCE HERMIT"
        }
        selection = 0
        
        in_options = True
        while in_options and self.gui.running:
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % (len(options) + 1)
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % (len(options) + 1)
                    elif event.key == pygame.K_RETURN:
                        if selection == len(options): # RETOUR
                            in_options = False
                        else:
                            config.toggle(options[selection])
                    elif event.key == pygame.K_ESCAPE:
                        in_options = False

            self.gui.clear_screen()
            self.gui.draw_background_image(self.assets.title_bg)
            
            # Titre Options
            self.gui.draw_text("OPTIONS", SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2 + 50, center=True)

            menu_right_margin = 50
            menu_y = SCREEN_HEIGHT // 2 + 100
            
            # Affichage des options
            for i, opt_key in enumerate(options):
                is_selected = (i == selection)
                color = COLOR_HIGHLIGHT if is_selected else COLOR_TEXT
                prefix = "► " if is_selected else ""
                
                state = "ON" if getattr(config, opt_key) else "OFF"
                label = labels[opt_key]
                
                text_str = f"{prefix}{label} : {state}"
                
                text_surf = self.gui.font.render(text_str, True, color)
                text_w = text_surf.get_width()
                x = SCREEN_WIDTH - text_w - menu_right_margin
                
                self.gui.screen.blit(text_surf, (x, menu_y + i * 40))
            
            # Bouton Retour
            i = len(options)
            is_selected = (i == selection)
            color = COLOR_HIGHLIGHT if is_selected else COLOR_TEXT
            prefix = "► " if is_selected else ""
            text_str = f"{prefix}RETOUR"
            
            text_surf = self.gui.font.render(text_str, True, color)
            text_w = text_surf.get_width()
            x = SCREEN_WIDTH - text_w - menu_right_margin
            self.gui.screen.blit(text_surf, (x, menu_y + i * 40))

            self.gui.update_display()
            
        return "quitter", None
