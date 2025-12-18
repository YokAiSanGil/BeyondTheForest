import os
import json
import uuid
import glob
from personnages.hero import Hero

# Utilisation d'un chemin absolu basé sur l'emplacement du script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAUVEGARDE_ROOT = os.path.join(BASE_DIR, 'sauvegarde')
SAUVEGARDE_DIR = os.path.join(SAUVEGARDE_ROOT, 'all_saves')
LEGACY_SAVE_PATH = os.path.join(SAUVEGARDE_ROOT, 'sauvegarde.json')

def migrer_anciennes_sauvegardes():
    """
    Migre les sauvegardes de l'ancien format (sauvegarde.json) vers le nouveau format (fichiers individuels).
    """
    if not os.path.exists(LEGACY_SAVE_PATH):
        return

    print("Migration des sauvegardes en cours...")
    with open(LEGACY_SAVE_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return

    for entry in data:
        if 'hero' in entry:
            h_data = entry['hero']
            # Assurer un ID
            if not h_data.get('id'):
                h_data['id'] = str(uuid.uuid4())
            
            hero_id = h_data['id']
            hero_nom = h_data['nom']
            
            # Créer la structure complète
            new_save_data = {
                'hero': h_data,
                'monstres_vaincus': entry.get('monstres_vaincus', 0),
                'npc_memories': {},
                'world_state': {}
            }
            
            # Sauvegarder dans le nouveau fichier
            # Nettoyer le nom pour éviter les caractères invalides dans le nom de fichier
            safe_nom = "".join([c for c in hero_nom if c.isalnum() or c in (' ', '-', '_')]).strip()
            filename = f"save_{safe_nom}_{hero_id}.json"
            filepath = os.path.join(SAUVEGARDE_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f_out:
                json.dump(new_save_data, f_out, indent=4, ensure_ascii=False)
                
    # Renommer l'ancien fichier pour éviter de le re-migrer
    os.rename(LEGACY_SAVE_PATH, LEGACY_SAVE_PATH + ".migrated")
    print("Migration terminée.")

def lister_sauvegardes() -> list:
    """
    Retourne la liste des sauvegardes sous forme de dictionnaires {'nom': str, 'id': str}.
    """
    # Vérifier migration
    if os.path.exists(LEGACY_SAVE_PATH):
        migrer_anciennes_sauvegardes()
        
    if not os.path.exists(SAUVEGARDE_DIR):
        return []
        
    files = glob.glob(os.path.join(SAUVEGARDE_DIR, "save_*.json"))
    result = []
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'hero' in data:
                    result.append({
                        'nom': data['hero']['nom'],
                        'id': data['hero']['id']
                    })
        except (json.JSONDecodeError, KeyError):
            continue
            
    return result

def sauvegarder_partie(hero: Hero, monstres_vaincus: int, npc_memories: dict = None, world_state: dict = None):
    """
    Sauvegarde la partie du héros dans un fichier JSON individuel.
    """
    if npc_memories is None:
        npc_memories = {}
    if world_state is None:
        world_state = {}
        
    os.makedirs(SAUVEGARDE_DIR, exist_ok=True)
    
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

    save_data = {
        'hero': hero_data,
        'monstres_vaincus': monstres_vaincus,
        'npc_memories': npc_memories,
        'world_state': world_state
    }

    safe_nom = "".join([c for c in hero.nom if c.isalnum() or c in (' ', '-', '_')]).strip()
    filename = f"save_{safe_nom}_{hero.id}.json"
    filepath = os.path.join(SAUVEGARDE_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=4, ensure_ascii=False)

def charger_partie(identifiant: str) -> tuple:
    """
    Charge la partie d'un héros par son ID.
    Retourne (Hero, monstres_vaincus, npc_memories, world_state).
    """
    # Vérifier migration
    if os.path.exists(LEGACY_SAVE_PATH):
        migrer_anciennes_sauvegardes()
        
    files = glob.glob(os.path.join(SAUVEGARDE_DIR, "save_*.json"))
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if 'hero' in data and data['hero'].get('id') == identifiant:
                hd = data['hero']
                hero = Hero(nom=hd['nom'], race=hd['race'])
                hero.id = hd.get('id')
                hero.points_de_vie_max = hd['points_de_vie_max']
                hero.points_de_vie = hd['points_de_vie']
                hero.gold = hd['gold']
                hero.cuir = hd['cuir']
                hero.morts = hd.get('morts', 0)
                
                monstres_vaincus = data.get('monstres_vaincus', 0)
                npc_memories = data.get('npc_memories', {})
                world_state = data.get('world_state', {})
                
                return hero, monstres_vaincus, npc_memories, world_state
                
        except (json.JSONDecodeError, KeyError):
            continue
            
    return None, 0, {}, {}

def supprimer_sauvegarde(hero_id: str):
    """
    Supprime la sauvegarde correspondant à l'ID du héros.
    """
    files = glob.glob(os.path.join(SAUVEGARDE_DIR, "save_*.json"))
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'hero' in data and data['hero'].get('id') == hero_id:
                os.remove(filepath)
                return
        except:
            continue


