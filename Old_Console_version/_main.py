"""
Script principal utilisant l'interface Dragon Quest avec architecture modulaire.
"""
import sys
import os
# Ajouter le dossier parent au path pour trouver les modules partagés (personnages, utils, etc.)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.music import *
from interfaces.phase_menu import PhaseMenu
from interfaces.phase_combat import PhaseCombat

from interfaces.phase_exploration import PhaseExploration
from affichage.widgets import afficher_stats_finales
from utils.outils import clear_screen, ecrire_lentement, pause, suivant
import random
from interfaces.phase_soin import PhaseSoin

def main():
    """
    Fonction principale du jeu utilisant l'architecture modulaire avec classes.
    """
    # Initialisation des interfaces
    phase_menu = PhaseMenu()
    phase_combat = PhaseCombat()
    phase_exploration = PhaseExploration()
    phase_soin = PhaseSoin()
    
    # Variables de jeu
    hero = None
    monstres_vaincus = 0
    
    # Affichage de l'intro
    phase_menu.afficher_ecran_intro()
    
    # Boucle principale du jeu
    while True:
        # Affichage du menu principal
        choix = phase_menu.afficher_menu_principal()
        
        if choix in ("nouveau", "continuer"):
            # Démarrer ou reprendre une partie
            if choix == "nouveau":
                hero = phase_menu.creer_hero()
                monstres_vaincus = 0
                if hero is None:
                    continue
                clear_screen()
                ecrire_lentement("Vous entrez dans la forêt des âmes damnées...")
                pause(3)
            else:
                result = phase_menu.continuer_jeu()
                if result is None:
                    continue
                hero, monstres_vaincus = result
                clear_screen()
                ecrire_lentement("Vous reprenez votre aventure au plus profond de la forêt...")
                pause(3)

            # Boucle de jeu
            while hero.est_vivant():
                resultat_exploration = phase_exploration.afficher(hero)

                if resultat_exploration == "combat":
                    monstre = phase_exploration.get_monstre_rencontre()

                    if monstre is not None:
                        resultat_combat = phase_combat.afficher(hero, monstre)

                        if resultat_combat == "victoire":
                            monstres_vaincus += 1
                            phase_soin.afficher(hero)
                        elif resultat_combat == "defaite":
                            break
                        elif resultat_combat == "fuite":
                            phase_soin.afficher(hero)
                        elif resultat_combat == "abandon":
                            ecrire_lentement("Vous quittez votre forme physique...")
                            suivant()
                            break
                    else:
                        ecrire_lentement("Erreur : aucun monstre trouvé pour le combat.")
                        continue

                elif resultat_exploration == "soin":
                    phase_soin.afficher(hero)
                elif resultat_exploration == "menu":
                    break

            # Fin du jeu - affichage des stats finales
            afficher_stats_finales(hero, monstres_vaincus)

        elif choix == "quitter":
            # Quitter le jeu
            if phase_menu.confirmer_quitter():
                break
                
        elif choix is None:  # Échap pressé
            # Menu de confirmation pour quitter
            if phase_menu.confirmer_quitter():
                break

if __name__ == "__main__":
    try:
        clear_screen()
        main()
    except KeyboardInterrupt:
        print("\n\nInterruption par l'utilisateur.")
    except Exception as e:
        print(f"\n\nUne erreur inattendue est survenue : {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Nettoyage final pour garantir un terminal propre
        stop_music()
        print("\033[?25h") # Réafficher le curseur
        print("\nFin du programme.")

