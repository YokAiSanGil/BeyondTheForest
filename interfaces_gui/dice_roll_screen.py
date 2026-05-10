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

_POPUP_SIZE  = 380
_DIE_SIZE    = 160
_DOT_RADIUS  = 12
_DOT_PADDING = 36

_BLACK       = (0, 0, 0)
_WHITE       = (255, 255, 255)


class DiceRollScreen:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()

    def show(self, title: str = "ROLL THE DICE") -> int:
        """
        Popup panel over the current screen.
        - Before throw : prompt only, die hidden
        - First Enter  : die appears and settles (white face, black dots)
        - Settled      : die turns gold with black dots
        - Second Enter : closes and returns the value (1–6)
        """
        final_value   = Die.roll(1, 6)
        shuffle_value = random.randint(1, 6)
        locked        = False
        settle_start  = None
        last_shuffle  = pygame.time.get_ticks()

        background = self.gui.screen.copy()

        px = (SCREEN_WIDTH  - _POPUP_SIZE) // 2
        py = (SCREEN_HEIGHT - _POPUP_SIZE) // 2

        while self.gui.running:
            now = pygame.time.get_ticks()

            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if not locked:
                        locked       = True
                        settle_start = now
                    else:
                        return final_value

            # Settle animation: rapid → slow → stop
            if locked and settle_start is not None:
                elapsed = now - settle_start
                if   elapsed < 400: interval = 60
                elif elapsed < 700: interval = 130
                elif elapsed < 900: interval = 250
                else:
                    settle_start = None     # Fully settled
                if settle_start is not None and now - last_shuffle >= interval:
                    shuffle_value = random.randint(1, 6)
                    last_shuffle  = now

            # Determine state
            settled  = locked and settle_start is None
            rolling  = locked and settle_start is not None
            waiting  = not locked

            if waiting:
                face       = None
                die_color  = None
                dot_color  = None
                prompt     = "[Enter] Throw your dice!"
            elif rolling:
                face       = shuffle_value
                die_color  = _WHITE
                dot_color  = _BLACK
                prompt     = ""
            else:  # settled
                face       = final_value
                die_color  = COLOR_HIGHLIGHT
                dot_color  = _BLACK
                prompt     = "[Enter] Continue"

            self._draw(background, px, py, face, die_color, dot_color, title, prompt)

        return final_value

    def _draw(self, background, px, py, face, die_color, dot_color, title, prompt):
        self.gui.screen.blit(background, (0, 0))
        self.gui.draw_panel(px, py, _POPUP_SIZE, _POPUP_SIZE, title=title)

        cx = px + _POPUP_SIZE // 2
        cy = py + _POPUP_SIZE // 2 - 10

        # Die — only shown after throw
        if face is not None:
            bx = cx - _DIE_SIZE // 2
            by = cy - _DIE_SIZE // 2
            pygame.draw.rect(self.gui.screen, die_color,  (bx, by, _DIE_SIZE, _DIE_SIZE), border_radius=18)
            pygame.draw.rect(self.gui.screen, _BLACK,     (bx, by, _DIE_SIZE, _DIE_SIZE), 2, border_radius=18)
            self._draw_dots(face, bx, by, dot_color)

        if prompt:
            self.gui.draw_text(prompt, cx, py + _POPUP_SIZE - 28, COLOR_TEXT, center=True)

        self.gui.update_display()

    def _draw_dots(self, face, bx, by, color):
        xs = [bx + _DOT_PADDING, bx + _DIE_SIZE // 2, bx + _DIE_SIZE - _DOT_PADDING]
        ys = [by + _DOT_PADDING, by + _DIE_SIZE // 2, by + _DIE_SIZE - _DOT_PADDING]
        for col, row in _DOT_GRIDS.get(face, []):
            pygame.draw.circle(self.gui.screen, color, (xs[col], ys[row]), _DOT_RADIUS)
