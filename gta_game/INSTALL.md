# INSTALLATION & SETUP GUIDE

## Complete Installation Steps

### 1. Verify Python Installation

Open Command Prompt and type:
```bash
python --version
```

Should show Python 3.7 or higher. If not, download from python.org

### 2. Navigate to Game Directory

```bash
cd C:\Users\akoothup\gta_game
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Pygame 2.1.3
- NumPy 1.21.0

### 4. Run the Game

```bash
python game.py
```

## What You Get

A fully playable GTA-like game with:
- ✓ 4 Vehicle types
- ✓ 8 Different missions
- ✓ Open world exploration
- ✓ Physics-based driving
- ✓ HUD and UI
- ✓ Mission system
- ✓ Money and rewards
- ✓ Particle effects

## Minimum Requirements

- Python 3.7+
- Pygame 2.1.3
- 500MB disk space
- 2GB RAM
- Dual-core processor

## Recommended Requirements

- Python 3.9+
- Windows 10/11
- 1GB RAM
- Quad-core processor
- Dedicated GPU

## Troubleshooting

### Python not recognized
- Add Python to PATH in Windows
- Restart Command Prompt after installation

### pygame not found
```bash
pip install --upgrade pip
pip install pygame==2.1.3 --force-reinstall
```

### Game won't start
```bash
python -c "import pygame; print(pygame.ver)"
```

If error, reinstall pygame.

### Game runs slowly
- Close other applications
- Reduce number of AI vehicles (edit game_world.py)
- Lower resolution (edit game.py)

## Quick Start

1. Open Command Prompt
2. `cd C:\Users\akoothup\gta_game`
3. `python game.py`
4. Press M to open missions
5. Play!

## File Locations

Main game: `C:\Users\akoothup\gta_game\game.py`
Config: Edit files as needed
Save data: None currently (future feature)

## Performance Tips

1. Close unnecessary programs
2. Use dedicated GPU if available
3. Update graphics drivers
4. Disable Windows transparency effects
5. Run as administrator (optional)

## Uninstallation

Simply delete the folder: `C:\Users\akoothup\gta_game\`

To remove Pygame:
```bash
pip uninstall pygame
```

## Getting Help

1. Check README.md for full documentation
2. Check QUICKSTART.md for basic controls
3. Read PROJECT_SUMMARY.txt for features
4. Check code comments for details

## Next Steps After Installation

1. **Play the game**:
   - Complete all 8 missions
   - Explore the entire map
   - Try different vehicles

2. **Customize the game**:
   - Add new missions
   - Add new vehicles
   - Change map size
   - Adjust difficulty

3. **Learn the code**:
   - Read game.py to understand main loop
   - Read game_world.py for physics
   - Read mission_system.py for missions
   - Read ui_system.py for UI

4. **Expand the game**:
   - Add multiplayer
   - Add weapons system
   - Add NPC pedestrians
   - Add police chase system

## Enjoy! 🎮

Your GTA-like game is ready to play!
