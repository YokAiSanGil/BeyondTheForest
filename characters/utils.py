def modifier(value):
    """Calculate the modifier based on strength/endurance."""
    if value < 5:
        return -1
    elif value < 10:
        return 0
    elif value < 15:
        return 1
    else:
        return 2
