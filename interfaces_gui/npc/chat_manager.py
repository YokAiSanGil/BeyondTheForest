import pygame

class ChatManager:
    def __init__(self, font):
        self.font = font
        self.history = []  # List of [speaker, text]
        self.scroll_y = 0
        self.scroll_to_bottom = False
        
        # Typewriter effect state
        self.pending_response = None
        self.target_message = ""
        self.typing_index = 0
        self.last_type_time = 0
        self.is_typing = False

    def add_message(self, speaker, text):
        self.history.append([speaker, text])
        self.scroll_to_bottom = True

    def start_typing(self, response):
        self.pending_response = None
        self.target_message = response
        self.add_message("Hermit", "")
        self.is_typing = True
        self.typing_index = 0
        self.last_type_time = pygame.time.get_ticks()
        self.scroll_to_bottom = True

    def update_typing(self):
        if not self.is_typing:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_type_time > 20:  # Speed (ms per char)
            self.last_type_time = current_time
            if self.typing_index < len(self.target_message):
                char = self.target_message[self.typing_index]
                self.history[-1][1] += char
                self.typing_index += 1
                self.scroll_to_bottom = True
            else:
                self.is_typing = False
                self.scroll_to_bottom = True

    def handle_scroll(self, dy, max_scroll):
        self.scroll_y -= dy
        self.clamp_scroll(max_scroll)

    def clamp_scroll(self, max_scroll):
        if self.scroll_y > max_scroll:
            self.scroll_y = max_scroll
        if self.scroll_y < 0:
            self.scroll_y = 0

    def wrap_text(self, text, max_width):
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
        return lines
