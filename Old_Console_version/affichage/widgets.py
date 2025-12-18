"""
Module widgets - Fonctions d'affichage et widgets pour le jeu.
Ce module contient les fonctions d'affichage réutilisables et les widgets visuels.
"""

from Old_Console_version.utils.outils import clear_screen, ecrire_lentement, suivant
from affichage.ascii_art import HUMAIN, NAIN, WOLF, ORC, DRAGONNET


def creer_barre_de_vie(pv_actuels, pv_max, longueur=20):
    """
    Crée une barre de vie visuelle.
    """
    pv_actuels = max(0, pv_actuels)
    pourcentage = pv_actuels / pv_max if pv_max > 0 else 0
    pv_remplis = int(longueur * pourcentage)
    pv_vides = longueur - pv_remplis
    barre = '█' * pv_remplis + '░' * pv_vides
    return f"[{barre}] {pv_actuels}/{pv_max}"


def combiner_blocs_ascii(bloc_gauche, bloc_droit, espacement=10):
    """
    Combine deux blocs ASCII côte à côte.
    """
    lignes_gauche = bloc_gauche.split('\n')
    lignes_droit = bloc_droit.split('\n')
    largeur_gauche = max(len(l) for l in lignes_gauche) if lignes_gauche else 0
    nb_lignes_max = max(len(lignes_gauche), len(lignes_droit))
    
    while len(lignes_gauche) < nb_lignes_max:
        lignes_gauche.append('')
    while len(lignes_droit) < nb_lignes_max:
        lignes_droit.append('')
    
    resultat = []
    for i in range(nb_lignes_max):
        ligne_g = lignes_gauche[i]
        ligne_d = lignes_droit[i]
        ligne_combinee = f"{ligne_g:<{largeur_gauche}}{' ' * espacement}{ligne_d}"
        resultat.append(ligne_combinee)
    
    return "\n".join(resultat)


def afficher_journal_combat(hero, monstre, messages: list):
    """
    Affiche le journal de combat avec les infos des protagonistes.
    """
    for msg in messages:
        art_hero = HUMAIN if hero.race == "Humain" else NAIN
        info_hero = f"{hero.nom} le {hero.race}\n{creer_barre_de_vie(hero.points_de_vie, hero.points_de_vie_max)}"
        bloc_hero = f"{art_hero}\n{info_hero}"
        
        race_monstre_lower = monstre.race.lower().strip()
        if race_monstre_lower == "loup": 
            art_monstre = WOLF
        elif race_monstre_lower == "orque": 
            art_monstre = ORC
        else: 
            art_monstre = DRAGONNET
            
        info_monstre = f"{monstre.race}\n{creer_barre_de_vie(monstre.points_de_vie, monstre.points_de_vie_max)}"
        bloc_monstre = f"{info_monstre}\n{art_monstre}"
        
        combat_info = combiner_blocs_ascii(bloc_hero, bloc_monstre, espacement=15)
        clear_screen()
        print(combat_info)
        print("=" * 80)
        ecrire_lentement(msg)
        suivant()


def afficher_stats_finales(hero, monstres_vaincus: int):
    """
    Affiche les statistiques finales du héros.
    """
    clear_screen()
    stats_finales = f"""
STATISTIQUES FINALES
Héros            : {hero.nom} le {hero.race}
Monstres vaincus : {monstres_vaincus}
Or collecté      : {hero.gold}
Cuir collecté    : {hero.cuir}
PV restants      : {hero.points_de_vie}
Merci d'avoir joué !
"""
    print(stats_finales)
    suivant()
