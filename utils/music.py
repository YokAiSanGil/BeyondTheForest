"""
Module music
Ce module appele les fichiers music dans le dossier assets
et fait de fonction selon la situation du jeu.
"""
import pygame
import time
import random
import os

def battle_music():
    """
    Joue la musique de combat en sélectionnant aléatoirement 
    un fichier musical du dossier assets.
    """
    # Initialiser pygame et le mixer
    pygame.mixer.init()
    
    # Construire un chemin absolu vers le dossier assets
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    assets_folder = os.path.join(script_dir, "assets")
    
    # Extensions de fichiers musicaux supportées
    extensions_musicales = ['.mid', '.midi', '.mp3', '.wav', '.ogg']
    music_files = []
    
    # Parcourir tous les fichiers du dossier assets
    for fichier in os.listdir(assets_folder):
        if any(fichier.lower().endswith(ext) for ext in extensions_musicales):
            music_files.append(fichier)
    
    if music_files:
        # Sélectionner un fichier musical au hasard
        selected_music = random.choice(music_files)
        music_path = os.path.join(assets_folder, selected_music)
        
        # Charger et jouer la musique en boucle
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

def stop_music():
    """
    Arrête la musique.
    """
    pygame.mixer.music.stop()

# Tester la fonction seulement si le script est exécuté directement
# if __name__ == "__main__":
#     print("Démarrage de la musique de combat...")
#     battle_music()
    
#     # Maintenir le programme en vie pour entendre la musique
# try:
#     print("Musique en cours... Appuyez sur Ctrl+C pour arrêter.")
#     while pygame.mixer.music.get_busy():
#            time.sleep(1)
# except KeyboardInterrupt:
#         print("\nArrêt de la musique...")
#         stop_music()
#         pygame.quit()
