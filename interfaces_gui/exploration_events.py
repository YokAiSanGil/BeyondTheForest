import random
from utils.de6faces import De

def get_exploration_event(hero):
    """
    Génère un événement d'exploration (texte d'ambiance + bonus éventuel).
    Retourne (message, bonus_dict)
    bonus_dict peut contenir {'gold': int} ou être vide.
    """
    messages = [
        "Vous avancez prudemment dans la forêt...",
        "Les arbres murmurent des secrets anciens...",
        "Vos pas résonnent sur le sol moussu...",
        "Une brise mystérieuse caresse votre visage...",
        "Vous sentez une présence dans l'ombre...",
        "La forêt semble vivante, chaque bruit attire votre attention...",
        "Vous entendez le chant des oiseaux au loin...",
        "Un léger brouillard enveloppe les arbres...",
        "Vous marchez sur un tapis de feuilles mortes...",
        "Un craquement dans les buissons vous fait sursauter...",
        "Vous avez l'impression d'être observé...",
        "Un sanglier passe à proximité.",
        "Vous continuez à avancer, le cœur battant...",
        "Un sanglier passe à proximité, vous avez le ventre qui gargouille...",
        "Des chants portés par le vent traversent la forêt obscure.",
        "Vous avez l'impression d'être déjà passé par ici...",
        "Un bruit étrange attire votre attention...",
        "Vous entendez le murmure d'une rivière au loin...",
        "L'odeur de la terre humide remplit vos narines...",
        "Vous entendez le bruit de vos propres pas sur les feuilles mortes...",
        "Une toile d'araignée scintille de rosée dans un rayon de soleil...",
        "Un papillon coloré volette devant vous avant de disparaître...",
        "Vous remarquez des traces de pas dans la terre meuble...",
        "Le vent fait danser les feuilles au-dessus de votre tête...",
        "Une branche craque quelque part derrière vous...",
        "L'écho de vos pas se perd dans l'immensité de la forêt..."
    ]
    
    if hero:
        messages.extend([
            f"{hero.nom} scrute les alentours avec attention...",
            f"{hero.nom} ressent une étrange énergie dans l'air...",
            f"{hero.nom} remarque de curieuses empreintes dans la boue...",
            f"{hero.nom} s'arrête un instant pour écouter...",
            f"{hero.nom} contourne prudemment un buisson épineux..."
        ])
    
    message = random.choice(messages)
    bonus = {}
    
    # Chance de bonus (1 sur 6)
    if De.lancer() == 6:
        type_bonus = De.lancer()
        if type_bonus <= 3:
            # Or
            amount = De.lancer()
            bonus['gold'] = amount
            message += f" ✨ (+{amount} Or)"
        else:
            # Ambiance extra
            extras = [
                " Un champignon bizarre attire votre oeil.",
                " Une luciole brille un instant.",
                " Un hibou hulule au loin."
            ]
            message += f"{random.choice(extras)}"
            
    return message, bonus
