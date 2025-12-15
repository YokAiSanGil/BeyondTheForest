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

# Dimensions des zones
SIDEBAR_WIDTH = 320
BOTTOM_HEIGHT = 240
VIEWPORT_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH
VIEWPORT_HEIGHT = SCREEN_HEIGHT - BOTTOM_HEIGHT

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
        """Dessine un panneau générique avec bordure"""
        rect = pygame.Rect(x, y, width, height)
        
        # Fond
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, rect)
        # Bordure
        pygame.draw.rect(self.screen, COLOR_BORDER, rect, 2)
        
        # Titre (optionnel, pour le debug visuel)
        if title:
            text_surf = self.font.render(title, True, COLOR_BORDER)
            self.screen.blit(text_surf, (x + 10, y + 10))

    def draw(self):
        """Boucle de rendu graphique"""
        self.screen.fill(COLOR_BG)

        # 1. Panneau Latéral (Gauche) - Stats
        self.draw_panel(0, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT, "STATS (HEROS)")

        # 2. Viewport (Haut-Droite) - Monde/Combat
        self.draw_panel(SIDEBAR_WIDTH, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT, "VIEWPORT (MONDE)")

        # 3. Panneau de Dialogue (Bas-Droite) - Logs/Input
        self.draw_panel(SIDEBAR_WIDTH, VIEWPORT_HEIGHT, VIEWPORT_WIDTH, BOTTOM_HEIGHT, "DIALOGUE / INPUT")

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
