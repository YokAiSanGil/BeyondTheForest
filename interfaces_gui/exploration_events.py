import random
from utils.dice import Die

def get_exploration_event(hero):
    """
    Generate an exploration event (ambient text + optional bonus).
    Returns (message, bonus_dict)
    bonus_dict may contain {'gold': int} or be empty.
    """
    messages = [
        "You move cautiously through the forest...",
        "The trees whisper ancient secrets...",
        "Your footsteps echo on the mossy ground...",
        "A mysterious breeze brushes your face...",
        "You sense a presence in the shadows...",
        "The forest seems alive, every sound draws your attention...",
        "You hear birdsong in the distance...",
        "A light mist envelops the trees...",
        "You walk on a carpet of dead leaves...",
        "A crack in the bushes startles you...",
        "You feel like you're being watched...",
        "A wild boar passes nearby.",
        "You press onward, heart pounding...",
        "A boar passes nearby, your stomach growling...",
        "Songs carried by the wind drift through the dark forest.",
        "You feel like you've passed through here before...",
        "A strange noise catches your attention...",
        "You hear the murmur of a river in the distance...",
        "The smell of damp earth fills your nostrils...",
        "You hear the sound of your own steps on the dead leaves...",
        "A spiderweb glistens with dew in a ray of sunlight...",
        "A colourful butterfly flutters before you then vanishes...",
        "You notice footprints in the soft earth...",
        "The wind makes the leaves dance above your head...",
        "A branch snaps somewhere behind you...",
        "The echo of your steps fades into the vastness of the forest..."
    ]

    if hero:
        messages.extend([
            f"{hero.name} scans the surroundings carefully...",
            f"{hero.name} senses a strange energy in the air...",
            f"{hero.name} notices curious tracks in the mud...",
            f"{hero.name} pauses for a moment to listen...",
            f"{hero.name} carefully circles around a thorny bush..."
        ])

    message = random.choice(messages)
    bonus = {}

    # Chance of bonus (1 in 6)
    if Die.roll() == 6:
        type_bonus = Die.roll()
        if type_bonus <= 3:
            # Gold
            amount = Die.roll()
            bonus['gold'] = amount
            message += f" ✨ (+{amount} Gold)"
        else:
            # Extra ambience
            extras = [
                " A strange mushroom catches your eye.",
                " A firefly glows for a moment.",
                " An owl hoots in the distance."
            ]
            message += f"{random.choice(extras)}"

    return message, bonus
