import pygame
import threading
import time
import os
from affichage_gui.gui_manager import (
    GuiManager, COLOR_TEXT, COLOR_HIGHLIGHT, COLOR_BORDER,
    PANEL_STATS_X, PANEL_STATS_Y, PANEL_STATS_W, PANEL_STATS_H,
    PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H,
    PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W, PANEL_DIALOG_H
)
from personnages.Hermit_NPC.Hermit_Brain import load_hermit, ask_hermit

class PhaseNPCGUI:
    def __init__(self):
        self.gui = GuiManager()
        self.font = pygame.font.Font(None, 24)
        self.chat_history = []  # List of (speaker, text)
        self.user_input = ""
        self.state = "LOADING"  # LOADING, IDLE, INPUT, GENERATING
        self.menu_options = ["Talk", "Leave"]
        self.selected_option = 0
        self.loading_text = "From the mist something or someone seems to appear slowly into the forest, like a dream or an illusion springing to life."
        
        # Placeholder for NPC Image
        self.npc_rect = pygame.Rect(PANEL_STATS_X + 20, PANEL_STATS_Y + 20, PANEL_STATS_W - 40, (PANEL_STATS_W - 40) * 16 // 9)
        self.npc_color = (50, 50, 50) # Dark grey placeholder
        self.npc_image = None
        self._load_npc_image()
        
        # Fade in effect
        self.fade_alpha = 0
        
        # Threading flags
        self.model_loaded = False
        self.generation_thread = None
        
        # Scroll
        self.scroll_y = 0
        
        # Cursor for input
        self.cursor_visible = True
        self.last_cursor_toggle = time.time()

    def _load_npc_image(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(base_dir, "assets", "TheHermit", "hermit.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                # Scale to fit npc_rect, keeping aspect ratio or crop? Let's scale to fill
                self.npc_image = pygame.transform.scale(img, (self.npc_rect.width, self.npc_rect.height))
            else:
                print(f"NPC Image not found at {path}")
        except Exception as e:
            print(f"Error loading NPC image: {e}")

    def start(self):
        """Called when entering the phase"""
        self.state = "LOADING"
        self.chat_history = []
        self.user_input = ""
        self.fade_alpha = 0
        # Start loading in a separate thread
        thread = threading.Thread(target=self._load_model_task)
        thread.daemon = True
        thread.start()

    def _load_model_task(self):
        success = load_hermit()
        if success:
            self.model_loaded = True
            self.state = "IDLE"
        else:
            self.state = "IDLE" # Allow user to leave even if error
            self.chat_history.append(("System", "Error: AI Model not found or failed to load."))
            self.chat_history.append(("System", "Please check 'models/' folder."))
        # Initial greeting from Hermit? Or just silence?
        # self.chat_history.append(("Hermit", "Greetings, mortal..."))

    def _generate_response_task(self, text):
        response = ask_hermit(text)
        self.chat_history.append(("Hermit", response))
        self.state = "IDLE"

    def handle_events(self, events):
        if self.state == "LOADING" or self.state == "GENERATING":
            return None

        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.state == "IDLE":
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.menu_options[self.selected_option] == "Talk":
                            self.state = "INPUT"
                            self.user_input = ""
                            pygame.key.start_text_input()
                        elif self.menu_options[self.selected_option] == "Leave":
                            return "exploration"
                            
                elif self.state == "INPUT":
                    if event.key == pygame.K_RETURN:
                        if self.user_input.strip():
                            self.chat_history.append(("Player", self.user_input))
                            self.state = "GENERATING"
                            pygame.key.stop_text_input()
                            
                            # Start generation thread
                            thread = threading.Thread(target=self._generate_response_task, args=(self.user_input,))
                            thread.daemon = True
                            thread.start()
                            
                            self.user_input = ""
                        else:
                            # Empty input, just go back
                            self.state = "IDLE"
                            pygame.key.stop_text_input()
                            
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "IDLE"
                        self.user_input = ""
                        pygame.key.stop_text_input()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        # Handled by TEXTINPUT usually, but for simple keys:
                        # self.user_input += event.unicode
                        pass
            
            elif event.type == pygame.TEXTINPUT and self.state == "INPUT":
                self.user_input += event.text

        return None

    def update(self):
        # Fade in
        if self.fade_alpha < 255:
            self.fade_alpha = min(255, self.fade_alpha + 5)

        # Cursor blink
        if time.time() - self.last_cursor_toggle > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = time.time()

    def draw(self, screen):
        self.gui.clear_screen()
        
        # 1. Left Panel (NPC Art)
        pygame.draw.rect(screen, COLOR_BORDER, (PANEL_STATS_X, PANEL_STATS_Y, PANEL_STATS_W, PANEL_STATS_H), 1)
        
        # Draw NPC Image with fade
        if self.npc_image:
            # Create a copy for alpha if needed, or just blit with special flags?
            # Pygame surfaces with per-pixel alpha (png) don't support set_alpha easily unless we blit to a temp surface
            # Or we can just use set_alpha if it doesn't have per-pixel alpha.
            # Assuming convert_alpha() was used.
            
            # To fade in a per-pixel alpha image, we need a helper or a temp surface
            temp_surf = self.npc_image.copy()
            temp_surf.fill((255, 255, 255, self.fade_alpha), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(temp_surf, self.npc_rect)
        else:
            # Draw placeholder
            pygame.draw.rect(screen, self.npc_color, self.npc_rect)
            
        pygame.draw.rect(screen, COLOR_BORDER, self.npc_rect, 1)
        
        # Label
        label = self.font.render("The Hermit", True, COLOR_HIGHLIGHT)
        screen.blit(label, (PANEL_STATS_X + (PANEL_STATS_W - label.get_width()) // 2, self.npc_rect.bottom + 20))

        # 2. Top Right Panel (Chat)
        pygame.draw.rect(screen, COLOR_BORDER, (PANEL_VIEW_X, PANEL_VIEW_Y, PANEL_VIEW_W, PANEL_VIEW_H), 1)
        
        if self.state == "LOADING":
            self._draw_text_wrapped(screen, self.loading_text, PANEL_VIEW_X + 20, PANEL_VIEW_Y + 20, PANEL_VIEW_W - 40, COLOR_TEXT)
            loading_lbl = self.font.render("Loading Brain...", True, COLOR_HIGHLIGHT)
            screen.blit(loading_lbl, (PANEL_VIEW_X + 20, PANEL_VIEW_Y + 100))
        else:
            self._draw_chat(screen)

        # 3. Bottom Right Panel (Menu/Input)
        pygame.draw.rect(screen, COLOR_BORDER, (PANEL_DIALOG_X, PANEL_DIALOG_Y, PANEL_DIALOG_W, PANEL_DIALOG_H), 1)
        
        if self.state == "INPUT":
            self._draw_input_box(screen)
        elif self.state == "GENERATING":
            lbl = self.font.render("The Hermit is thinking...", True, COLOR_HIGHLIGHT)
            screen.blit(lbl, (PANEL_DIALOG_X + 20, PANEL_DIALOG_Y + 20))
        elif self.state == "IDLE":
            self._draw_menu(screen)

    def _draw_menu(self, screen):
        y = PANEL_DIALOG_Y + 30
        for i, option in enumerate(self.menu_options):
            color = COLOR_HIGHLIGHT if i == self.selected_option else COLOR_TEXT
            text = f"> {option}" if i == self.selected_option else option
            surf = self.font.render(text, True, color)
            screen.blit(surf, (PANEL_DIALOG_X + 40, y))
            y += 30

    def _draw_input_box(self, screen):
        lbl = self.font.render("You say:", True, COLOR_HIGHLIGHT)
        screen.blit(lbl, (PANEL_DIALOG_X + 20, PANEL_DIALOG_Y + 20))
        
        # Input text
        txt_surf = self.font.render(self.user_input + ("_" if self.cursor_visible else ""), True, COLOR_TEXT)
        screen.blit(txt_surf, (PANEL_DIALOG_X + 20, PANEL_DIALOG_Y + 50))
        
        help_surf = self.font.render("[Enter] Send  [Esc] Cancel", True, (150, 150, 150))
        screen.blit(help_surf, (PANEL_DIALOG_X + 20, PANEL_DIALOG_Y + PANEL_DIALOG_H - 30))

    def _draw_chat(self, screen):
        # Simple chat rendering
        # We start from bottom and go up? Or top down with scroll?
        # Let's do bottom-up for latest messages
        
        x_left = PANEL_VIEW_X + 20
        x_right = PANEL_VIEW_X + PANEL_VIEW_W - 20
        y_bottom = PANEL_VIEW_Y + PANEL_VIEW_H - 20
        
        current_y = y_bottom
        
        # Iterate backwards
        for speaker, text in reversed(self.chat_history):
            is_player = (speaker == "Player")
            color = (100, 200, 255) if is_player else (200, 100, 100)
            align_right = is_player
            
            # Wrap text
            max_w = PANEL_VIEW_W * 0.6
            lines = self._wrap_text(text, self.font, max_w)
            
            # Calculate height of this block
            block_h = len(lines) * 25 + 10
            
            if current_y - block_h < PANEL_VIEW_Y:
                break # Stop if out of view (simple clipping)
                
            # Draw lines
            text_y = current_y - block_h
            for line in lines:
                surf = self.font.render(line, True, color)
                if align_right:
                    screen.blit(surf, (x_right - surf.get_width(), text_y))
                else:
                    screen.blit(surf, (x_left, text_y))
                text_y += 25
            
            current_y -= (block_h + 10)

    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            w, h = font.size(test_line)
            if w <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        return lines

    def _draw_text_wrapped(self, screen, text, x, y, max_width, color):
        lines = self._wrap_text(text, self.font, max_width)
        for line in lines:
            surf = self.font.render(line, True, color)
            screen.blit(surf, (x, y))
            y += 25
