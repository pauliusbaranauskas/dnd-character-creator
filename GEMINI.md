We are building an application using Python and PyQt6. This application will be used to create characters for a D&D game. The application will have a simple interface with buttons and text fields. The user will be able to create a character by selecting a class, race, and stats. The user will also be able to save the character to a file and load it later. The application will use the data from the data.py file to create characters.
After creating a character the user will be able to level up the character. This should be done through a series of prompts that will ask the user what they want to do. For example, the user might want to increase a stat, or learn a new skill. These updates should be tracked in the character data and displayed in the review screen and undoable.
Application should be able to run on any operating system.

## Implementation Remarks
- **UI Structure:** Class and Race selection are separated into two distinct screens to provide ample space for detailed descriptions and feature lists.
- **Dynamic Data Display:** The UI must dynamically display detailed information such as hit dice, primary abilities, saving throws, racial traits, and ability score bonuses directly from `data.py` upon selection.
- **Data Source of Truth:** `data.py` is the primary source of truth for all game-related definitions. Any additions to classes or races should follow the established schema to maintain UI compatibility.
- **Responsive Layouts:** Given the varying length of class features and racial descriptions, UI labels should support word-wrap and sufficient minimum heights, or be contained within scrollable areas where necessary.
- **Environment Setup:** Standard setup instructions for virtual environments on macOS/Linux are documented in `README.md`.