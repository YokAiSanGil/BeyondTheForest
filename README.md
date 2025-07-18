# HeroesVsMonsters

Un jeu de combat textuel en Python.

## Installation

1. Cloner le dépôt :

   ```bash
   git clone https://github.com/YokAiSanGil/HeroesVsMonsters.git
   cd HeroesVsMonsters
   ```

2. Installer Python 3.12
3. Installer les dépendances :

   ```bash
   pip install pygame
   ```

## Usage

Lancer la partie :
Lancer la partie :

```bash
python _main.py
```

## Structure du projet

- `personnages/` : classes `Hero`, `Monster`, `actions`
- `interfaces/` : phases de jeu (`PhaseMenu`, `PhaseExploration`, `PhaseCombat`, `PhaseSoin`)
- `affichage/` : ASCII art, widgets d'affichage
- `utils/` : utilitaires, gestion de la musique et des dés
- `_main.py` : point d'entrée du jeu

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
