import pygame
import sys
from display.effects import create_scanlines, get_flicker_color
from display.config import GameConfig

# --- CONFIGURATION ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
COLOR_BG = (5, 5, 10)
COLOR_PANEL_BG = (0, 0, 0, 180)  # Semi-transparent black
COLOR_BORDER = (255, 255, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_HIGHLIGHT = (255, 215, 0)

# Dimensions
MARGIN = 20
HEADER_HEIGHT = 30  # Space for the title above the window
SIDEBAR_WIDTH = 300
PANEL_STATS_X = MARGIN
PANEL_STATS_Y = MARGIN + HEADER_HEIGHT
PANEL_STATS_W = SIDEBAR_WIDTH
PANEL_STATS_H = SCREEN_HEIGHT - (2 * MARGIN) - HEADER_HEIGHT
PANEL_VIEW_X = PANEL_STATS_X + PANEL_STATS_W + MARGIN
PANEL_VIEW_Y = MARGIN + HEADER_HEIGHT
PANEL_VIEW_W = SCREEN_WIDTH - PANEL_VIEW_X - MARGIN
PANEL_VIEW_H = 400
PANEL_DIALOG_X = PANEL_VIEW_X
PANEL_DIALOG_Y = PANEL_VIEW_Y + PANEL_VIEW_H + MARGIN + HEADER_HEIGHT
PANEL_DIALOG_W = PANEL_VIEW_W
PANEL_DIALOG_H = SCREEN_HEIGHT - PANEL_DIALOG_Y - MARGIN

# New constants for split dialog panel
PANEL_MENU_WIDTH = 200
PANEL_LOG_X = PANEL_DIALOG_X + PANEL_MENU_WIDTH + MARGIN
PANEL_LOG_W = PANEL_DIALOG_W - PANEL_MENU_WIDTH - MARGIN

class GuiManager:
    """
    Manages Pygame initialization, the main window, and basic drawing functions.
    Singleton shared by all phases.
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
        pygame.display.set_caption("BEYOND the FOREST - GUI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier New", 20, bold=True)
        self.title_font = pygame.font.SysFont("Courier New", 40, bold=True)
        self.scanline_surface = create_scanlines(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.running = True
        self.initialized = True

        # Load settings
        self.config = GameConfig()
        self.settings = {
            "debug_force_hermit": getattr(self.config, "debug_force_hermit", False)
        }

    def clear_screen(self):
        self.screen.fill(COLOR_BG)

    def draw_background_image(self, image):
        """Draw a background image (already dithered)."""
        if image:
            self.screen.blit(image, (0, 0))

    def update_display(self):
        if GameConfig().enable_scanlines:
            self.screen.blit(self.scanline_surface, (0, 0))
        pygame.display.flip()
        self.clock.tick(FPS)

    def draw_panel(self, x, y, w, h, title=None):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, rect, border_radius=15)

        # CRT Flicker effect
        if GameConfig().enable_flicker:
            flicker_color = get_flicker_color()
        else:
            flicker_color = COLOR_BORDER

        pygame.draw.rect(self.screen, flicker_color, rect, 2, border_radius=15)
        if title:
            # Title outside the window, above and to the left
            text = self.font.render(title, True, flicker_color)
            self.screen.blit(text, (x, y - 25))

    def draw_text(self, text, x, y, color=COLOR_TEXT, font=None, center=False):
        if font is None: font = self.font
        surf = font.render(text, True, color)
        if center:
            rect = surf.get_rect(center=(x, y))
            self.screen.blit(surf, rect)
        else:
            self.screen.blit(surf, (x, y))

    def draw_logs(self, messages, x, y, max_width, max_lines=4, color=COLOR_TEXT, font=None):
        """Display logs with automatic line wrapping and limit the number of visible lines."""
        if font is None: font = self.font

        wrapped_lines = []
        for msg in messages:
            words = msg.split(' ')
            current_line = []
            first_line_of_msg = True

            for word in words:
                prefix = "> " if first_line_of_msg else "  "
                test_line = prefix + ' '.join(current_line + [word])
                if font.size(test_line)[0] <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        wrapped_lines.append(prefix + ' '.join(current_line))
                    current_line = [word]
                    first_line_of_msg = False

            prefix = "> " if first_line_of_msg else "  "
            if current_line:
                wrapped_lines.append(prefix + ' '.join(current_line))

        # Keep only last max_lines
        lines_to_draw = wrapped_lines[-max_lines:]

        for i, line in enumerate(lines_to_draw):
            self.draw_text(line, x, y + i * font.get_linesize(), color, font)

    def get_events(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
        return events

    # Helpers for drawing in specific zones
    def draw_stats_panel(self, title="STATS", hero=None):
        self.draw_panel(PANEL_STATS_X, PANEL_STATS_Y, PANEL_STATS_W, PANEL_STATS_H, title)

        if hero:
            # Display hero stats
            start_x = PANEL_STATS_X + 20
            start_y = PANEL_STATS_Y + 40
            line_height = 30

            self.draw_text(f"NAME: {hero.name}", start_x, start_y)
            self.draw_text(f"RACE: {hero.race}", start_x, start_y + line_height)

            # HP bar
            hp_y = start_y + line_height * 2
            self.draw_text(f"HP  : {hero.hp}/{hero.max_hp}", start_x, hp_y)

            # Draw the bar
            bar_w = PANEL_STATS_W - 40
            bar_h = 15
            bar_y = hp_y + 25

            # Bar background (dark)
            pygame.draw.rect(self.screen, (50, 50, 0), (start_x, bar_y, bar_w, bar_h))
            # Current HP (Gold / Highlight)
            ratio = max(0, hero.hp / hero.max_hp)
            pygame.draw.rect(self.screen, COLOR_HIGHLIGHT, (start_x, bar_y, bar_w * ratio, bar_h))

            # Stats
            stats_y = bar_y + 30
            self.draw_text(f"STR : {hero.strength}", start_x, stats_y)
            self.draw_text(f"END : {hero.endurance}", start_x, stats_y + line_height)

            # Gold and Leather
            res_y = stats_y + line_height * 2 + 10
            self.draw_text(f"GOLD: {hero.gold}", start_x, res_y, COLOR_HIGHLIGHT)
            self.draw_text(f"LTHR: {hero.leather}", start_x, res_y + line_height)

    def draw_viewport_panel(self, title="VIEWPORT"):
        self.draw_panel(PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H, title)

    def draw_dialog_panel(self, title="DIALOGUE"):
        self.draw_panel(PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W, PANEL_DIALOG_H, title)

    def draw_bottom_interface(self, menu_options=None, selected_index=0, logs=None, input_mode=False, input_text="", input_prompt="", panel_title=None):
        """
        Handles the bottom area display in a flexible way.

        Args:
            menu_options (list): List of options for the menu (Standard Mode).
            selected_index (int): Currently selected index (Standard Mode).
            logs (list): List of messages to display (Standard Mode).
            input_mode (bool): If True, shows a full-width input field instead of split menu/log.
            input_text (str): The text currently being typed (Input Mode).
            input_prompt (str): The question or prompt (Input Mode).
            panel_title (str): Panel title (default "ACTIONS" or "INPUT").
        """
        # Adaptive title
        if panel_title is None:
            title = "INPUT" if input_mode else "ACTIONS"
        else:
            title = panel_title

        self.draw_dialog_panel(title)

        if input_mode:
            # --- INPUT MODE (Full width) ---
            x = PANEL_DIALOG_X + 20
            y = PANEL_DIALOG_Y + 30

            # Prompt
            self.draw_text(input_prompt, x, y, COLOR_HIGHLIGHT)

            # Input field
            y_text = y + 40
            cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
            full_text = input_text + cursor

            # Wrapping logic
            max_width = PANEL_DIALOG_W - 40
            font = self.font
            lines = []
            words = full_text.split(' ')
            current_line = []

            for word in words:
                test_line = ' '.join(current_line + [word])
                if font.size(test_line)[0] <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]

            if current_line:
                lines.append(' '.join(current_line))

            # Limit visible lines to fit in panel
            max_lines = 5
            visible_lines = lines[-max_lines:]

            for i, line in enumerate(visible_lines):
                self.draw_text(line, x, y_text + i * font.get_linesize(), COLOR_TEXT)

            # Help text
            y_help = PANEL_DIALOG_Y + PANEL_DIALOG_H - 30
            self.draw_text("[Enter] Confirm   [Esc] Cancel", x, y_help, (150, 150, 150), font=pygame.font.SysFont("Courier New", 16))

        else:
            # --- STANDARD MODE (Split Menu / Logs) ---
            # 1. Menu (Left)
            if menu_options:
                menu_x = PANEL_DIALOG_X + 20
                menu_y = PANEL_DIALOG_Y + 30
                for i, option in enumerate(menu_options):
                    # Handle if option is a tuple (Label, ID) or just a str
                    label = option[0] if isinstance(option, tuple) else option

                    color = COLOR_HIGHLIGHT if i == selected_index else COLOR_TEXT
                    prefix = "► " if i == selected_index else "  "
                    self.draw_text(f"{prefix}{label}", menu_x, menu_y + i * 30, color)

            # 2. Logs (Right)
            if logs:
                # Use existing draw_logs method which handles wrapping
                self.draw_logs(logs, PANEL_LOG_X, PANEL_DIALOG_Y + 30, PANEL_LOG_W, max_lines=5)

    def input_text(self, prompt, x, y, max_length=15):
        """
        Display a prompt and wait for text input from the user.
        Blocking until Enter is pressed.
        """
        # Capture current background (without scanlines if update_display wasn't just called)
        # This avoids scanline accumulation each frame of the loop
        background_snapshot = self.screen.copy()

        input_text = ""
        active = True

        while active and self.running:
            events = self.get_events()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if input_text.strip():  # Only confirm if non-empty
                            active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < max_length and event.unicode.isprintable():
                            input_text += event.unicode

            # 1. Restore clean background (clears previous frame)
            self.screen.blit(background_snapshot, (0, 0))

            # 2. Draw input panel on top
            self.draw_dialog_panel("INPUT")
            self.draw_text(prompt, x, y)

            # Blinking cursor
            cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
            self.draw_text(input_text + cursor, x, y + 40, COLOR_HIGHLIGHT)

            # 3. Apply scanlines and refresh
            self.update_display()

        return input_text
