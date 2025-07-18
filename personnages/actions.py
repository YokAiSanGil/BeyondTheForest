"""
Module de gestion des actions.
Ce module contient les classes et fonctions pour la gestion 
des actions dans le jeu.
"""
from .personnage import Personnage
from .hero import Hero
from .monstre import Monster
from utils.de6faces import De
from utils.outils import modificateur


def calculer_degats(attaquant: Personnage):
    """Calcule les dégâts pour une attaque."""
    de4 = De(1, 4)
    return de4.lancer() + modificateur(attaquant.force)

def frapper(attaquant: Personnage, cible: Personnage):
    """
    Prépare une séquence d'attaque et retourne les messages et les dégâts.
    N'APPLIQUE PAS les dégâts directement.
    Ceci est la version de HvsM_BattleBranche, qui est nécessaire pour l'interface de combat.
    """
    messages = []
    if not attaquant.est_vivant():
        messages.append(f"{attaquant.nom or attaquant.race} ne peut pas attaquer, il est K.O.")
        return messages, 0

    # Message d'intention
    messages.append(f"{attaquant.nom or attaquant.race} attaque {cible.nom or cible.race}...")

    # Calcul des dégâts
    degats = calculer_degats(attaquant)
    
    # Message de résultat
    messages.append(f"L'attaque inflige {degats} points de dégâts !")
    
    # Prévoir si la cible sera vaincue, sans appliquer les dégâts
    if (cible.points_de_vie - degats) <= 0:
        messages.append(f"{cible.nom or cible.race} a été vaincu !")
    
    return messages, degats

def fuir(personnage: Hero, monstre: Monster):
    """
    Tente de fuir le combat. Combine la logique de 'main' avec le retour de messages de 'HvsM_BattleBranche'.
    Retourne un tuple (succès, messages, dégâts subis si échec).
    """
    messages = []
    
    # Logique de calcul de la branche 'main'
    chance_base = 50
    resultat_de = De(1, 6).lancer()
    
    if resultat_de == 1: bonus_de = -15
    elif resultat_de == 2: bonus_de = -10
    elif resultat_de == 3: bonus_de = -5
    elif resultat_de == 4: bonus_de = 5
    elif resultat_de == 5: bonus_de = 10
    else: bonus_de = 15
    
    bonus_hero = modificateur(personnage.endurance) * 8
    malus_monstre = modificateur(monstre.force) * 6
    
    diff_endurance = personnage.endurance - monstre.endurance
    if diff_endurance > 3: bonus_niveau = 10
    elif diff_endurance > 0: bonus_niveau = 5
    elif diff_endurance < -3: bonus_niveau = -10
    elif diff_endurance < 0: bonus_niveau = -5
    else: bonus_niveau = 0
    
    chance_fuite = max(10, min(90, chance_base + bonus_de + bonus_hero - malus_monstre + bonus_niveau))
    jet_final = De(1, 100).lancer()
    reussite = jet_final <= chance_fuite

    messages.append(f"{personnage.nom} tente de fuir (dé de base: {resultat_de}, chance: {chance_fuite}%)...")

    if reussite:
        messages.append("La fuite réussit !")
        return True, messages, 0
    else:
        messages.append("La fuite a échoué !")
        # En cas d'échec, le monstre attaque. On prépare les messages et les dégâts.
        contre_messages, contre_degats = frapper(monstre, personnage)
        messages.extend(contre_messages) # Ajoute l'intention et le résultat
        return False, messages, contre_degats

def depecer(hero: Hero, monstre: Monster):
    """Le héros dépouille un monstre mort et retourne les messages."""
    messages = []
    if monstre.est_vivant():
        messages.append("Le monstre est encore vivant, impossible de le dépecer !")
        return messages

    messages.append(f"{hero.nom} dépouille le {monstre.race}.")
    if monstre.gold > 0:
        hero.gold += monstre.gold
        messages.append(f"Il trouve {monstre.gold} pièce(s) d'or.")
    if monstre.cuir > 0:
        hero.cuir += monstre.cuir
        messages.append(f"Il récupère {monstre.cuir} morceau(x) de cuir.")
    
    if not monstre.gold and not monstre.cuir:
        messages.append(f"Le {monstre.race} n'avait rien d'intéressant.")
        
    return messages
