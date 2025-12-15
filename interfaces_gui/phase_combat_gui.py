import pygame
import time
from affichage_gui.gui_manager import GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W
from utils.de6faces import De
from personnages import frapper, fuir, depecer
from affichage.ascii_art import WOLF, ORC, DRAGONNET
from sauvegarde.gestion_sauvegarde import sauvegarder_partie, supprimer_sauvegarde

class PhaseCombatGUI:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()
        self.hero = None
        self.monstre = None
        self.combat_log = []

    def afficher(self, hero, monstre):
        """
        Boucle principale de combat.
        Retourne "victoire", "defaite" ou "fuite".
        """
        self.hero = hero
        self.monstre = monstre
        self.combat_log = [f"Un {monstre.race} sauvage apparaît !"]
        
        options = [("ATTAQUER", "attaquer"), ("FUIR", "fuir")]
        selection = 0
        
        # Boucle de combat
        while self.gui.running:
            # 1. Events
            action_choisie = None
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        action_choisie = options[selection][1]

            # 2. Logique du tour (si action choisie)
            if action_choisie:
                if action_choisie == "attaquer":
                    resultat = self.tour_de_combat()
                    if resultat:
                        return resultat
                elif action_choisie == "fuir":
                    succes, messages, degats = fuir(self.hero, self.monstre)
                    for msg in messages:
                        self.typewriter_log(msg)
                    
                    if succes:
                        return "fuite"
                    else:
                        self.hero.points_de_vie -= degats
                        if self.hero.points_de_vie <= 0:
                            return "defaite"

            # 3. Draw
            self.draw_interface(selection, options)
        
        return "quitter"

    def draw_interface(self, selection=0, options=[]):
        self.gui.clear_screen()
        self.gui.draw_stats_panel(hero=self.hero)
        self.gui.draw_viewport_panel(f"COMBAT VS {self.monstre.race.upper()}")
        self.gui.draw_dialog_panel("ACTIONS")

        self.dessiner_monstre()

        # Logs
        start_log_y = PANEL_DIALOG_Y + 40
        for i, msg in enumerate(self.combat_log[-4:]):
            self.gui.draw_text(f"> {msg}", PANEL_DIALOG_X + 20, start_log_y + i * 25)

        # Menu (si options fournies)
        if options:
            menu_x = PANEL_DIALOG_X + PANEL_DIALOG_W - 200
            for i, (label, _) in enumerate(options):
                color = COLOR_HIGHLIGHT if i == selection else COLOR_TEXT
                prefix = "► " if i == selection else "  "
                self.gui.draw_text(f"{prefix}{label}", menu_x, start_log_y + i * 30, color)
        
        self.gui.update_display()

    def typewriter_log(self, message):
        self.combat_log.append("")
        if len(self.combat_log) > 10:
            self.combat_log.pop(0)
            
        for char in message:
            self.combat_log[-1] += char
            self.draw_interface() 
            pygame.time.wait(20) 
        
        self.attendre_entree()

    def attendre_entree(self):
        waiting = True
        while waiting and self.gui.running:
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
            pygame.time.wait(10)

    def ajouter_log(self, message):
        self.combat_log.append(message)
        if len(self.combat_log) > 10:
            self.combat_log.pop(0)

    def dessiner_monstre(self):
        # Centre du viewport
        cx = PANEL_VIEW_X + PANEL_VIEW_W // 2
        cy = PANEL_VIEW_Y + PANEL_VIEW_H // 2
        
        # Choix de l'ASCII Art
        art = None
        race = self.monstre.race.lower()
        if "loup" in race:
            art = WOLF
        elif "orque" in race:
            art = ORC
        elif "dragon" in race:
            art = DRAGONNET
            
        if art:
            lines = art.strip().split('\n')
            start_y = cy - (len(lines) * 10) # Centrage vertical approximatif
            for i, line in enumerate(lines):
                # Centrage horizontal approximatif (chaque char ~10px)
                text_w = len(line) * 10 
                x = cx - text_w // 2
                self.gui.draw_text(line, x, start_y + i * 20, (200, 200, 200))
        else:
            # Fallback si pas d'art
            rect_monstre = pygame.Rect(0, 0, 100, 100)
            rect_monstre.center = (cx, cy)
            pygame.draw.rect(self.gui.screen, (200, 50, 50), rect_monstre)
            self.gui.draw_text(f"{self.monstre.race}", cx - 40, cy - 70, (255, 100, 100))
        
        # Barre de vie du monstre
        width_bar = 150
        height_bar = 10
        x_bar = cx - width_bar // 2
        y_bar = cy + 100 # Un peu plus bas que l'art
        
        ratio = max(0, self.monstre.points_de_vie / self.monstre.points_de_vie_max)
        pygame.draw.rect(self.gui.screen, (50, 0, 0), (x_bar, y_bar, width_bar, height_bar))
        pygame.draw.rect(self.gui.screen, (255, 0, 0), (x_bar, y_bar, width_bar * ratio, height_bar))
        
        self.gui.draw_text(f"{self.monstre.points_de_vie}/{self.monstre.points_de_vie_max} PV", cx - 30, y_bar + 15, (200, 200, 200))

    def tour_de_combat(self):
        """Exécute un tour de combat complet (Héros frappe, puis Monstre frappe si vivant)"""
        
        # 1. Héros attaque
        msgs, degats = frapper(self.hero, self.monstre)
        for msg in msgs:
            self.typewriter_log(msg)
        
        # Appliquer dégâts APRES les messages
        self.monstre.points_de_vie -= degats
        self.draw_interface() # Refresh pour voir les PV baisser
        
        if self.monstre.points_de_vie <= 0:
            self.typewriter_log(f"Le {self.monstre.race} est vaincu !")
            
            # Loot
            msgs_loot = depecer(self.hero, self.monstre)
            for msg in msgs_loot:
                self.typewriter_log(msg)
            
            # Sauvegarde auto après victoire
            sauvegarder_partie(self.hero, 0)
            self.typewriter_log("Partie sauvegardée.")
                
            return "victoire"

        # 2. Monstre attaque
        if self.monstre.est_vivant():
            msgs_monstre, degats_monstre = frapper(self.monstre, self.hero)
            for msg in msgs_monstre:
                self.typewriter_log(msg)
            
            self.hero.points_de_vie -= degats_monstre
            self.draw_interface()
        
        if self.hero.points_de_vie <= 0:
            self.typewriter_log("Vous êtes mort...")
            # Suppression sauvegarde (Permadeath)
            supprimer_sauvegarde(self.hero.id)
            self.typewriter_log("Sauvegarde supprimée.")
            return "defaite"
            
        return None