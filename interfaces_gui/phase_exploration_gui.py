import pygame
import random
import os
from affichage_gui.gui_manager import GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W, PANEL_LOG_X, PANEL_LOG_W
from utils.de6faces import De
from interfaces_gui.utils import handle_menu_navigation, load_and_scale_image, typewriter_effect
from personnages.monstre import creer_monstre_aleatoire
from sauvegarde.gestion_sauvegarde import sauvegarder_partie
from interfaces_gui.exploration_events import get_exploration_event

class PhaseExplorationGUI:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()
        self.hero = None
        self.message_log = []
        self.first_visit = True
        self.exploration_images = []
        self.current_image = None
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
                    img = load_and_scale_image(path, target_w, target_h)
                    if img:
                        self.exploration_images.append(img)
        
        if self.exploration_images:
            self.current_image = random.choice(self.exploration_images)

    def reset(self):
        self.first_visit = True
        if self.exploration_images:
            self.current_image = random.choice(self.exploration_images)

    def afficher(self, hero):
        """
        Boucle principale d'exploration.
        Retourne ("combat", monstre), "menu" ou "quitter".
        """
        # Nettoyer les événements précédents pour éviter les clics fantômes (ex: Entrée resté enfoncé après combat)
        pygame.event.clear()
        
        self.hero = hero
        
        # Reset logs and play intro animation
        self.message_log = []
        if self.first_visit:
            msg = "Vous commencez votre exploration..."
            self.first_visit = False
        else:
            msg = "Vous continuez votre exploration..."
            
        self.ajouter_log(msg, typewriter=True, show_menu=False, skippable=False)
        
        options = [("EXPLORER", "explorer"), ("REPOS", "repos"), ("MENU", "menu")]
        selection = 0
        
        while self.gui.running:
            # 1. Events
            for event in self.gui.get_events():
                selection, confirmed = handle_menu_navigation(event, selection, len(options))
                
                if confirmed:
                    action = options[selection][1]
                    if action == "explorer":
                        result = self.explorer()
                        if isinstance(result, tuple) and result[0] == "combat":
                            return result
                        elif result == "npc":
                            return "npc"
                    elif action == "repos":
                        self.se_reposer()
                    elif action == "menu":
                        return "menu"

            # 2. Draw
            self._draw_interface(selection, options)
        return "quitter"

    def ajouter_log(self, message, typewriter=True, show_menu=True, skippable=True):
        """Ajoute un message au log, avec effet typewriter optionnel."""
        if not typewriter:
            self.message_log.append(message)
            if len(self.message_log) > 10:
                self.message_log.pop(0)
            return

        # Utilisation de la fonction centralisée
        # On crée une lambda pour le callback de dessin qui inclut l'argument show_menu
        draw_callback = lambda: self._draw_interface(show_menu=show_menu)
        
        typewriter_effect(
            self.gui, 
            self.message_log, 
            message, 
            draw_callback, 
            skippable=skippable
        )
            
    def _draw_interface(self, selection=0, options=None, show_menu=True):
        """Helper pour redessiner l'interface pendant les animations."""
        if options is None:
            options = [("EXPLORER", "explorer"), ("REPOS", "repos"), ("MENU", "menu")]
            
        self.gui.clear_screen()
        self.gui.draw_stats_panel(hero=self.hero)
        self.gui.draw_viewport_panel("FORET SOMBRE")
        # self.gui.draw_dialog_panel("EXPLORATION") # Supprimé pour éviter superposition

        # Viewport
        rect_foret = pygame.Rect(PANEL_VIEW_X + 20, PANEL_VIEW_Y + 40, PANEL_VIEW_W - 40, PANEL_VIEW_H - 60)
        if self.current_image:
            self.gui.screen.blit(self.current_image, (PANEL_VIEW_X + 20, PANEL_VIEW_Y + 40))
        else:
            pygame.draw.rect(self.gui.screen, (10, 30, 10), rect_foret)
            self.gui.draw_text("...", PANEL_VIEW_X + 100, PANEL_VIEW_Y + 150, (50, 100, 50), font=self.gui.title_font)

        # Interface du bas unifiée (Mode Standard)
        # Si show_menu est False, on passe None pour les options
        display_options = options if show_menu else None
        
        self.gui.draw_bottom_interface(
            menu_options=display_options,
            selected_index=selection,
            logs=self.message_log,
            input_mode=False,
            panel_title="EXPLORATION"
        )

        self.gui.update_display()

    def explorer(self):
        """Logique d'exploration (copiée/adaptée de phase_exploration.py)"""
        jet = De.lancer()
        
        # Combat : 2 et 4
        if jet in [2, 4]:
            self.ajouter_log("[!] Un bruit suspect approche !", typewriter=True)
            # Petit délai pour lire
            pygame.time.wait(500)
            
            # Attendre que le joueur relâche les touches pour éviter de boucler
            pygame.event.clear()
            
            monstre = creer_monstre_aleatoire()
            return "combat", monstre
            
        # Hermite : 6
        elif jet == 6:
            # Rencontre avec l'Hermite
            self.ajouter_log("[?] Une silhouette émerge de la brume...", typewriter=True)
            pygame.time.wait(500)
            return "npc"
            
        # Exploration : 1, 3, 5
        else:
            # Changer d'image d'ambiance seulement si on explore sans encombre
            # Et avec une probabilité de 30% pour ne pas changer trop souvent
            if self.exploration_images and random.random() < 0.3:
                self.current_image = random.choice(self.exploration_images)
                
            msg, bonus = get_exploration_event(self.hero)
            if 'gold' in bonus:
                self.hero.gold += bonus['gold']
            
            self.ajouter_log(msg, typewriter=True)
            return "exploration"

    def se_reposer(self):
        if self.hero.points_de_vie < self.hero.points_de_vie_max:
            soin = self.hero.points_de_vie_max // 2
            self.hero.points_de_vie = min(self.hero.points_de_vie + soin, self.hero.points_de_vie_max)
            self.ajouter_log(f"Vous vous reposez (+{soin} PV).")
            sauvegarder_partie(self.hero, 0) # Sauvegarde auto
            self.ajouter_log("Partie sauvegardée.")
        else:
            self.ajouter_log("Vous êtes déjà en pleine forme.")
            sauvegarder_partie(self.hero, 0) # Sauvegarde auto même si pas de soin
            self.ajouter_log("Partie sauvegardée.")
