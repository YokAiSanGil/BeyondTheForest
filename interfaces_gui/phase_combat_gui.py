import pygame
import time
from affichage_gui.gui_manager import GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W, PANEL_LOG_X, PANEL_LOG_W
from utils.de6faces import De
from interfaces_gui.utils import handle_menu_navigation, load_and_scale_image, typewriter_effect, wait_for_enter
from personnages import frapper, fuir, depecer
from sauvegarde.gestion_sauvegarde import sauvegarder_partie, supprimer_sauvegarde

class PhaseCombatGUI:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()
        self.hero = None
        self.monstre = None
        self.monster_surface = None
        self.combat_log = []

    def afficher(self, hero, monstre, npc_memories=None, world_state=None):
        """
        Boucle principale de combat.
        Retourne "victoire", "defaite" ou "fuite".
        """
        self.hero = hero
        self.monstre = monstre
        self.npc_memories = npc_memories if npc_memories is not None else {}
        self.world_state = world_state if world_state is not None else {}
        self.combat_log = []
        
        # Chargement et traitement de l'image du monstre
        self.monster_surface = None
        if hasattr(monstre, 'image_path'):
            if monstre.race == "The True Hermit":
                # Le boss remplit tout le panneau de vue
                self.monster_surface = load_and_scale_image(monstre.image_path, PANEL_VIEW_W, PANEL_VIEW_H, keep_ratio=False)
            else:
                self.monster_surface = load_and_scale_image(monstre.image_path, 350, 350)
        
        # Intro cinématique bloquante
        self.typewriter_log(f"Un {monstre.race} sauvage apparaît !", show_menu=False, wait_input=False)
        
        options = [("ATTAQUER", "attaquer"), ("FUIR", "fuir")]
        selection = 0
        
        # Boucle de combat
        while self.gui.running:
            # 1. Events
            action_choisie = None
            for event in self.gui.get_events():
                selection, confirmed = handle_menu_navigation(event, selection, len(options))
                
                if confirmed:
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

    def draw_interface(self, selection=0, options=[], show_menu=True):
        self.gui.clear_screen()
        self.gui.draw_stats_panel(hero=self.hero)
        # On retire le titre automatique pour le dessiner nous-même avec la barre de vie
        self.gui.draw_viewport_panel(None)
        # self.gui.draw_dialog_panel("ACTIONS") # Supprimé pour éviter superposition

        self.dessiner_monstre()

        # Interface du bas unifiée (Mode Standard)
        display_options = options if show_menu else None
        
        self.gui.draw_bottom_interface(
            menu_options=display_options,
            selected_index=selection,
            logs=self.combat_log,
            input_mode=False,
            panel_title="COMBAT"
        )
        
        self.gui.update_display()

    def typewriter_log(self, message, show_menu=True, wait_input=True):
        # Utilisation de la fonction centralisée
        draw_callback = lambda: self.draw_interface(show_menu=show_menu)
        
        typewriter_effect(
            self.gui, 
            self.combat_log, 
            message, 
            draw_callback, 
            speed=20,
            skippable=True
        )
        
        if wait_input:
            wait_for_enter(self.gui)

    def ajouter_log(self, message):
        self.combat_log.append(message)
        if len(self.combat_log) > 10:
            self.combat_log.pop(0)

    def dessiner_monstre(self):
        # 1. En-tête : Nom + Barre de vie (HORS de la fenêtre, au-dessus)
        header_y = PANEL_VIEW_Y - 25
        name_x = PANEL_VIEW_X
        
        # Nom du monstre
        name_text = self.monstre.race.upper()
        self.gui.draw_text(name_text, name_x, header_y, color=COLOR_TEXT)
        
        # Calcul de la position de la barre (à droite du nom)
        font = self.gui.font
        name_width = font.size(name_text)[0]
        
        bar_x = name_x + name_width + 20
        bar_y = header_y + 5 # Un peu plus bas pour centrer avec le texte
        bar_w = 200
        bar_h = 12
        
        # Dessin de la barre de vie
        ratio = max(0, self.monstre.points_de_vie / self.monstre.points_de_vie_max)
        # Fond (Sombre)
        pygame.draw.rect(self.gui.screen, (50, 50, 0), (bar_x, bar_y, bar_w, bar_h))
        # Vie (Or / Highlight)
        pygame.draw.rect(self.gui.screen, COLOR_HIGHLIGHT, (bar_x, bar_y, bar_w * ratio, bar_h))
        # Bordure fine pour la barre
        pygame.draw.rect(self.gui.screen, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 1)

        # 2. Image du Monstre (Centrée dans le reste de l'espace)
        cx = PANEL_VIEW_X + PANEL_VIEW_W // 2
        cy = PANEL_VIEW_Y + PANEL_VIEW_H // 2
        
        if self.monster_surface:
            # On centre l'image parfaitement maintenant
            rect = self.monster_surface.get_rect(center=(cx, cy))
            self.gui.screen.blit(self.monster_surface, rect)
        else:
            # Fallback text
            self.gui.draw_text(f"{self.monstre.race}", cx, cy, (255, 100, 100), center=True)

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
            sauvegarder_partie(self.hero, 0, self.npc_memories, self.world_state)
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