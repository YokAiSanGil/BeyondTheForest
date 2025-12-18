import pygame
import os


### --------------------------- Gestion des menus --------------------------- ###


def handle_menu_navigation(event, current_selection, num_options):
    """
    Gère la navigation standard dans un menu (Haut, Bas, Entrée).
    
    Args:
        event (pygame.event.Event): L'événement à traiter.
        current_selection (int): L'index de l'option actuellement sélectionnée.
        num_options (int): Le nombre total d'options dans le menu.
        
    Returns:
        tuple: (nouvelle_selection, est_valide)
               - nouvelle_selection (int): L'index mis à jour.
               - est_valide (bool): True si l'utilisateur a appuyé sur Entrée.
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


### --------------------------- Gestion des images --------------------------- ###


def load_and_scale_image(path, max_width, max_height):
    """
    Charge une image et la redimensionne pour tenir dans les dimensions données
    tout en conservant le ratio d'aspect.
    
    Args:
        path (str): Chemin vers l'image.
        max_width (int): Largeur maximale.
        max_height (int): Hauteur maximale.
        
    Returns:
        pygame.Surface or None: L'image redimensionnée ou None si erreur.
    """
    try:
        if not os.path.exists(path):
            return None
            
        img = pygame.image.load(path).convert_alpha()
        
        # Calcul du ratio
        width_ratio = max_width / img.get_width()
        height_ratio = max_height / img.get_height()
        scale = min(width_ratio, height_ratio)
        
        # Si l'image est plus petite que la cible, on peut choisir de l'agrandir ou non.
        # Ici, on redimensionne seulement si nécessaire ou pour adapter au cadre.
        # Pour le pixel art, on préfère souvent des entiers, mais ici on fait simple.
        
        new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
        img = pygame.transform.scale(img, new_size)
        
        return img
    except Exception as e:
        print(f"Erreur chargement image {path}: {e}")
        return None
    

### --------------------------- Effets de machine à écrire --------------------------- ###


def typewriter_effect(gui_manager, messages_list, new_message, draw_callback, speed=30, skippable=True):
    """
    Ajoute un message à une liste lettre par lettre en appelant draw_callback.
    
    Args:
        gui_manager: Instance du GuiManager (pour les events).
        messages_list (list): La liste où ajouter le message.
        new_message (str): Le message à écrire.
        draw_callback (func): Fonction à appeler pour redessiner l'écran.
        speed (int): Temps en ms entre chaque lettre.
        skippable (bool): Si True, Espace/Entrée complète le texte instantanément.
    """
    # Ajouter placeholder
    messages_list.append("")
    full_text = new_message
    current_text = ""
    
    # Nettoyer les événements précédents
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
            
    # Finaliser
    messages_list[-1] = full_text
    # Limiter la taille de l'historique (optionnel, mais bonne pratique)
    if len(messages_list) > 10:
        messages_list.pop(0)


### --------------------------- Attente d'entrée utilisateur --------------------------- ###


def wait_for_enter(gui_manager):
    """Bloque l'exécution jusqu'à ce que Entrée soit pressé."""
    pygame.event.clear()
    waiting = True
    while waiting and gui_manager.running:
        for event in gui_manager.get_events():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
        pygame.time.wait(10)
