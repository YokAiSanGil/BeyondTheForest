"""
Module interface de jeu en console.
Ce module est inspiré de l'interface de jeu de Dragon Quest 1. 
"""


from actions import depecer, fuir, frapper
from perso import Personnage
from heros import Hero
from monstre import Monster, creer_monstre_aleatoire
from outils import *
from music import battle_music, stop_music
from ascii_art import *
from menu_anime import MenuAnime, afficher_fenetre, afficher_titre_simple


def afficher_ecran_intro():
    """
    Affiche l'art ascii de l'intro tout stylé du jeu.
    Version de 'main' qui utilise ligne_par_ligne.
    """
    clear_screen()
    ligne_par_ligne(OPENING, 0.1)
    pause(2)
    print(TITLE_SCREEN)
    suivant()

def menu_principal():
    """
    Menu principal qui utilise la nouvelle classe MenuAnime.
    """
    options = [
        ("NOUVEAU JEU", "nouveau"),
        ("CONTINUER", "continuer"),
        ("QUITTER", "quitter")
    ]
    menu = MenuAnime()
    return menu.afficher("MENU", options)

def continuer_jeu():
    """
    Charge une partie existante.
    """
    clear_screen()
    ecrire_lentement("La fonctionnalité de sauvegarde n'est pas encore implémentée...")
    ecrire_lentement("Revenez bientôt pour cette fonctionnalité !")
    pause(2)
    return None

def quitter_jeu():
    """
    Quitte le jeu avec confirmation, en utilisant MenuAnime.
    """
    options_quitter = [
        ("Oui, quitter le jeu", "oui"),
        ("Non, continuer l'aventure", "non")
    ]
    menu = MenuAnime()
    confirmer = menu.afficher("Voulez-vous vraiment quitter ?", options_quitter)
    
    if confirmer == "oui":
        clear_screen()
        message_fin = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║                Merci d'avoir joué !                  ║
║                                                      ║
║         À bientôt dans Heroes Vs Monsters !          ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""
        print(message_fin)
        ecrire_lentement("Au revoir, brave aventurier...")
        exit()
    else:
        return False

def creer_hero():
    """
    Crée un héros, fusion des deux versions.
    """
    clear_screen()
    ecrire_lentement("Bienvenue, brave aventurier !")
    ecrire_lentement("Quel est votre nom ?")
    nom = input("► ")
    while not nom.strip():
        print("Vous devez avoir un nom, brave Hero ...")
        nom = input("► ")

    clear_screen()
    ecrire_lentement(f"Enchanté, {nom} !")
    ecrire_lentement("Votre forme actuelle est une ame perdue.")
    ecrire_lentement("...",0.9)
    
    pause(1)
    clear_screen()
    options_race = [
        ("HUMAIN (+1 Force, +1 Endurance)", "Humain"),
        ("NAIN (+2 Endurance)", "Nain")
    ]
    menu = MenuAnime.style_simple()
    race = menu.afficher(f"Choisissez une nouvelle forme physique.", options_race)

    if race is None:
        return creer_hero()
    
    hero = Hero(nom, race)
    clear_screen()
    ecrire_lentement('... vous possédez une nouvelle forme ...', 0.07)
    ecrire_lentement(f"{hero.nom}, la foret vous appelle.", 0.07)
    ecrire_lentement("...", 0.9)
    pause(1)
    clear_screen()

    ASCII = NAIN if hero.race == "Nain" else HUMAIN
    ligne_par_ligne(ASCII, 0.2)
    pause(1)
    stats_contenu = f"""
{hero.nom.upper()} {('le ' if hero.race == "Nain" else "l'")}{hero.race.upper()}

Endurance     : {hero.endurance}
Force         : {hero.force}
Points de Vie : {hero.points_de_vie}
Or            : {hero.gold}
Cuir          : {hero.cuir}
"""
    afficher_fenetre(stats_contenu, largeur_min=30, marge=4)
    suivant()
    return hero

# On garde les fonctions de HvsM_BattleBranche pour l'affichage du combat
def creer_barre_de_vie(pv_actuels, pv_max, longueur=20):
    pv_actuels = max(0, pv_actuels)
    pourcentage = pv_actuels / pv_max if pv_max > 0 else 0
    pv_remplis = int(longueur * pourcentage)
    pv_vides = longueur - pv_remplis
    barre = '█' * pv_remplis + '░' * pv_vides
    return f"[{barre}] {pv_actuels}/{pv_max}"


def combiner_blocs_ascii(bloc_gauche, bloc_droit, espacement=10):
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


def afficher_journal_combat(hero: Hero, monstre: Monster, messages: list):
    for msg in messages:
        art_hero = HUMAIN if hero.race == "Humain" else NAIN
        info_hero = f"{hero.nom} le {hero.race}\n{creer_barre_de_vie(hero.points_de_vie, hero.points_de_vie_max)}"
        bloc_hero = f"{art_hero}\n{info_hero}"
        race_monstre_lower = monstre.race.lower().strip()
        if race_monstre_lower == "loup": art_monstre = WOLF
        elif race_monstre_lower == "orque": art_monstre = ORC
        else: art_monstre = DRAGONNET
        info_monstre = f"{monstre.race}\n{creer_barre_de_vie(monstre.points_de_vie, monstre.points_de_vie_max)}"
        bloc_monstre = f"{info_monstre}\n{art_monstre}"
        combat_info = combiner_blocs_ascii(bloc_hero, bloc_monstre, espacement=15)
        clear_screen()
        print(combat_info)
        print("=" * 80)
        ecrire_lentement(msg)
        suivant()

# Interface de soin de la branche 'main'
def interface_soin(hero: Hero):
    clear_screen()
    hero_ascii = NAIN if hero.race == "Nain" else HUMAIN
    print(hero_ascii)
    barre_vie = creer_barre_de_vie(hero.points_de_vie, hero.points_de_vie_max)
    print(f"\n{hero.nom} le {hero.race}")
    print(f"PV: {barre_vie}")
    print(f"Or: {hero.gold} | Cuir: {hero.cuir}")
    print("\n" + "=" * 50 + "\n")
    if hero.points_de_vie < hero.points_de_vie_max:
        ecrire_lentement(f"{hero.nom} prend un moment pour se soigner...")
        suivant()
        clear_screen()
        options_soin = [("SE REPOSER (Récupère tous les PV)", "repos"), ("CONTINUER L'AVENTURE", "continuer")]
        menu = MenuAnime.style_simple()
        choix = menu.afficher("Que voulez-vous faire ?", options_soin)
        if choix == "repos":
            clear_screen()
            ecrire_lentement(f"{hero.nom} se repose paisiblement...")
            suivant()
            clear_screen()
            ancien_pv = hero.points_de_vie
            hero.se_reposer()
            pv_recuperes = hero.points_de_vie - ancien_pv
            ecrire_lentement(f"✨ {hero.nom} récupère {pv_recuperes} PV !")
            suivant()
            clear_screen()
            nouvelle_barre = creer_barre_de_vie(hero.points_de_vie, hero.points_de_vie_max)
            print(f"{hero.nom} le {hero.race}")
            print(f"PV: {nouvelle_barre}")
            print("\n💚 Complètement restauré !")
            suivant()
        else:
            clear_screen()
            ecrire_lentement(f"{hero.nom} décide de continuer malgré ses blessures...")
            suivant()
    else:
        ecrire_lentement(f"{hero.nom} est en pleine forme !")
        suivant()
        clear_screen()
        ecrire_lentement("Prêt pour de nouvelles aventures !")
        suivant()
    clear_screen()
    ecrire_lentement(f"{hero.nom} reprend son exploration...")
    suivant()
    return "exploration"


def interface_combat(hero: Hero, monstre: Monster):
    """
    Interface de combat fusionnée.
    """
    battle_music()
    clear_screen()
    ecrire_lentement(f"Un {monstre.race} sauvage apparaît !")
    suivant()
    
    # Création d'une instance de menu réutilisable pour le combat
    menu_combat = MenuAnime(
        instructions="↑↓ Sélectionner, Entrée pour confirmer",
        afficher_titre_jeu=False,
        conserver_ecran=True,  # Important pour ne pas effacer le header
        style_fenetre=False
    )

    while hero.est_vivant() and monstre.est_vivant():
        # Préparation de l'affichage
        art_hero = HUMAIN if hero.race == "Humain" else NAIN
        info_hero = f"{hero.nom} le {hero.race}\n{creer_barre_de_vie(hero.points_de_vie, hero.points_de_vie_max)}"
        bloc_hero = f"{art_hero}\n{info_hero}"
        
        race_monstre_lower = monstre.race.lower().strip()
        if race_monstre_lower == "loup": art_monstre = WOLF
        elif race_monstre_lower == "orque": art_monstre = ORC
        else: art_monstre = DRAGONNET
        
        info_monstre = f"{monstre.race}\n{creer_barre_de_vie(monstre.points_de_vie, monstre.points_de_vie_max)}"
        bloc_monstre = f"{info_monstre}\n{art_monstre}"
        
        combat_info = combiner_blocs_ascii(bloc_hero, bloc_monstre, espacement=15)
        
        # Affichage manuel de l'état du combat
        clear_screen()
        print(combat_info)
        print("=" * 80)

        options_combat = [("FRAPPER", "attaquer"), ("FUIR", "fuir"), ("STATS", "stats")]
        
        # Appel du menu sans header_info
        action = menu_combat.afficher(f"Que fait {hero.nom} ?", options_combat)
        
        if action == "attaquer":
            messages_attaque, degats_attaque = frapper(hero, monstre)
            
            # Afficher l'intention d'attaquer
            afficher_journal_combat(hero, monstre, messages_attaque[:1])
            
            # Appliquer les dégâts et afficher le résultat
            monstre.points_de_vie -= degats_attaque
            if len(messages_attaque) > 1:
                afficher_journal_combat(hero, monstre, messages_attaque[1:])

            if monstre.est_vivant() and hero.est_vivant():
                messages_contre, degats_contre = frapper(monstre, hero)
                
                # Afficher l'intention de la contre-attaque
                afficher_journal_combat(hero, monstre, messages_contre[:1])

                # Appliquer les dégâts et afficher le résultat
                hero.points_de_vie -= degats_contre
                if len(messages_contre) > 1:
                    afficher_journal_combat(hero, monstre, messages_contre[1:])
                
        elif action == "fuir":
            succes_fuite, messages_fuite, degats_fuite = fuir(hero, monstre)
            if not succes_fuite:
                afficher_journal_combat(hero, monstre, messages_fuite[:1]) # Message de tentative
                hero.points_de_vie -= degats_fuite
                afficher_journal_combat(hero, monstre, messages_fuite[1:]) # Messages de contre-attaque
            else:
                afficher_journal_combat(hero, monstre, messages_fuite)
                stop_music()
                interface_soin(hero) # Appel de la nouvelle fonction de soin
                return "fuite"

        elif action == "stats":
            afficher_stats_combat(hero, monstre)
            continue
            
        elif action is None: # L'utilisateur a appuyé sur Echap
            # L'écran est déjà affiché avec les bonnes infos, on affiche juste le menu de confirmation
            options_confirmer = [("Oui, abandonner le combat", "oui"), ("Non, continuer à combattre", "non")]
            confirmer = menu_combat.afficher("Voulez-vous vraiment abandonner ?", options_confirmer)
            if confirmer == "oui":
                stop_music()
                return "abandon"
            else:
                continue

    stop_music()
    if hero.est_vivant():
        messages_fin_combat = [f"Le {monstre.race} est vaincu !", f"{hero.nom} remporte la victoire !"]
        afficher_journal_combat(hero, monstre, messages_fin_combat)
        messages_depouillement = depecer(hero, monstre)
        if messages_depouillement:
            afficher_journal_combat(hero, monstre, messages_depouillement)
        interface_soin(hero) # Appel de la nouvelle fonction de soin
        return "victoire"
    else:
        messages_fin_combat = [f"{hero.nom} est vaincu...", "GAME OVER"]
        afficher_journal_combat(hero, monstre, messages_fin_combat)
        return "defaite"

def afficher_stats_combat(hero: Hero, monstre: Monster):
    """
    Affiche les statistiques détaillées avec l'art ASCII du héros
    en utilisant afficher_fenetre de manière compatible avec combiner_blocs_ascii.
    """
    clear_screen()

    # --- Préparation du bloc du Héros ---
    art_hero = HUMAIN if hero.race == "Humain" else NAIN
    
    # Contenu textuel des stats du héros
    stats_hero_contenu = f"""
{hero.nom.upper()} - {hero.race.upper()}
- - - - - - - - - - - - - - -
Endurance   : {hero.endurance}
Force       : {hero.force}
PV          : {hero.points_de_vie}/{hero.points_de_vie_max}
Or          : {hero.gold}
Cuir        : {hero.cuir}
"""

    # Utilisation d'afficher_fenetre en mode "retour de chaîne"
    cadre_hero = afficher_fenetre(stats_hero_contenu, largeur_min=25, marge=4, retourner_string=True)
    
    # Combinaison du cadre et de l'art ASCII
    bloc_hero_final = combiner_blocs_ascii(cadre_hero, art_hero, espacement=5)

    # --- Préparation du bloc du Monstre ---
    stats_monstre_contenu = f"""
{monstre.race.upper()}
- - - - - - - - - - - - - - -
Endurance   : {monstre.endurance}
Force       : {monstre.force}
PV          : {monstre.points_de_vie}/{monstre.points_de_vie_max}
"""

    # --- Affichage final ---
    print("STATISTIQUES DÉTAILLÉES\n")
    print(bloc_hero_final)
    print("\n")
    afficher_fenetre(stats_monstre_contenu, largeur_min=25, marge=4)  # Utilisation normale

    print("\nAppuyez sur Entrée pour revenir au combat...")
    suivant()

def message_exploration():
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
        "Un crasquement dans les buissons vous fait sursauter...",
        "Vous avez l'impression d'être observé...",
        "Un sanglier passe à proximité.",
        "Vous continuez à avancer, le cœur battant...",
        "Un sanglier passe à proximité, vous avez le ventre qui gargouille...",
        "Des chants portés par le vent traversent la forêt obscure.",
        "Vous avez l'impression d'être déjà passé par ici...",
        "Un bruit étrange attire votre attention...",
        "Vous entendez le murmure d'une rivière au loin...",
    ]
    import random
    message = random.choice(messages)
    ecrire_lentement(message)

def afficher_stats_finales(hero: Hero, monstres_vaincus: int):
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
