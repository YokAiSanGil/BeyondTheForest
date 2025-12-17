"""
Module affichage - Utilitaires et widgets d'affichage.
Contient les fonctions pour l'affichage, les animations et les widgets.
"""

from .widgets import creer_barre_de_vie, combiner_blocs_ascii, afficher_journal_combat, afficher_stats_finales
from .animations import ligne_par_ligne, ecrire_lentement

__all__ = [
    'creer_barre_de_vie',
    'combiner_blocs_ascii',
    'afficher_journal_combat',
    'afficher_stats_finales',
    'ligne_par_ligne',
    'ecrire_lentement'
]