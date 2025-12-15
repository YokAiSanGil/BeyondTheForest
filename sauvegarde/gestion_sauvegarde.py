import os
import json
import uuid
from personnages.hero import Hero

# Utilisation d'un chemin absolu basé sur l'emplacement du script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAUVEGARDE_PATH = os.path.join(BASE_DIR, 'sauvegarde', 'sauvegarde.json')


def lister_sauvegardes() -> list:
    """
    Retourne la liste des sauvegardes sous forme de dictionnaires {'nom': str, 'id': str}.
    """
    if not os.path.exists(SAUVEGARDE_PATH):
        return []
    with open(SAUVEGARDE_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    
    result = []
    for entry in data:
        if 'hero' in entry:
            h_data = entry['hero']
            # Compatibilité : si pas d'ID, on en génère un temporaire pour l'affichage, 
            # mais idéalement il faudrait le sauvegarder. Pour l'instant on lit ce qui existe.
            h_id = h_data.get('id')
            result.append({'nom': h_data['nom'], 'id': h_id})
    return result

def sauvegarder_partie(hero: Hero, monstres_vaincus: int):
    """
    Sauvegarde ou met à jour la partie du héros dans un fichier JSON.
    Utilise l'ID du héros pour l'unicité.
    """
    os.makedirs(os.path.dirname(SAUVEGARDE_PATH), exist_ok=True)
    saves = []
    if os.path.exists(SAUVEGARDE_PATH):
        with open(SAUVEGARDE_PATH, 'r', encoding='utf-8') as f:
            try:
                saves = json.load(f)
            except json.JSONDecodeError:
                saves = []
    
    # Assurer que le héros a un ID
    if hero.id is None:
        hero.id = str(uuid.uuid4())

    # Préparer les données du héros
    hero_data = {
        'id': hero.id,
        'nom': hero.nom,
        'race': hero.race,
        'points_de_vie': hero.points_de_vie,
        'points_de_vie_max': hero.points_de_vie_max,
        'gold': hero.gold,
        'cuir': hero.cuir,
        'morts': getattr(hero, 'morts', 0)
    }

    entry = {
        'hero': hero_data,
        'monstres_vaincus': monstres_vaincus
    }

    # Chercher si une sauvegarde existe déjà pour cet ID
    found_index = -1
    for i, save in enumerate(saves):
        if 'hero' in save:
            # Vérification par ID (prioritaire)
            if save['hero'].get('id') == hero.id:
                found_index = i
                break
            # Vérification par nom (pour rétrocompatibilité ou si ID manquant dans save)
            elif save['hero'].get('id') is None and save['hero'].get('nom') == hero.nom:
                found_index = i
                break
    
    if found_index != -1:
        saves[found_index] = entry
    else:
        saves.append(entry)

    with open(SAUVEGARDE_PATH, 'w', encoding='utf-8') as f:
        json.dump(saves, f, indent=4, ensure_ascii=False)

def charger_sauvegardes():
    """
    Charge toutes les sauvegardes brutes.
    """
    if not os.path.exists(SAUVEGARDE_PATH):
        return []
    with open(SAUVEGARDE_PATH, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def charger_partie(identifiant: str) -> tuple:
    """
    Charge la partie d'un héros par son ID (ou nom pour rétrocompatibilité).
    Retourne (Hero, monstres_vaincus) ou (None, 0).
    """
    saves = charger_sauvegardes()
    for entry in saves:
        hd = entry.get('hero', {})
        # On cherche par ID si présent, sinon par nom
        if hd.get('id') == identifiant or (hd.get('id') is None and hd.get('nom') == identifiant):
            # Créer le héros
            hero = Hero(nom=hd['nom'], race=hd['race'])
            hero.id = hd.get('id') # Récupérer l'ID sauvegardé
            hero.points_de_vie_max = hd['points_de_vie_max']
            hero.points_de_vie = hd['points_de_vie']
            hero.gold = hd['gold']
            hero.cuir = hd['cuir']
            hero.morts = hd.get('morts', 0)
            
            # Si on a chargé par nom et qu'il n'y avait pas d'ID, on peut en générer un maintenant
            # ou attendre la prochaine sauvegarde.
            if hero.id is None:
                 hero.id = str(uuid.uuid4())

            return hero, entry.get('monstres_vaincus', 0)
    return None, 0

def supprimer_sauvegarde(hero_id: str):
    """
    Supprime la sauvegarde correspondant à l'ID du héros.
    """
    if not os.path.exists(SAUVEGARDE_PATH):
        return

    saves = charger_sauvegardes()
    new_saves = []
    found = False
    
    for save in saves:
        if 'hero' in save and save['hero'].get('id') == hero_id:
            found = True
            continue # On saute cette sauvegarde
        new_saves.append(save)
    
    if found:
        with open(SAUVEGARDE_PATH, 'w', encoding='utf-8') as f:
            json.dump(new_saves, f, indent=4, ensure_ascii=False)


