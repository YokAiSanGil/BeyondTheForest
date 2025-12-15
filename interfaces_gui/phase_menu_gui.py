from affichage_gui.gui_manager import GuiManager
from interfaces_gui.menus.menu_assets import MenuAssets
from interfaces_gui.menus.title_screen import TitleScreen
from interfaces_gui.menus.character_creation import CharacterCreation
from interfaces_gui.menus.save_load import SaveLoadMenu

class PhaseMenuGUI:
    """
    Contrôleur principal pour la phase de menu.
    Délègue la logique aux sous-modules dans interfaces_gui/menus/.
    """
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()
        
        # Initialisation des composants
        self.assets = MenuAssets()
        self.char_creation = CharacterCreation(self.gui, self.assets)
        self.save_load = SaveLoadMenu(self.gui, self.assets)
        self.title_screen = TitleScreen(self.gui, self.assets, self.save_load)

    def afficher_menu_principal(self):
        """Affiche l'écran titre et le menu principal."""
        return self.title_screen.run()

    def creer_hero(self):
        """Lance la séquence de création de personnage."""
        return self.char_creation.run()
