"""
Actions module.
Contains combat action functions used in the game.
"""
from .character import Character
from .hero import Hero
from .monster import Monster
from utils.dice import Die
from characters.utils import modifier


def calculate_damage(attacker: Character):
    """Calculate damage for an attack."""
    # Special case for The True Hermit (One Hit Kill)
    if attacker.race == "The True Hermit":
        return 9999

    die4 = Die(1, 4)
    return die4.roll() + modifier(attacker.strength)

def attack(attacker: Character, target: Character):
    """
    Prepares an attack sequence and returns messages and damage.
    Does NOT apply damage directly.
    """
    messages = []
    if not attacker.is_alive():
        messages.append(f"{attacker.name or attacker.race} cannot attack, they are K.O.")
        return messages, 0

    # Intent message
    messages.append(f"{attacker.name or attacker.race} attacks {target.name or target.race}...")

    # Calculate damage
    damage = calculate_damage(attacker)

    # Result message
    messages.append(f"The attack deals {damage} damage!")

    # Predict if target will be defeated, without applying damage
    if (target.hp - damage) <= 0:
        messages.append(f"{target.name or target.race} has been defeated!")

    return messages, damage

def flee(hero: Hero, monster: Monster):
    """
    Attempt to flee combat. Returns a tuple (success, messages, damage taken if failed).
    """
    messages = []

    # Flee chance calculation
    base_chance = 50
    dice_result = Die(1, 6).roll()

    if dice_result == 1: dice_bonus = -15
    elif dice_result == 2: dice_bonus = -10
    elif dice_result == 3: dice_bonus = -5
    elif dice_result == 4: dice_bonus = 5
    elif dice_result == 5: dice_bonus = 10
    else: dice_bonus = 15

    hero_bonus = modifier(hero.endurance) * 8
    monster_penalty = modifier(monster.strength) * 6

    endurance_diff = hero.endurance - monster.endurance
    if endurance_diff > 3: level_bonus = 10
    elif endurance_diff > 0: level_bonus = 5
    elif endurance_diff < -3: level_bonus = -10
    elif endurance_diff < 0: level_bonus = -5
    else: level_bonus = 0

    flee_chance = max(10, min(90, base_chance + dice_bonus + hero_bonus - monster_penalty + level_bonus))
    final_roll = Die(1, 100).roll()
    success = final_roll <= flee_chance

    messages.append(f"{hero.name} attempts to flee (base roll: {dice_result}, chance: {flee_chance}%)...")

    if success:
        messages.append("You flee successfully!")
        return True, messages, 0
    else:
        messages.append("The escape failed!")
        # On failure, the monster attacks. Prepare messages and damage.
        counter_messages, counter_damage = attack(monster, hero)
        messages.extend(counter_messages)
        return False, messages, counter_damage

def loot(hero: Hero, monster: Monster):
    """The hero searches a dead monster and returns messages."""
    messages = []
    if monster.is_alive():
        messages.append("The monster is still alive, cannot loot!")
        return messages

    messages.append(f"{hero.name} searches the {monster.race}.")
    if monster.gold > 0:
        hero.gold += monster.gold
        messages.append(f"Found {monster.gold} gold piece(s).")
    if monster.leather > 0:
        hero.leather += monster.leather
        messages.append(f"Recovered {monster.leather} piece(s) of leather.")

    if not monster.gold and not monster.leather:
        messages.append(f"The {monster.race} had nothing of interest.")

    return messages
