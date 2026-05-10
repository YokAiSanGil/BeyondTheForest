import pygame
import os
from display.gui_manager import SCREEN_WIDTH, SCREEN_HEIGHT

class MenuAssets:
    """Manages shared graphical resources for menus (background, title)."""
    def __init__(self):
        self.title_bg = None
        self.title_surface = None
        self._load_assets()

    def _load_assets(self):
        # Load the background image
        # Go up 3 levels: interfaces_gui/menus/ -> interfaces_gui/ -> root/ -> assets/
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.join(base_dir, "assets", "TitleScreen", "ScreenTitleImage_dithered.png")
        print(f"DEBUG: Attempting to load title image from: {img_path}")

        if os.path.exists(img_path):
            try:
                img = pygame.image.load(img_path).convert()
                self.title_bg = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print("DEBUG: Title image loaded successfully")
            except Exception as e:
                print(f"Error loading title image: {e}")
        else:
            print("DEBUG: Title image file not found!")

        self.title_surface = self._generate_dithered_title()
        print(f"DEBUG: Title surface generated: {self.title_surface}")

    def _generate_dithered_title(self):
        """Generate a surface with the vertical dithered title."""
        words = ["BEYOND", "the", "FOREST"]
        font = pygame.font.SysFont("Palatino", 60)

        max_w = 0
        total_h = 0
        surfaces = []
        for w in words:
            s = font.render(w, True, (255, 255, 255))
            surfaces.append(s)
            max_w = max(max_w, s.get_width())
            total_h += s.get_height()

        container = pygame.Surface((max_w, total_h), pygame.SRCALPHA)
        container.fill((0, 0, 0, 0))

        y = 0
        for s in surfaces:
            x = (max_w - s.get_width()) // 2
            container.blit(s, (x, y))
            y += s.get_height()

        # Return the container directly without dithering
        container.set_colorkey((0, 0, 0))

        return container
