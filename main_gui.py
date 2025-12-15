import pygame
import sys

# --- CONFIGURATION ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Couleurs (Palette Rétro Sombre)
COLOR_BG = (5, 5, 10)           # Noir bleuté très profond
COLOR_PANEL_BG = (15, 15, 20)   # Gris sombre pour les fonds de panneaux
COLOR_BORDER = (100, 100, 120)  # Gris bleuté pour les bordures
COLOR_TEXT = (200, 200, 200)    # Blanc cassé

# Dimensions des zones (ajustées avec marges)
MARGIN = 20  # Marge externe et entre les fenêtres
SIDEBAR_WIDTH = 300

# Calculs dynamiques pour que ça rentre dans l'écran
# Panneau Gauche
PANEL_STATS_X = MARGIN
PANEL_STATS_Y = MARGIN
PANEL_STATS_W = SIDEBAR_WIDTH
PANEL_STATS_H = SCREEN_HEIGHT - (2 * MARGIN)

# Panneau Haut-Droite (Viewport)
PANEL_VIEW_X = PANEL_STATS_X + PANEL_STATS_W + MARGIN
PANEL_VIEW_Y = MARGIN
PANEL_VIEW_W = SCREEN_WIDTH - PANEL_VIEW_X - MARGIN
PANEL_VIEW_H = 400 # Hauteur fixe pour le viewport

# Panneau Bas-Droite (Dialogue)
PANEL_DIALOG_X = PANEL_VIEW_X
PANEL_DIALOG_Y = PANEL_VIEW_Y + PANEL_VIEW_H + MARGIN
PANEL_DIALOG_W = PANEL_VIEW_W
PANEL_DIALOG_H = SCREEN_HEIGHT - PANEL_DIALOG_Y - MARGIN

class GameGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Heroes vs Monsters - GUI Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Police rétro (type machine à écrire)
        # On essaie de charger une police système monospace, sinon défaut
        self.font = pygame.font.SysFont("Courier New", 20, bold=True)

        # Préparation de l'effet Dithering (Tramage)
        self.dither_surface = self.creer_effet_dithering()

    def creer_effet_dithering(self):
        """
        Crée une surface transparente avec un motif de points 
        pour simuler un écran rétro basse résolution.
        """
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # On dessine des lignes horizontales fines semi-transparentes (scanlines)
        # et quelques points pour le bruit
        for y in range(0, SCREEN_HEIGHT, 2):
            pygame.draw.line(surface, (0, 0, 0, 40), (0, y), (SCREEN_WIDTH, y))
        
        return surface

    def handle_events(self):
        """Gestion des entrées clavier (Flèches + Entrée + Echap)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Placeholder pour les contrôles futurs
                elif event.key == pygame.K_UP:
                    print("Haut")
                elif event.key == pygame.K_DOWN:
                    print("Bas")
                elif event.key == pygame.K_RETURN:
                    print("Entrée")

    def draw_panel(self, x, y, width, height, title=None):
        """Dessine un panneau flottant avec bords arrondis"""
        rect = pygame.Rect(x, y, width, height)
        
        # Fond avec coins arrondis
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, rect, border_radius=15)
        
        # Bordure avec coins arrondis
        pygame.draw.rect(self.screen, COLOR_BORDER, rect, 2, border_radius=15)
        
        # Titre
        if title:
            text_surf = self.font.render(title, True, COLOR_BORDER)
            # Centrer le titre un peu mieux
            self.screen.blit(text_surf, (x + 20, y + 15))

    def draw(self):
        """Boucle de rendu graphique"""
        self.screen.fill(COLOR_BG)

        # 1. Panneau Latéral (Gauche) - Stats
        self.draw_panel(PANEL_STATS_X, PANEL_STATS_Y, PANEL_STATS_W, PANEL_STATS_H, "STATS")

        # 2. Viewport (Haut-Droite) - Monde/Combat
        self.draw_panel(PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, "VIEWPORT")

        # 3. Panneau de Dialogue (Bas-Droite) - Logs/Input
        self.draw_panel(PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W, PANEL_DIALOG_H, "DIALOGUE")

        # 4. Overlay Dithering (toujours à la fin)
        self.screen.blit(self.dither_surface, (0, 0))

        pygame.display.flip()

    def run(self):
        """Boucle principale"""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameGUI()
    game.run()
