import logging
import os
import pygame

logger = logging.getLogger(__name__)


### --------------------------- Menu navigation --------------------------- ###


def handle_menu_navigation(event, current_selection, num_options):
    """
    Handle standard menu navigation (Up, Down, Enter).

    Args:
        event (pygame.event.Event): The event to process.
        current_selection (int): Currently selected option index.
        num_options (int): Total number of options in the menu.

    Returns:
        tuple: (new_selection, is_confirmed)
               - new_selection (int): The updated index.
               - is_confirmed (bool): True if the user pressed Enter.
    """
    new_selection = current_selection
    is_confirmed = False
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            new_selection = (current_selection - 1) % num_options
        elif event.key == pygame.K_DOWN:
            new_selection = (current_selection + 1) % num_options
        elif event.key == pygame.K_RETURN:
            is_confirmed = True
            
    return new_selection, is_confirmed


### --------------------------- Image management --------------------------- ###


def load_and_scale_image(path, max_width, max_height, keep_ratio=True):
    """
    Load an image and resize it to fit within the given dimensions.

    Args:
        path (str): Path to the image.
        max_width (int): Maximum width.
        max_height (int): Maximum height.
        keep_ratio (bool): If True, preserve aspect ratio (fit).
                           If False, stretch the image to fill.

    Returns:
        pygame.Surface or None: The resized image or None on error.
    """
    try:
        if not os.path.exists(path):
            return None
            
        img = pygame.image.load(path).convert_alpha()
        
        if keep_ratio:
            # Calcul du ratio pour "fit"
            width_ratio = max_width / img.get_width()
            height_ratio = max_height / img.get_height()
            scale = min(width_ratio, height_ratio)
            new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
        else:
            # Force les dimensions exactes "fill"
            new_size = (max_width, max_height)
            
        img = pygame.transform.scale(img, new_size)
        
        return img
    except Exception as e:
        logger.error(f"Error loading image {path}: {e}")
        return None
    

### --------------------------- Typewriter effects --------------------------- ###


def typewriter_effect(gui_manager, messages_list, new_message, draw_callback, speed=30, skippable=True):
    """
    Add a message to a list letter by letter while calling draw_callback.

    Args:
        gui_manager: GuiManager instance (for events).
        messages_list (list): The list to append the message to.
        new_message (str): The message to type out.
        draw_callback (func): Function to call to redraw the screen.
        speed (int): Time in ms between each letter.
        skippable (bool): If True, Space/Enter completes the text instantly.
    """
    # Add placeholder
    messages_list.append("")
    full_text = new_message
    current_text = ""

    # Clear previous events
    pygame.event.clear()
    
    skip = False
    for char in full_text:
        if skip:
            current_text += char
            continue
            
        current_text += char
        messages_list[-1] = current_text
        
        # Redessiner
        draw_callback()
        
        # Gestion du skip
        if skippable:
            for event in gui_manager.get_events():
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    skip = True
        else:
            pygame.event.pump()
            
        if not skip:
            pygame.time.wait(speed)
            
    # Finalise
    messages_list[-1] = full_text
    # Limit history size (optional, but good practice)
    if len(messages_list) > 10:
        messages_list.pop(0)


### --------------------------- Wait for user input --------------------------- ###


def wait_for_enter(gui_manager):
    """Block execution until Enter is pressed."""
    pygame.event.clear()
    waiting = True
    while waiting and gui_manager.running:
        for event in gui_manager.get_events():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
        pygame.time.wait(10)
