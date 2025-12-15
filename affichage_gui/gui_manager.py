import pygame
import sys
from affichage.ascii_art import HUMAIN, NAIN
from affichage_gui.dithering import apply_jarvis_judice_ninke_dithering

# --- CONFIGURATION ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Couleurs
COLOR_BG = (5, 5, 10)
COLOR_PANEL_BG = (15, 15, 20)
COLOR_BORDER = (100, 100, 120)
COLOR_TEXT = (200, 200, 200)
COLOR_HIGHLIGHT = (255, 215, 0)

# Dimensions
MARGIN = 20
SIDEBAR_WIDTH = 300
PANEL_STATS_X = MARGIN
PANEL_STATS_Y = MARGIN
PANEL_STATS_W = SIDEBAR_WIDTH
PANEL_STATS_H = SCREEN_HEIGHT - (2 * MARGIN)
PANEL_VIEW_X = PANEL_STATS_X + PANEL_STATS_W + MARGIN
PANEL_VIEW_Y = MARGIN
PANEL_VIEW_W = SCREEN_WIDTH - PANEL_VIEW_X - MARGIN
PANEL_VIEW_H = 400
PANEL_DIALOG_X = PANEL_VIEW_X
PANEL_DIALOG_Y = PANEL_VIEW_Y + PANEL_VIEW_H + MARGIN
PANEL_DIALOG_W = PANEL_VIEW_W
PANEL_DIALOG_H = SCREEN_HEIGHT - PANEL_DIALOG_Y - MARGIN

class GuiManager:
    """
    Gère l'initialisation de Pygame, la fenêtre principale et les fonctions de dessin de base.
    Singleton partagé par toutes les phases.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GuiManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def init(self):
        if self.initialized:
            return
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Heroes vs Monsters - GUI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier New", 20, bold=True)
        self.title_font = pygame.font.SysFont("Courier New", 40, bold=True)
        self.running = True
        self.initialized = True

    def clear_screen(self):
        self.screen.fill(COLOR_BG)

    def draw_background_image(self, image):
        """Dessine une image de fond (déjà ditherée)."""
        if image:
            self.screen.blit(image, (0, 0))

    def update_display(self):
        pygame.display.flip()
        self.clock.tick(FPS)

    def draw_panel(self, x, y, w, h, title=None):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, rect, border_radius=15)
        pygame.draw.rect(self.screen, COLOR_BORDER, rect, 2, border_radius=15)
        if title:
            text = self.font.render(title, True, COLOR_BORDER)
            self.screen.blit(text, (x + 20, y + 15))

    def draw_text(self, text, x, y, color=COLOR_TEXT, font=None, center=False):
        if font is None: font = self.font
        surf = font.render(text, True, color)
        if center:
            rect = surf.get_rect(center=(x, y))
            self.screen.blit(surf, rect)
        else:
            self.screen.blit(surf, (x, y))

    def get_events(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
        return events

    # Helpers pour dessiner dans les zones spécifiques
    def draw_stats_panel(self, title="STATS", hero=None):
        self.draw_panel(PANEL_STATS_X, PANEL_STATS_Y, PANEL_STATS_W, PANEL_STATS_H, title)
        
        if hero:
            # Affichage de l'avatar
            art = HUMAIN if hero.race == "Humain" else NAIN
            lines = art.strip().split('\n')
            avatar_y = PANEL_STATS_Y + 40
            for i, line in enumerate(lines):
                self.draw_text(line, PANEL_STATS_X + 20, avatar_y + i * 15, (150, 150, 150))

            # Affichage des stats du héros
            start_x = PANEL_STATS_X + 20
            start_y = avatar_y + (len(lines) * 15) + 20
            line_height = 30
            
            self.draw_text(f"NOM : {hero.nom}", start_x, start_y)
            self.draw_text(f"RACE: {hero.race}", start_x, start_y + line_height)
            
            # Barre de vie
            pv_y = start_y + line_height * 2
            self.draw_text(f"PV  : {hero.points_de_vie}/{hero.points_de_vie_max}", start_x, pv_y)
            
            # Dessin de la barre
            bar_w = PANEL_STATS_W - 40
            bar_h = 15
            bar_y = pv_y + 25
            
            # Fond barre (rouge sombre)
            pygame.draw.rect(self.screen, (50, 0, 0), (start_x, bar_y, bar_w, bar_h))
            # Vie actuelle (rouge vif)
            ratio = max(0, hero.points_de_vie / hero.points_de_vie_max)
            pygame.draw.rect(self.screen, (200, 20, 20), (start_x, bar_y, bar_w * ratio, bar_h))
            
            # Stats
            stats_y = bar_y + 30
            self.draw_text(f"FORCE: {hero.force}", start_x, stats_y)
            self.draw_text(f"ENDU : {hero.endurance}", start_x, stats_y + line_height)
            
            # Or et Cuir
            res_y = stats_y + line_height * 2 + 10
            self.draw_text(f"OR   : {hero.gold}", start_x, res_y, COLOR_HIGHLIGHT)
            self.draw_text(f"CUIR : {hero.cuir}", start_x, res_y + line_height)

    def draw_viewport_panel(self, title="VIEWPORT"):
        self.draw_panel(PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, title)

    def draw_dialog_panel(self, title="DIALOGUE"):
        self.draw_panel(PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W, PANEL_DIALOG_H, title)

    def input_text(self, prompt, x, y, max_length=15):
        """
        Affiche un prompt et attend une saisie texte de l'utilisateur.
        Bloquant jusqu'à ce que Entrée soit pressé.
        """
        input_text = ""
        active = True
        
        while active and self.running:
            events = self.get_events()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if input_text.strip(): # Valider seulement si non vide
                            active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < max_length and event.unicode.isprintable():
                            input_text += event.unicode
            
            # Redessiner (on doit redessiner tout l'écran pour éviter les artefacts)
            # Note: Idéalement on passerait une callback de dessin pour le fond, 
            # mais ici on va juste effacer la zone de texte ou redessiner le panneau dialogue
            # Pour simplifier, on suppose que l'appelant redessine le fond avant d'appeler input_text
            # MAIS comme c'est une boucle bloquante, on doit gérer le rafraichissement ici.
            # On va faire simple : on redessine juste un rectangle noir sur la zone de texte
            
            # Pour faire propre, on demande à l'appelant de gérer le dessin de fond via une fonction lambda ?
            # Trop complexe. On va juste redessiner le panneau dialogue ici.
            
            self.draw_dialog_panel("SAISIE")
            self.draw_text(prompt, x, y)
            
            # Curseur clignotant
            cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
            self.draw_text(input_text + cursor, x, y + 40, COLOR_HIGHLIGHT)
            
            self.update_display()
            
        return input_text
