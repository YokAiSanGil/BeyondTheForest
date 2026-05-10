import os
import json
import uuid
import glob
import logging
from characters.hero import Hero

logger = logging.getLogger(__name__)

# Use absolute path based on script location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVES_ROOT = os.path.join(BASE_DIR, 'saves')
SAVES_DIR = os.path.join(SAVES_ROOT, 'all_saves')
LEGACY_SAVE_PATH = os.path.join(SAVES_ROOT, 'sauvegarde.json')

def migrate_old_saves() -> None:
    """
    Migrate saves from old format (sauvegarde.json) to new format (individual files).
    """
    if not os.path.exists(LEGACY_SAVE_PATH):
        return

    logger.info("Migrating saves...")
    with open(LEGACY_SAVE_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return

    for entry in data:
        if 'hero' in entry:
            h_data = entry['hero']
            # Ensure an ID exists
            if not h_data.get('id'):
                h_data['id'] = str(uuid.uuid4())

            hero_id = h_data['id']
            # Support both old 'nom' key and new 'name' key
            hero_name = h_data.get('name', h_data.get('nom', 'Unknown'))

            # Build the full save structure
            new_save_data = {
                'hero': h_data,
                'monsters_defeated': entry.get('monstres_vaincus', entry.get('monsters_defeated', 0)),
                'npc_memories': {},
                'world_state': {}
            }

            # Sanitize name to avoid invalid filename characters
            safe_name = "".join([c for c in hero_name if c.isalnum() or c in (' ', '-', '_')]).strip()
            filename = f"save_{safe_name}_{hero_id}.json"
            filepath = os.path.join(SAVES_DIR, filename)

            with open(filepath, 'w', encoding='utf-8') as f_out:
                json.dump(new_save_data, f_out, indent=4, ensure_ascii=False)

    # Rename old file to avoid re-migrating
    os.rename(LEGACY_SAVE_PATH, LEGACY_SAVE_PATH + ".migrated")
    logger.info("Migration complete.")

def list_saves() -> list[dict]:
    """
    Return a list of saves as dicts {'name': str, 'id': str}.
    """
    # Check for migration
    if os.path.exists(LEGACY_SAVE_PATH):
        migrate_old_saves()

    if not os.path.exists(SAVES_DIR):
        return []

    files = glob.glob(os.path.join(SAVES_DIR, "save_*.json"))
    result = []

    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'hero' in data:
                    # Support both old 'nom' key and new 'name' key
                    hero_name = data['hero'].get('name', data['hero'].get('nom', 'Unknown'))
                    result.append({
                        'name': hero_name,
                        'id': data['hero']['id']
                    })
        except (json.JSONDecodeError, KeyError):
            continue

    return result

def save_game(hero: Hero, monsters_defeated: int, npc_memories: dict = None, world_state: dict = None) -> None:
    """
    Save the hero's game to an individual JSON file.
    """
    if npc_memories is None:
        npc_memories = {}
    if world_state is None:
        world_state = {}

    os.makedirs(SAVES_DIR, exist_ok=True)

    # Ensure hero has an ID
    if hero.id is None:
        hero.id = str(uuid.uuid4())

    # Prepare hero data
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'race': hero.race,
        'hp': hero.hp,
        'max_hp': hero.max_hp,
        'gold': hero.gold,
        'leather': hero.leather,
        'morts': getattr(hero, 'morts', 0)
    }

    save_data = {
        'hero': hero_data,
        'monsters_defeated': monsters_defeated,
        'npc_memories': npc_memories,
        'world_state': world_state
    }

    safe_name = "".join([c for c in hero.name if c.isalnum() or c in (' ', '-', '_')]).strip()
    filename = f"save_{safe_name}_{hero.id}.json"
    filepath = os.path.join(SAVES_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=4, ensure_ascii=False)

def load_game(identifier: str) -> tuple[Hero | None, int, dict, dict]:
    """
    Load a hero's game by ID.
    Returns (Hero, monsters_defeated, npc_memories, world_state).
    """
    # Check for migration
    if os.path.exists(LEGACY_SAVE_PATH):
        migrate_old_saves()

    files = glob.glob(os.path.join(SAVES_DIR, "save_*.json"))

    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if 'hero' in data and data['hero'].get('id') == identifier:
                hd = data['hero']
                # Support both old and new key names
                hero_name = hd.get('name', hd.get('nom', 'Unknown'))
                hero = Hero(name=hero_name, race=hd['race'])
                hero.id = hd.get('id')
                hero.max_hp = hd.get('max_hp', hd.get('points_de_vie_max', hero.max_hp))
                hero.hp = hd.get('hp', hd.get('points_de_vie', hero.hp))
                hero.gold = hd['gold']
                hero.leather = hd.get('leather', hd.get('cuir', 0))
                hero.morts = hd.get('morts', 0)

                monsters_defeated = data.get('monsters_defeated', data.get('monstres_vaincus', 0))
                npc_memories = data.get('npc_memories', {})
                world_state = data.get('world_state', {})

                return hero, monsters_defeated, npc_memories, world_state

        except (json.JSONDecodeError, KeyError):
            continue

    return None, 0, {}, {}

def delete_save(hero_id: str) -> None:
    """
    Delete the save file matching the given hero ID.
    """
    files = glob.glob(os.path.join(SAVES_DIR, "save_*.json"))

    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if 'hero' in data and data['hero'].get('id') == hero_id:
                os.remove(filepath)
                return
        except:
            continue
