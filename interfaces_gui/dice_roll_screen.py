import random
import pygame
from display.gui_manager import (
    GuiManager, COLOR_HIGHLIGHT, COLOR_TEXT, COLOR_BORDER,
    SCREEN_WIDTH, SCREEN_HEIGHT
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

_DIE_SIZE = 200
_DOT_RADIUS = 14
_DOT_PADDING = 44


class DiceRollScreen:
    def __init__(self):
        self.gui = GuiManager()
        self.gui.init()

    def show(self, title: str = "ROLL THE DICE", hero=None) -> int:
        """
        Display a full-screen dice overlay.
        Dice shuffles until the player presses Enter to throw, then
        a second Enter confirms the result. Returns the rolled value (1–6).
        """
        final_value = Die.roll(1, 6)   # Outcome fixed before the throw
        shuffle_value = random.randint(1, 6)
        locked = False
        last_shuffle = pygame.time.get_ticks()

        while self.gui.running:
            now = pygame.time.get_ticks()

            # --- Events ---
            for event in self.gui.get_events():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if not locked:
                        locked = True          # First Enter = throw
                    else:
                        return final_value     # Second Enter = confirm

            # --- Keep shuffling until thrown ---
            if not locked:
                interval = 80
                if now - last_shuffle >= interval:
                    shuffle_value = random.randint(1, 6)
                    last_shuffle = now

            # --- Draw ---
            face = final_value if locked else shuffle_value
            dot_color = COLOR_TEXT if locked else COLOR_HIGHLIGHT
            prompt = "[Enter] Continue" if locked else "[Enter] Throw!"
            self._draw(face, dot_color, title, prompt, hero)

        return final_value

    def _draw(self, face: int, dot_color: tuple, title: str, prompt: str, hero) -> None:
        # Draw the existing game state first (stats panel if hero provided)
        self.gui.clear_screen()
        if hero:
            self.gui.draw_stats_panel(hero=hero)

        # Full-screen dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.gui.screen.blit(overlay, (0, 0))

        # Die box — centred on the full screen
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2 - 30   # Slightly above centre for the label below

        box_x = cx - _DIE_SIZE // 2
        box_y = cy - _DIE_SIZE // 2

        # Title above the die
        self.gui.draw_text(title, cx, box_y - 50, COLOR_HIGHLIGHT, font=self.gui.title_font, center=True)

        # Die background and border
        pygame.draw.rect(self.gui.screen, (15, 15, 25), (box_x, box_y, _DIE_SIZE, _DIE_SIZE), border_radius=22)
        pygame.draw.rect(self.gui.screen, COLOR_BORDER, (box_x, box_y, _DIE_SIZE, _DIE_SIZE), 2, border_radius=22)

        # Dots
        self._draw_dots(face, box_x, box_y, dot_color)

        # Value label below the die
        label = str(face) if face else "?"
        self.gui.draw_text(label, cx, box_y + _DIE_SIZE + 18, COLOR_HIGHLIGHT, font=self.gui.title_font, center=True)

        # Prompt below the label
        self.gui.draw_text(prompt, cx, box_y + _DIE_SIZE + 55, COLOR_TEXT, center=True)

        self.gui.update_display()

    def _draw_dots(self, face: int, box_x: int, box_y: int, color: tuple) -> None:
        dots = _DOT_GRIDS.get(face, [])

        xs = [
            box_x + _DOT_PADDING,
            box_x + _DIE_SIZE // 2,
            box_x + _DIE_SIZE - _DOT_PADDING,
        ]
        ys = [
            box_y + _DOT_PADDING,
            box_y + _DIE_SIZE // 2,
            box_y + _DIE_SIZE - _DOT_PADDING,
        ]

        for col, row in dots:
            pygame.draw.circle(self.gui.screen, color, (xs[col], ys[row]), _DOT_RADIUS)
