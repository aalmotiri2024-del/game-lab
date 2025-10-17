# Text Adventure Game

A Python-based interactive text adventure game where players navigate through a university building by choosing directional exits from various rooms. The game features robust input processing, room management, and a menu-driven interface.

## Features

- Navigate through 5 interconnected rooms (Reception, Admin office, Tutor's office, Parking lot, General office)
- Flexible input handling that accepts commands with punctuation and mixed case (e.g., "South!", "EAST??")
- Interactive menu system with validated exit choices
- Clean game loop with room descriptions and navigation prompts
- Comprehensive doctest coverage for quality assurance

## How to Play

```bash
python game.py
```

Choose directions by typing compass directions (north, south, east, west) at each prompt to explore the building.

## Project Structure

- `game.py` - Core game logic with functions for input processing, display, navigation, and the main game loop
- `map.py` - Game world definition with room layouts and exit configurations

## Technology

- Python 3
- Doctest for automated testing

## Additional Features

For extended gameplay features including inventory management, item collection, and puzzle solving, see the **lab6** branch.
