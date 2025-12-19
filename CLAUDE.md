# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Creature Collector is a single-player gacha-style creature collecting game with turn-based battles. The game features:
- Python backend using Streamlit for the UI
- Turn-based battles with real-time skill-test events during attacks
- Pixel-art sprites for creatures
- Gacha mechanics for items (not creatures)
- Creature combination system with predictable special combinations
- Potential future features: web frontend, multiplayer battles

## Code Style (Python)

- Use pound (#) for comments instead of triple-quote
- Prefer comments on the same line as the thing they refer to, rather than on their own line
- Follow the global naming conventions:
  - snake_case for variables
  - CamelCase for class names
  - Prefix globals with g_
  - Prefix statics with s_
  - Prefix pointers with p_ (if using ctypes or similar)

## Development Commands

### Initial Setup
```bash
./setup.sh  # Creates venv, installs dependencies
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Game
```bash
source venv/bin/activate  # Activate virtual environment first
streamlit run main.py
```

## Architecture Guidance

### Core Systems to Implement

1. **Creature System**: Creature data structures, stats, abilities, and sprite management
2. **Battle System**: Turn-based combat with action selection and real-time skill events
3. **Gacha System**: Item acquisition mechanics (not for creatures)
4. **Combination System**: Creature fusion with deterministic special combinations
5. **UI Layer**: Streamlit-based interface for all game interactions

### Design Considerations

- Creatures are NOT obtained through gacha (use alternative acquisition methods)
- Battle actions should support integration with real-time skill events
- Combination system should be deterministic for special combinations
- Keep multiplayer expansion in mind but focus on single-player for now
