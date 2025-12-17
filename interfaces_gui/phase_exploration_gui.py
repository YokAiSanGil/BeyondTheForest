import pygame
import random
import os
from affichage_gui.gui_manager import GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W
from utils.de6faces import De
from personnages.monstre import creer_monstre_aleatoire
from sauvegarde.gestion_sauvegarde import sauvegarder_partie
from interfaces_gui.exploration_events import get_exploration_event

class PhaseExplorationGUI:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()
        self.hero = None
        self.message_log = ["Vous entrez dans la forêt..."]
        self.exploration_images = []
        self.current_image = None
        self._load_exploration_images()

    def _load_exploration_images(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_dir = os.path.join(base_dir, "assets", "Exploration")
        
        if os.path.exists(img_dir):
            for filename in os.listdir(img_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        path = os.path.join(img_dir, filename)
                        img = pygame.image.load(path).convert()
                        # Redimensionner pour le viewport (en gardant un peu de marge si besoin, ou fill)
                        # On va remplir le viewport : PANEL_VIEW_W - 40, PANEL_VIEW_H - 60
                        target_w = PANEL_VIEW_W - 40
                        target_h = PANEL_VIEW_H - 60
                        img = pygame.transform.scale(img, (target_w, target_h))
                        self.exploration_images.append(img)
                    except Exception as e:
                        print(f"Erreur chargement image exploration {filename}: {e}")
        
        if self.exploration_images:
            self.current_image = random.choice(self.exploration_images)

    def reset(self):
        self.message_log = ["Vous entrez dans la forêt..."]
        if self.exploration_images:
            self.current_image = random.choice(self.exploration_images)

    def afficher(self, hero):
        """
        Boucle principale d'exploration.
        Retourne ("combat", monstre), "menu" ou "quitter".
        """
        # Nettoyer les événements précédents pour éviter les clics fantômes (ex: Entrée resté enfoncé après combat)
        pygame.event.clear()
        pygame.time.wait(200)
        
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
            self._draw_interface(selection, options)
        return "quitter"

    def ajouter_log(self, message, typewriter=True):
        """Ajoute un message au log, avec effet typewriter optionnel."""
        if not typewriter:
            self.message_log.append(message)
            if len(self.message_log) > 10:
                self.message_log.pop(0)
            return

        # Effet Typewriter
        full_message = message
        current_text = ""
        self.message_log.append("") # Placeholder pour le message en cours
        
        # Nettoyer la queue d'événements pour éviter les inputs fantômes
        pygame.event.clear()
        
        skip = False
        for char in full_message:
            if skip:
                current_text += char
                continue
                
            current_text += char
            self.message_log[-1] = current_text
            
            # Redessiner l'interface
            self._draw_interface()
            
            # Gestion du skip (Espace ou Entrée)
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        skip = True
            
            if not skip:
                pygame.time.wait(30) # Vitesse de frappe
        
        # Finaliser le message
        self.message_log[-1] = full_message
        if len(self.message_log) > 10:
            self.message_log.pop(0)
            
    def _draw_interface(self, selection=0, options=None):
        """Helper pour redessiner l'interface pendant les animations."""
        if options is None:
            options = [("EXPLORER", "explorer"), ("REPOS", "repos"), ("MENU", "menu")]
            
        self.gui.clear_screen()
        self.gui.draw_stats_panel(hero=self.hero)
        self.gui.draw_viewport_panel("FORET SOMBRE")
        self.gui.draw_dialog_panel("EXPLORATION")

        # Viewport
        rect_foret = pygame.Rect(PANEL_VIEW_X + 20, PANEL_VIEW_Y + 40, PANEL_VIEW_W - 40, PANEL_VIEW_H - 60)
        if self.current_image:
            self.gui.screen.blit(self.current_image, (PANEL_VIEW_X + 20, PANEL_VIEW_Y + 40))
        else:
            pygame.draw.rect(self.gui.screen, (10, 30, 10), rect_foret)
            self.gui.draw_text("🌲  🌲  🌲", PANEL_VIEW_X + 100, PANEL_VIEW_Y + 150, (50, 100, 50), font=self.gui.title_font)

        # Logs
        start_log_y = PANEL_DIALOG_Y + 40
        # On affiche les 3 derniers messages, y compris celui en cours d'écriture
        msgs_to_show = self.message_log[-3:]
        for i, msg in enumerate(msgs_to_show):
            # Utiliser une police plus petite si possible, sinon standard
            self.gui.draw_text(f"> {msg}", PANEL_DIALOG_X + 20, start_log_y + i * 25)

        # Menu
        menu_x = PANEL_DIALOG_X + PANEL_DIALOG_W - 200
        for i, (label, _) in enumerate(options):
            color = COLOR_HIGHLIGHT if i == selection else COLOR_TEXT
            prefix = "► " if i == selection else "  "
            self.gui.draw_text(f"{prefix}{label}", menu_x, start_log_y + i * 30, color)

        self.gui.update_display()

    def explorer(self):
        """Logique d'exploration (copiée/adaptée de phase_exploration.py)"""
        jet = De.lancer()
        if jet <= 3:
            self.ajouter_log("[!] Un bruit suspect approche !", typewriter=True)
            # Petit délai pour lire
            pygame.time.wait(500)
            
            # Attendre que le joueur relâche les touches pour éviter de boucler
            pygame.event.clear()
            
            monstre = creer_monstre_aleatoire()
            return "combat", monstre
        elif jet == 3:
            # Rencontre avec l'Hermite
            self.ajouter_log("[?] Une silhouette émerge de la brume...", typewriter=True)
            pygame.time.wait(500)
            return "npc"
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
            self.ajouter_log(f"💤 Vous vous reposez (+{soin} PV).")
            sauvegarder_partie(self.hero, 0) # Sauvegarde auto
            self.ajouter_log("Partie sauvegardée.")
        else:
            self.ajouter_log("Vous êtes déjà en pleine forme.")
            sauvegarder_partie(self.hero, 0) # Sauvegarde auto même si pas de soin
            self.ajouter_log("Partie sauvegardée.")
