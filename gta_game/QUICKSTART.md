# GTA-like Game - Quick Start Guide

## Installation

1. **Install Python 3.7+** from python.org

2. **Install Pygame**:
```bash
cd C:\Users\akoothup\gta_game
pip install -r requirements.txt
```

3. **Run the game**:
```bash
python game.py
```

## Your First Mission

1. **Start the game** - You'll see the game world
2. **Press M** to open the Missions menu
3. **Use UP/DOWN** arrows to select a mission
4. **Press ENTER** to start the mission
5. **Follow the markers** on your map
6. **Complete objectives** to finish the mission

## Basic Controls

### Walking Around
- **W/A/S/D** - Move
- **E** - Enter nearby vehicle
- **M** - Open missions menu
- **ESC** - Pause

### Driving
- **W/A/S/D** - Drive in directions
- **Mouse** - Aim/steer direction
- **E** - Exit vehicle
- **ESC** - Pause

## Mission Types

### 🚗 Delivery
- Drive to the location
- Simple and fast money
- Reward: $500-750

### 💰 Robbery
- Navigate to target
- Grab the loot!
- Reward: $1000-2000

### 🏃 Chase
- Find and catch the suspect
- Use vehicles for speed
- Reward: $800-1200

### 💥 Destruction
- Destroy multiple targets
- Action-packed gameplay
- Reward: $600-1500

## Tips & Tricks

1. **Use Motorcycles** for fast deliveries
2. **Trucks are slow** but good for ramming
3. **Police cars** are police AI - avoid them!
4. **Fuel depletes** while driving - watch your fuel gauge
5. **Vehicle health** matters - avoid obstacles
6. **Earn money** by completing missions
7. **Complete more missions** to level up

## Game Features

✓ 5 AI vehicles on the map
✓ 4 vehicle types
✓ 8 different missions
✓ Dynamic missions
✓ Real-time physics
✓ Smooth camera follow
✓ HUD with stats

## Customization

### Want more/fewer missions?
Edit `mission_system.py` - modify `_generate_missions()`

### Want faster vehicles?
Edit `game_world.py` - increase `max_speed` in Vehicle class

### Want bigger map?
Edit `game.py` - change width/height in GTAGame init

### Want more vehicles?
Edit `game_world.py` - add more entries to vehicle_positions

## File Guide

- **game.py** - Main game, start here!
- **game_world.py** - All game objects
- **mission_system.py** - Mission logic
- **ui_system.py** - Menus and HUD
- **graphics.py** - Visual effects
- **requirements.txt** - Install dependencies

## Troubleshooting

### "ModuleNotFoundError: No module named pygame"
```bash
pip install pygame==2.1.3
```

### Game runs slow
- Reduce vehicles or FPS
- Close other apps

### Can't see the mission marker
- Make sure mission is started (press M)
- Check your map position

### Vehicle won't move
- Make sure fuel > 0
- Try pressing W multiple times
- Check health isn't 0

## Next Steps

1. Complete all 8 missions
2. Explore the entire map
3. Try different vehicles
4. Read the code and modify it!

## Have Fun! 🎮

This is your game - modify, expand, and enjoy!

For more details, see README.md
