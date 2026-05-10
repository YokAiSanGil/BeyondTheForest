from display.gui_manager import GuiManager
from interfaces_gui.menus.menu_assets import MenuAssets
from interfaces_gui.menus.title_screen import TitleScreen
from interfaces_gui.menus.character_creation import CharacterCreation
from interfaces_gui.menus.save_load import SaveLoadMenu

class PhaseMenuGUI:
    """
    Main controller for the menu phase.
    Delegates logic to sub-modules in interfaces_gui/menus/.
    """
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()

        # Initialise components
        self.assets = MenuAssets()
        self.char_creation = CharacterCreation(self.gui, self.assets)
        self.save_load = SaveLoadMenu(self.gui, self.assets)
        self.title_screen = TitleScreen(self.gui, self.assets, self.save_load)

    def show_main_menu(self):
        """Display the title screen and main menu."""
        return self.title_screen.run()

    def create_hero(self):
        """Launch the character creation sequence."""
        return self.char_creation.run()
