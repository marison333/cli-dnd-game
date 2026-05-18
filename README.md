# py-dnd-game

A small, text-based Dungeons & Dragons inspired game engine in Python.

Quick start

- Prerequisites: Python 3.8+ (3.10 recommended)
- Run the game: `python3 src/main.py`
- Run tests: `pytest`

Project layout
```
.
├── assets
├── docs
└── src
    ├── core                # main game loops
    ├── create_player.py    # function for creating the player
    ├── entities            # classes for player and monsters
    ├── main.py             # ties everything together
    ├── story_navigators.py # runs through the story
    ├── story.json          # story library
    ├── tests               # ensures the code quality is and stay high
    └── utils.py            # hellpers and utility functions
```
