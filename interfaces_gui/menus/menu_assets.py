import pygame
import os
from affichage_gui.gui_manager import SCREEN_WIDTH, SCREEN_HEIGHT

class MenuAssets:
    """Gère les ressources graphiques partagées des menus (Fond, Titre)."""
    def __init__(self):
        self.title_bg = None
        self.title_surface = None
        self._load_assets()

    def _load_assets(self):
        # Chargement de l'image de fond
        # On remonte de 3 niveaux : interfaces_gui/menus/ -> interfaces_gui/ -> root/ -> assets/
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.join(base_dir, "assets", "TitleScreen", "ScreenTitleImage_dithered.png")
        print(f"DEBUG: Tentative chargement image titre depuis: {img_path}")
        
        if os.path.exists(img_path):
            try:
                img = pygame.image.load(img_path).convert()
                self.title_bg = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print("DEBUG: Image titre chargée avec succès")
            except Exception as e:
                print(f"Erreur chargement image titre: {e}")
        else:
            print("DEBUG: Fichier image titre introuvable !")
        
        self.title_surface = self._generate_dithered_title()
        print(f"DEBUG: Surface titre générée: {self.title_surface}")

    def _generate_dithered_title(self):
        """Génère une surface avec le titre vertical dithered."""
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
            
        # On retourne le conteneur directement sans dithering
        container.set_colorkey((0, 0, 0))
        
        return container
