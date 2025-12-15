import pygame
from sauvegarde.gestion_sauvegarde import charger_partie, lister_sauvegardes
from affichage_gui.gui_manager import COLOR_HIGHLIGHT, COLOR_TEXT, SCREEN_WIDTH, SCREEN_HEIGHT

class SaveLoadMenu:
    def __init__(self, gui, assets):
        self.gui = gui
        self.assets = assets

    def run(self):
        """Affiche le menu de chargement de sauvegarde."""
        saves = lister_sauvegardes()
        if not saves:
            self._afficher_message_vide()
            return None
        
        options = []
        for s in saves:
            identifiant = s['id'] if s['id'] is not None else s['nom']
            options.append((f"{s['nom']}", identifiant))
        
        options.append(("RETOUR", "___RETOUR___"))
        
        selection = 0
        
        while self.gui.running:
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        choix_id = options[selection][1]
                        if choix_id == "___RETOUR___":
                            return None
                        else:
                            hero, _ = charger_partie(choix_id)
                            return hero
                    elif event.key == pygame.K_ESCAPE:
                        return None

            self.gui.clear_screen()
            self.gui.draw_background_image(self.assets.title_bg)
            
            # Titre
            if self.assets.title_surface:
                title_x = SCREEN_WIDTH - self.assets.title_surface.get_width() - 50
                self.gui.screen.blit(self.assets.title_surface, (title_x, 50))

            self.gui.draw_text("Choose Incarnation", SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2 + 50, COLOR_TEXT, center=True)

            # Liste
            menu_right_margin = 50
            menu_y = SCREEN_HEIGHT // 2 + 100
            for i, (label, _) in enumerate(options):
                color = COLOR_HIGHLIGHT if i == selection else COLOR_TEXT
                prefix = "► " if i == selection else ""
                text_str = f"{prefix}{label}"
                
                text_surf = self.gui.font.render(text_str, True, color)
                text_w = text_surf.get_width()
                x = SCREEN_WIDTH - text_w - menu_right_margin
                
                self.gui.screen.blit(text_surf, (x, menu_y + i * 40))
                
            self.gui.update_display()
            
        return None

    def _afficher_message_vide(self):
        self.gui.clear_screen()
        self.gui.draw_background_image(self.assets.title_bg)
        
        if self.assets.title_surface:
            title_x = SCREEN_WIDTH - self.assets.title_surface.get_width() - 50
            self.gui.screen.blit(self.assets.title_surface, (title_x, 50))
            
        self.gui.draw_text("AUCUNE SAUVEGARDE", SCREEN_WIDTH - 200, SCREEN_HEIGHT // 2 + 100, (255, 50, 50), center=True)
        self.gui.update_display()
        pygame.time.wait(1500)
