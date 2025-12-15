import pygame
import random
from affichage_gui.gui_manager import GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W
from utils.de6faces import De
from personnages.monstre import creer_monstre_aleatoire

class PhaseExplorationGUI:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()
        self.hero = None
        self.message_log = ["Vous entrez dans la forêt..."]

    def reset(self):
        self.message_log = ["Vous entrez dans la forêt..."]

    def afficher(self, hero):
        """
        Boucle principale d'exploration.
        Retourne ("combat", monstre), "menu" ou "quitter".
        """
        self.hero = hero
        options = [("EXPLORER", "explorer"), ("REPOS", "repos"), ("MENU", "menu")]
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
                        action = options[selection][1]
                        if action == "explorer":
                            result = self.explorer()
                            if isinstance(result, tuple) and result[0] == "combat":
                                return result
                        elif action == "repos":
                            self.se_reposer()
                        elif action == "menu":
                            return "menu"

            # 2. Draw
            self.gui.clear_screen()
            self.gui.draw_stats_panel(hero=self.hero)
            self.gui.draw_viewport_panel("FORET SOMBRE")
            self.gui.draw_dialog_panel("EXPLORATION")

            # Viewport : Placeholder Forêt (Un rectangle vert sombre pour l'instant)
            rect_foret = pygame.Rect(PANEL_VIEW_X + 20, PANEL_VIEW_Y + 40, PANEL_VIEW_W - 40, PANEL_VIEW_H - 60)
            pygame.draw.rect(self.gui.screen, (10, 30, 10), rect_foret)
            self.gui.draw_text("🌲  🌲  🌲", PANEL_VIEW_X + 100, PANEL_VIEW_Y + 150, (50, 100, 50), font=self.gui.title_font)

            # Dialogue : Logs + Menu
            # Afficher les 3 derniers messages
            start_log_y = PANEL_DIALOG_Y + 40
            for i, msg in enumerate(self.message_log[-3:]):
                self.gui.draw_text(f"> {msg}", PANEL_DIALOG_X + 20, start_log_y + i * 25)

            # Afficher le menu à droite
            menu_x = PANEL_DIALOG_X + PANEL_DIALOG_W - 200
            for i, (label, _) in enumerate(options):
                color = COLOR_HIGHLIGHT if i == selection else COLOR_TEXT
                prefix = "► " if i == selection else "  "
                self.gui.draw_text(f"{prefix}{label}", menu_x, start_log_y + i * 30, color)

            self.gui.update_display()
        return "quitter"

    def ajouter_log(self, message):
        self.message_log.append(message)
        if len(self.message_log) > 10:
            self.message_log.pop(0)

    def explorer(self):
        """Logique d'exploration (copiée/adaptée de phase_exploration.py)"""
        jet = De.lancer()
        if jet <= 4:
            self.ajouter_log("⚠️ Un bruit suspect approche !")
            # Petit délai pour lire
            pygame.time.wait(500)
            monstre = creer_monstre_aleatoire()
            return "combat", monstre
        else:
            events = [
                "Rien à signaler.",
                "Vous trouvez des traces anciennes.",
                "Le vent souffle dans les branches.",
                "Vous trouvez une pièce d'or !"
            ]
            msg = random.choice(events)
            if "or" in msg:
                self.hero.gold += 1
            self.ajouter_log(msg)
            return "exploration"

    def se_reposer(self):
        if self.hero.points_de_vie < self.hero.points_de_vie_max:
            soin = self.hero.points_de_vie_max // 2
            self.hero.points_de_vie = min(self.hero.points_de_vie + soin, self.hero.points_de_vie_max)
            self.ajouter_log(f"💤 Vous vous reposez (+{soin} PV).")
        else:
            self.ajouter_log("Vous êtes déjà en pleine forme.")
