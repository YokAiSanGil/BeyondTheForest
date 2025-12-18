import pygame
import threading
import time
from personnages.Hermit_NPC.Hermit_Brain import load_hermit, ask_hermit
from interfaces_gui.npc.chat_manager import ChatManager
from interfaces_gui.npc.npc_renderer import NPCRenderer
from interfaces_gui.utils import handle_menu_navigation

class PhaseNPCGUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        
        # Managers
        self.chat_manager = ChatManager(self.font)
        self.renderer = NPCRenderer(self.font)
        
        self.user_input = ""
        self.state = "LOADING"  # LOADING, IDLE, INPUT, GENERATING, TYPING
        self.menu_options = ["Talk", "Leave"]
        self.selected_option = 0
        self.loading_text = "From the mist something or someone seems to appear slowly into the forest, like a dream or an illusion springing to life."
        
        # Threading flags
        self.model_loaded = False
        self.pending_response = None
        
        # Cursor for input
        self.cursor_visible = True
        self.last_cursor_toggle = time.time()

    def start(self, npc_memories=None, world_state=None):
        """Called when entering the phase"""
        self.npc_memories = npc_memories if npc_memories is not None else {}
        self.world_state = world_state if world_state is not None else {}
        self.state = "LOADING"
        self.chat_manager.history = []
        self.user_input = ""
        self.renderer.reset_fade()
        
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
            self.chat_manager.add_message("System", "Error: AI Model not found or failed to load.")
            self.chat_manager.add_message("System", "Please check 'models/' folder.")

    def _generate_response_task(self, text):
        response = ask_hermit(text)
        self.pending_response = response
        # State remains GENERATING until update picks it up

    def handle_events(self, events):
        if self.state == "LOADING" or self.state == "GENERATING":
            return None

        for event in events:
            if self.state == "IDLE":
                # Navigation standard
                self.selected_option, confirmed = handle_menu_navigation(event, self.selected_option, len(self.menu_options))
                
                if confirmed:
                    if self.menu_options[self.selected_option] == "Talk":
                        self.state = "INPUT"
                        self.user_input = ""
                        pygame.key.start_text_input()
                    elif self.menu_options[self.selected_option] == "Leave":
                        return "exploration"
                
                # Scroll controls (spécifique NPC)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PAGEUP:
                        self.chat_manager.handle_scroll(20, 1000)
                    elif event.key == pygame.K_PAGEDOWN:
                        self.chat_manager.handle_scroll(-20, 1000)
                            
            elif self.state == "INPUT":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.user_input.strip():
                            self.chat_manager.add_message("Player", self.user_input)
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
            
            elif event.type == pygame.TEXTINPUT and self.state == "INPUT":
                self.user_input += event.text
            
            # Mouse wheel scrolling
            elif event.type == pygame.MOUSEWHEEL:
                self.chat_manager.handle_scroll(event.y * 20, 10000) # Max scroll handled in draw/clamp

        return None

    def update(self):
        # Fade in
        self.renderer.update_fade()

        # Cursor blink
        if time.time() - self.last_cursor_toggle > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = time.time()
            
        # Check for pending response from thread
        if self.pending_response:
            self.chat_manager.start_typing(self.pending_response)
            self.pending_response = None
            self.state = "TYPING"
            
        # Handle Typing
        if self.state == "TYPING":
            self.chat_manager.update_typing()
            if not self.chat_manager.is_typing:
                self.state = "IDLE"

    def draw(self, screen):
        self.renderer.draw_main_layout(
            screen, 
            self.state, 
            self.chat_manager, 
            self.loading_text, 
            self.menu_options, 
            self.selected_option, 
            self.user_input
        )
