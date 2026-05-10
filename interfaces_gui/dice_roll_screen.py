import random
import pygame
from display.gui_manager import (
    GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT,
    SCREEN_WIDTH, SCREEN_HEIGHT
)
from utils.dice import Die


_DOT_GRIDS = {
    1: [(1, 1)],
    2: [(0, 0), (2, 2)],
    3: [(0, 0), (1, 1), (2, 2)],
    4: [(0, 0), (2, 0), (0, 2), (2, 2)],
    5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)],
    6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)],
}

_POPUP_SIZE  = 380          # Square popup side length
_DIE_SIZE    = 160
_DOT_RADIUS  = 12
_DOT_PADDING = 36


class DiceRollScreen:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()

    def show(self, title: str = "ROLL THE DICE") -> int:
        """
        Draw a popup panel over the current screen (background stays visible).
        - First Enter  → throws the die (animation settles on result)
        - Second Enter → closes the popup and returns the value
        """
        final_value  = Die.roll(1, 6)
        shuffle_value = random.randint(1, 6)
        locked       = False
        last_shuffle = pygame.time.get_ticks()
        settle_start = None

        # Snapshot the screen as it is right now so we can redraw it each frame
        background = self.gui.screen.copy()

        # Popup geometry — centred on screen
        px = (SCREEN_WIDTH  - _POPUP_SIZE) // 2
        py = (SCREEN_HEIGHT - _POPUP_SIZE) // 2

        while self.gui.running:
            now = pygame.time.get_ticks()

            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if not locked:
                        locked       = True
                        settle_start = now          # Begin settle animation
                    else:
                        return final_value          # Confirm result

            # Shuffle before throw
            if not locked:
                if now - last_shuffle >= 80:
                    shuffle_value = random.randint(1, 6)
                    last_shuffle  = now

            # Short settle animation: rapid → slow → stop
            if locked and settle_start:
                elapsed = now - settle_start
                if elapsed < 400:
                    interval = 60
                elif elapsed < 700:
                    interval = 130
                elif elapsed < 900:
                    interval = 250
                else:
                    settle_start = None             # Animation done, lock final face
                if settle_start and now - last_shuffle >= interval:
                    shuffle_value = random.randint(1, 6)
                    last_shuffle  = now

            face      = final_value if (locked and settle_start is None) else shuffle_value
            dot_color = COLOR_TEXT  if (locked and settle_start is None) else COLOR_HIGHLIGHT
            prompt    = "[Enter] Continue" if (locked and settle_start is None) else "[Enter] Throw!"

            self._draw(background, px, py, face, dot_color, title, prompt)

        return final_value

    def _draw(self, background, px, py, face, dot_color, title, prompt):
        # Restore the game screen behind the popup
        self.gui.screen.blit(background, (0, 0))

        # Popup panel (uses the same draw_panel style as all other windows)
        self.gui.draw_panel(px, py, _POPUP_SIZE, _POPUP_SIZE, title=title)

        # Die box — centred inside the popup
        cx = px + _POPUP_SIZE // 2
        cy = py + _POPUP_SIZE // 2 - 20

        bx = cx - _DIE_SIZE // 2
        by = cy - _DIE_SIZE // 2

        pygame.draw.rect(self.gui.screen, (15, 15, 25), (bx, by, _DIE_SIZE, _DIE_SIZE), border_radius=18)
        pygame.draw.rect(self.gui.screen, (255, 255, 255), (bx, by, _DIE_SIZE, _DIE_SIZE), 2, border_radius=18)

        self._draw_dots(face, bx, by, dot_color)

        # Value label
        self.gui.draw_text(str(face), cx, by + _DIE_SIZE + 14, COLOR_HIGHLIGHT, font=self.gui.title_font, center=True)

        # Prompt at the bottom of the popup
        self.gui.draw_text(prompt, cx, py + _POPUP_SIZE - 28, COLOR_TEXT, center=True)

        self.gui.update_display()

    def _draw_dots(self, face, bx, by, color):
        xs = [bx + _DOT_PADDING, bx + _DIE_SIZE // 2, bx + _DIE_SIZE - _DOT_PADDING]
        ys = [by + _DOT_PADDING, by + _DIE_SIZE // 2, by + _DIE_SIZE - _DOT_PADDING]
        for col, row in _DOT_GRIDS.get(face, []):
            pygame.draw.circle(self.gui.screen, color, (xs[col], ys[row]), _DOT_RADIUS)
