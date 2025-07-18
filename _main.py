"""
Script principal utilisant l'interface Dragon Quest avec architecture modulaire.
"""
from music import *
from interfaces.phase_menu import PhaseMenu
from interfaces.phase_combat import PhaseCombat
from interfaces.phase_soin import PhaseSoin
from interfaces.phase_exploration import PhaseExploration
from affichage.widgets import afficher_stats_finales
from utils.outils import clear_screen, ecrire_lentement, pause, suivant
import random

def main():
    """
    Fonction principale du jeu utilisant l'architecture modulaire avec classes.
    """
    # Initialisation des interfaces
    phase_menu = PhaseMenu()
    phase_combat = PhaseCombat()
    phase_soin = PhaseSoin()
    phase_exploration = PhaseExploration()
    
    # Variables de jeu
    hero = None
    monstres_vaincus = 0
    
    # Affichage de l'intro
    phase_menu.afficher_ecran_intro()
    
    # Boucle principale du jeu
    while True:
        # Affichage du menu principal
        choix = phase_menu.afficher_menu_principal()
        
        if choix == "nouveau":
            # Nouvelle partie
            hero = phase_menu.creer_hero()
            if hero is None:
                continue
            
            monstres_vaincus = 0
            clear_screen()
            ecrire_lentement(f"Vous entrez dans la forêt des âmes damnées...")
            pause(3)
            
            # Boucle de jeu
            while hero.est_vivant():
                # Phase d'exploration
                resultat_exploration = phase_exploration.afficher(hero)
                
                if resultat_exploration == "combat":
                    # Un monstre a été rencontré
                    monstre = phase_exploration.get_monstre_rencontre()
                    
                    # Phase de combat
                    resultat_combat = phase_combat.afficher(hero, monstre)
                    
                    if resultat_combat == "victoire":
                        monstres_vaincus += 1
                        # Soin automatique après victoire
                        phase_soin.afficher(hero)
                        
                    elif resultat_combat == "defaite":
                        break
                        
                    elif resultat_combat == "fuite":
                        # Soin automatique après fuite
                        phase_soin.afficher(hero)
                        
                    elif resultat_combat == "abandon":
                        ecrire_lentement("Vous quittez votre forme physique...")
                        suivant()
                        break
                        
                elif resultat_exploration == "soin":
                    # Phase de soin demandée
                    phase_soin.afficher(hero)
                    
                elif resultat_exploration == "menu":
                    # Retour au menu principal
                    break
            
            # Fin du jeu - affichage des stats finales
            afficher_stats_finales(hero, monstres_vaincus)
            
        elif choix == "continuer":
            # Continuer une partie (pas encore implémenté)
            phase_menu.continuer_jeu()
            
        elif choix == "quitter":
            # Quitter le jeu
            if phase_menu.confirmer_quitter():
                break
                
        elif choix is None:  # Échap pressé
            # Menu de confirmation pour quitter
            if phase_menu.confirmer_quitter():
                break

if __name__ == "__main__":
    clear_screen()
    main()

