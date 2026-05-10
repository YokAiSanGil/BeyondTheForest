import pygame
import os
from display.gui_manager import (
    GuiManager, COLOR_TEXT, COLOR_HIGHLIGHT, COLOR_BORDER,
    PANEL_STATS_X, PANEL_STATS_Y, PANEL_STATS_W, PANEL_STATS_H,
    PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H
)
from interfaces_gui.utils import load_and_scale_image

class NPCRenderer:
    def __init__(self, font):
        self.gui = GuiManager()
        self.font = font
        self.npc_rect = pygame.Rect(PANEL_STATS_X + 20, PANEL_STATS_Y + 20, PANEL_STATS_W - 40, (PANEL_STATS_W - 40) * 16 // 9)
        self.npc_color = (50, 50, 50)
        self.npc_image = self._load_npc_image()
        self.fade_alpha = 0

    def _load_npc_image(self):
        # This file is in interfaces_gui/npc/
        # Go up 3 levels to get to root: npc -> interfaces_gui -> HeroesVsMonsters
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(base_dir, "assets", "TheHermit", "hermit.png")

        return load_and_scale_image(path, self.npc_rect.width, self.npc_rect.height)

    def update_fade(self):
        if self.fade_alpha < 255:
            self.fade_alpha = min(255, self.fade_alpha + 5)

    def reset_fade(self):
        self.fade_alpha = 0

    def draw_main_layout(self, screen, state, chat_manager, loading_text, menu_options, selected_option, user_input):
        self.gui.clear_screen()

        # 1. Left Panel (NPC Art)
        self.gui.draw_panel(PANEL_STATS_X, PANEL_STATS_Y, PANEL_STATS_W, PANEL_STATS_H, None)
        self._draw_npc(screen)

        # Label "THE HERMIT"
        label = self.font.render("THE HERMIT", True, COLOR_TEXT)
        screen.blit(label, (PANEL_STATS_X + (PANEL_STATS_W - label.get_width()) // 2, self.npc_rect.bottom + 20))

        # 2. Top Right Panel (Chat)
        self.gui.draw_viewport_panel("CHAT")

        # Clipping rect for chat
        chat_rect = pygame.Rect(PANEL_VIEW_X + 5, PANEL_VIEW_Y + 5, PANEL_VIEW_W - 10, PANEL_VIEW_H - 10)
        screen.set_clip(chat_rect)

        if state == "LOADING":
            self._draw_loading(screen, loading_text)
        else:
            self._draw_chat(screen, chat_manager)

        screen.set_clip(None)

        # 3. Bottom Right Panel (Unified Interface)
        is_input_mode = (state == "INPUT")
        self.gui.draw_bottom_interface(
            menu_options=menu_options,
            selected_index=selected_option,
            logs=None,
            input_mode=is_input_mode,
            input_text=user_input,
            input_prompt="You say:",
            panel_title="OPTIONS" if not is_input_mode else "DIALOGUE"
        )

    def _draw_npc(self, screen):
        if self.npc_image:
            if self.fade_alpha < 255:
                temp_surf = self.npc_image.copy()
                temp_surf.fill((255, 255, 255, self.fade_alpha), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(temp_surf, self.npc_rect)
            else:
                screen.blit(self.npc_image, self.npc_rect)
        else:
            pygame.draw.rect(screen, self.npc_color, self.npc_rect)

    def _draw_loading(self, screen, text):
        self._draw_text_wrapped(screen, text, PANEL_VIEW_X + 20, PANEL_VIEW_Y + 20, PANEL_VIEW_W - 40, COLOR_TEXT)
        loading_lbl = self.font.render("Loading...", True, COLOR_HIGHLIGHT)
        screen.blit(loading_lbl, (PANEL_VIEW_X + 20, PANEL_VIEW_Y + 100))

    def _draw_chat(self, screen, chat_manager):
        x_left = PANEL_VIEW_X + 20
        x_right = PANEL_VIEW_X + PANEL_VIEW_W - 20
        y_top = PANEL_VIEW_Y + 20

        # Calculate total height and blocks
        total_height = 0
        message_blocks = []

        for speaker, text in chat_manager.history:
            is_player = (speaker == "Player")
            color = (100, 200, 255) if is_player else (200, 100, 100)
            align_right = is_player

            max_w = PANEL_VIEW_W * 0.6
            lines = chat_manager.wrap_text(text, max_w)
            block_h = len(lines) * 25 + 10

            message_blocks.append((lines, color, align_right, block_h))
            total_height += block_h

        # Auto-scroll logic
        view_h = PANEL_VIEW_H - 40
        max_scroll = max(0, total_height - view_h)

        if chat_manager.scroll_to_bottom:
            chat_manager.scroll_y = max_scroll
            if not chat_manager.is_typing:
                chat_manager.scroll_to_bottom = False

        chat_manager.clamp_scroll(max_scroll)

        # Draw visible blocks
        current_y = y_top - chat_manager.scroll_y

        for lines, color, align_right, block_h in message_blocks:
            if current_y + block_h > PANEL_VIEW_Y and current_y < PANEL_VIEW_Y + PANEL_VIEW_H:
                text_y = current_y
                for line in lines:
                    surf = self.font.render(line, True, color)
                    if align_right:
                        screen.blit(surf, (x_right - surf.get_width(), text_y))
                    else:
                        screen.blit(surf, (x_left, text_y))
                    text_y += 25
            current_y += block_h

    def _draw_text_wrapped(self, screen, text, x, y, max_width, color):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            w, h = self.font.size(test_line)
            if w <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))

        for line in lines:
            surf = self.font.render(line, True, color)
            screen.blit(surf, (x, y))
            y += 25
