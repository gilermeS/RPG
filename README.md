# RPG Text Adventure Game

A text-based RPG adventure game built with Python that features dynamic storytelling and state management.

> **⚠️ Work in Progress**  
> This project is currently under development. Please note that response times may be slow as the game uses local language model processing for narrative generation.

## Description

This is an interactive text-based RPG game where players can explore a fantasy world through text commands. The game features:

- Dynamic narrative generation
- State management with save/load functionality
- Rich text interface with typing effects
- Health and inventory system
- Persistent game state

## Features

- **Interactive Storytelling**: The game generates dynamic narratives based on player actions
- **State Management**: Save and load game progress automatically
- **Rich Text Interface**: Beautiful console output with typing effects
- **Health System**: Track your character's health with a visual health bar
- **Inventory System**: Manage your items and equipment
- **Command System**: Simple text-based commands for player actions

## Requirements

- Python 3.x
- Required packages:
  - rich
  - pathlib
  - json

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gilermeS/RPG.git
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the game using:
```bash
python main.py
```

### Game Commands

- Type your actions as text commands
- Type 'quit' to exit the game
- Type 'reset' to start a new game

## Project Structure

```
RPG/
├── main.py              # Main game logic
├── utils/
│   └── api_utils.py     # Utility functions for narrative generation
├── .streamlit/          # Streamlit configuration
└── game_state.json      # Game save file
```

## Author

Guilherme de Souza Ramos Cardoso

## License

MIT License

## Contributing

Feel free to submit issues and enhancement requests! 