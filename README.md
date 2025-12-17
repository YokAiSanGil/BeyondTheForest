# BEYOND the FOREST

A retro-style RPG adventure game built with Python and Pygame.

## Overview

BEYOND the FOREST invites you to explore the Dark Forest. Create your hero, battle fearsome monsters, and survive as long as you can in this object-oriented programming project brought to life with a nostalgic CRT aesthetic.

## Features

*   **Retro GUI**: A custom graphical interface featuring scanlines, CRT flicker effects, and pixel-art style rendering.
*   **Character Creation**: Choose your race (Human or Dwarf), name your hero, and roll your stats.
*   **Exploration**: Wander through the dark forest with dynamic background images and rich atmospheric text events.
*   **AI NPC Interaction**: Encounter The Hermit, a mysterious entity powered by a local LLM (Gemma) for dynamic roleplay conversations.
*   **Combat System**: Turn-based battles against BloodFairies, HellParasites, NightScreamers, StingFishes, and StrygMoths.
*   **Progression**: Gain gold, loot leather, and manage your health.
*   **Save System**: Auto-save functionality allows you to continue your journey where you left off.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/YokAiSanGil/BeyondTheForest.git
    cd BeyondTheForest
    ```

2.  **Prerequisites:**
    *   Python 3.12 or higher.
    *   `pygame` library.
    *   `llama-cpp-python` library.

3.  **Install dependencies:**

    ```bash
    pip install pygame llama-cpp-python
    ```

4.  **Setup AI Model:**
    *   Create a folder named `models` in the root directory.
    *   Download the `gemma-3npc-it-q4_k_m.gguf` model.
    *   Place the file in `models/gemma-3npc-it-q4_k_m.gguf`.

## How to Play

Launch the game using the main GUI script:

```bash
python3 main_gui.py
```

*   **Controls**: Use the **Arrow Keys** to navigate menus and **Enter** to select options.
*   **Gameplay**:
    *   **New Game**: Create a new hero.
    *   **Continue**: Load your last saved hero.
    *   **Explore**: Venture into the forest to find events or monsters.
    *   **Rest**: Heal your wounds (auto-saves the game).

## Project Structure

*   `main_gui.py`: The main entry point for the graphical version of the game.
*   `affichage_gui/`: Handles the graphical engine, window management, and CRT effects.
*   `interfaces_gui/`: Contains the logic for different game phases (Menu, Exploration, Combat).
*   `personnages/`: Core classes for Heroes and Monsters.
*   `assets/`: Images and sound resources.
*   `Old_Console_version/`: The original text-based console version of the game.

## License

Copyright (c) 2025 YokAiSanGil. All Rights Reserved.

This project is proprietary. Unauthorized copying, modification, distribution, or use of this software, via any medium, is strictly prohibited.

---
*Developed by YokAiSanGil*
