import random
import pygame
from display.gui_manager import (
    GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, COLOR_BORDER, COLOR_BG,
    PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H
)
from utils.dice import Die


# Dot layout for each face value, as (col, row) offsets — resolved at draw time
_DOT_GRIDS = {
    1: [(1, 1)],
    2: [(0, 0), (2, 2)],
    3: [(0, 0), (1, 1), (2, 2)],
    4: [(0, 0), (2, 0), (0, 2), (2, 2)],
    5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)],
    6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)],
}

_DIE_SIZE = 180
_DOT_RADIUS = 12
_DOT_PADDING = 40  # Distance from edge of box to outer dots


class DiceRollScreen:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()

    def show(self, title: str = "ROLL THE DICE", hero=None) -> int:
        """
        Display an animated dice roll screen.
        Blocks until the player confirms. Returns the rolled value (1–6).
        """
        final_value = Die.roll(1, 6)   # Outcome decided before animation starts
        shuffle_value = random.randint(1, 6)

        locked = False
        waiting_confirm = False
        shuffle_start = pygame.time.get_ticks()
        last_shuffle = shuffle_start

        while self.gui.running:
            now = pygame.time.get_ticks()
            elapsed = now - shuffle_start

            # --- Events ---
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if not locked:
                        locked = True
                        waiting_confirm = True
                    elif waiting_confirm:
                        return final_value

            # --- Shuffle animation ---
            if not locked:
                interval = 80 if elapsed < 600 else 120
                if now - last_shuffle >= interval:
                    shuffle_value = random.randint(1, 6)
                    last_shuffle = now
                if elapsed >= 900:
                    locked = True
                    waiting_confirm = True

            # --- Draw ---
            face = final_value if locked else shuffle_value
            dot_color = COLOR_TEXT if locked else COLOR_HIGHLIGHT
            prompt = "[Enter] Continue" if locked else "[Enter] Roll!"
            self._draw(face, dot_color, title, prompt, hero)

        return final_value

    def _draw(self, face: int, dot_color: tuple, title: str, prompt: str, hero) -> None:
        self.gui.clear_screen()

        if hero:
            self.gui.draw_stats_panel(hero=hero)

        self.gui.draw_viewport_panel(title)

        # Die box — centred in the viewport panel
        cx = PANEL_VIEW_X + PANEL_VIEW_W // 2
        cy = PANEL_VIEW_Y + PANEL_VIEW_H // 2

        box_x = cx - _DIE_SIZE // 2
        box_y = cy - _DIE_SIZE // 2

        # Background
        pygame.draw.rect(self.gui.screen, (15, 15, 25), (box_x, box_y, _DIE_SIZE, _DIE_SIZE), border_radius=20)
        # Border
        pygame.draw.rect(self.gui.screen, COLOR_BORDER, (box_x, box_y, _DIE_SIZE, _DIE_SIZE), 2, border_radius=20)

        # Dots
        self._draw_dots(face, box_x, box_y, dot_color)

        # Roll value label below the die
        label = str(face) if face else "?"
        self.gui.draw_text(label, cx, box_y + _DIE_SIZE + 20, COLOR_HIGHLIGHT, font=self.gui.title_font, center=True)

        # Prompt at the bottom of the viewport panel
        prompt_y = PANEL_VIEW_Y + PANEL_VIEW_H - 30
        self.gui.draw_text(prompt, cx, prompt_y, COLOR_TEXT, center=True)

        self.gui.update_display()

    def _draw_dots(self, face: int, box_x: int, box_y: int, color: tuple) -> None:
        dots = _DOT_GRIDS.get(face, [])

        # Three possible X positions (left, centre, right)
        xs = [
            box_x + _DOT_PADDING,
            box_x + _DIE_SIZE // 2,
            box_x + _DIE_SIZE - _DOT_PADDING,
        ]
        # Three possible Y positions (top, centre, bottom)
        ys = [
            box_y + _DOT_PADDING,
            box_y + _DIE_SIZE // 2,
            box_y + _DIE_SIZE - _DOT_PADDING,
        ]

        for col, row in dots:
            pygame.draw.circle(self.gui.screen, color, (xs[col], ys[row]), _DOT_RADIUS)
