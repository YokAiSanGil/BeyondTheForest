"""
Music module.
Handles music files in the assets folder and plays them based on game situation.
"""
import pygame
import time
import random
import os

def battle_music():
    """
    Playing battle music by randomly selecting a music file from the assets folder.
    """
    # Initialize pygame and mixer
    pygame.mixer.init()

    # Build absolute path to assets folder
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    assets_folder = os.path.join(script_dir, "assets")

    # Supported music file extensions
    music_extensions = ['.mid', '.midi', '.mp3', '.wav', '.ogg']
    music_files = []

    # Scan all files in the assets folder
    for filename in os.listdir(assets_folder):
        if any(filename.lower().endswith(ext) for ext in music_extensions):
            music_files.append(filename)

    if music_files:
        # Selecting a random music file
        selected_music = random.choice(music_files)
        music_path = os.path.join(assets_folder, selected_music)

        # Load and play music on loop
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # -1 to loop

def stop_music():
    """
    Stop the music.
    """
    pygame.mixer.music.stop()
