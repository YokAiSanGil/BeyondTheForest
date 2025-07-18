import os
import json
from personnages.hero import Hero

SAUVEGARDE_PATH = os.path.join(os.getcwd(), 'sauvegarde', 'sauvegarde.json')


def lister_sauvegardes() -> list:
    """
    Retourne la liste des noms de héros sauvegardés.
    """
    if not os.path.exists(SAUVEGARDE_PATH):
        return []
    with open(SAUVEGARDE_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    # Attendu: liste de dicts
    return [entry['hero']['nom'] for entry in data if 'hero' in entry]

def sauvegarder_partie(hero: Hero, monstres_vaincus: int):
    """
    Sauvegarde ou met à jour la partie du héros dans un fichier JSON (liste de slots).
    """
    os.makedirs(os.path.dirname(SAUVEGARDE_PATH), exist_ok=True)
    saves = []
    if os.path.exists(SAUVEGARDE_PATH):
        with open(SAUVEGARDE_PATH, 'r', encoding='utf-8') as f:
            try:
                saves = json.load(f)
            except json.JSONDecodeError:
                saves = []
    # Préparer l'entrée
    entry = {
        'hero': {
            'nom': hero.nom,
            'race': hero.race,
            'points_de_vie': hero.points_de_vie,
            'points_de_vie_max': hero.points_de_vie_max,
            'gold': hero.gold,
            'cuir': hero.cuir,
            'morts': getattr(hero, 'morts', 0)
        },
        'monstres_vaincus': monstres_vaincus
    }
    # Mettre à jour si existant
    noms = [s['hero']['nom'] for s in saves]
    if hero.nom in noms:
        idx = noms.index(hero.nom)
        saves[idx] = entry
    else:
        saves.append(entry)
    with open(SAUVEGARDE_PATH, 'w', encoding='utf-8') as f:
        json.dump(saves, f, indent=4, ensure_ascii=False)

def charger_sauvegardes():
    """
    Charge toutes les sauvegardes, retourne liste d'entrées.
    """
    if not os.path.exists(SAUVEGARDE_PATH):
        return []
    with open(SAUVEGARDE_PATH, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def charger_partie(nom: str) -> tuple:
    """
    Charge la partie d'un héros par nom.
    Retourne (Hero, monstres_vaincus) ou (None,0).
    """
    saves = charger_sauvegardes()
    for entry in saves:
        hd = entry.get('hero', {})
        if hd.get('nom') == nom:
            # Créer le héros
            hero = Hero(nom=hd['nom'], race=hd['race'])
            hero.points_de_vie_max = hd['points_de_vie_max']
            hero.points_de_vie = hd['points_de_vie']
            hero.gold = hd['gold']
            hero.cuir = hd['cuir']
            hero.morts = hd.get('morts', 0)
            return hero, entry.get('monstres_vaincus', 0)
    return None, 0


