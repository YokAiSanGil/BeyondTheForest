def modificateur(valeur):
    """Calcule le modificateur selon la force/endurance."""
    if valeur < 5:
        return -1
    elif valeur < 10:
        return 0
    elif valeur < 15:
        return 1
    else:
        return 2
