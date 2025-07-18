import os
import json
from personnages.hero import Hero

SAUVEGARDE_PATH = os.path.join(os.getcwd(), 'sauvegarde', 'sauvegarde.json')


def sauvegarder_partie(hero: Hero, monstres_vaincus: int):
    """
    Sauvegarde l'état de la partie dans un fichier JSON.
    """
    donnees = {
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
    os.makedirs(os.path.dirname(SAUVEGARDE_PATH), exist_ok=True)
    with open(SAUVEGARDE_PATH, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)


def charger_partie():
    """
    Charge l'état de la partie depuis le fichier JSON.
    Retourne un tuple (Hero, monstres_vaincus) ou (None,0) si aucune sauvegarde.
    """
    if not os.path.exists(SAUVEGARDE_PATH):
        return None, 0

    with open(SAUVEGARDE_PATH, 'r', encoding='utf-8') as f:
        donnees = json.load(f)

    hero_data = donnees.get('hero')
    if not hero_data:
        return None, 0

    # Crée le héros avec nom et race, puis restaure les autres attributs
    hero = Hero(
        nom=hero_data['nom'],
        race=hero_data['race']
    )
    # Restaurer les points de vie
    hero.points_de_vie_max = hero_data['points_de_vie_max']
    hero.points_de_vie = hero_data['points_de_vie']
    # Restaurer or, cuir et morts
    hero.gold = hero_data['gold']
    hero.cuir = hero_data['cuir']
    hero.morts = hero_data.get('morts', 0)

    monstres_vaincus = donnees.get('monstres_vaincus', 0)
    return hero, monstres_vaincus
