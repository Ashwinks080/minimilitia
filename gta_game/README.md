# GTA-like Game 🎮

A top-down action game inspired by Grand Theft Auto, built with Pygame. Features vehicles, missions, and open-world gameplay!

## Features

### 🚗 Vehicles
- **Car** - Balanced speed and acceleration
- **Truck** - Slow but heavy, good for plowing through
- **Motorcycle** - Fast and nimble
- **Police Car** - Spawned as AI

### 🎯 Mission System
- **8 Different Missions**:
  - Delivery missions
  - Robbery missions
  - Chase missions
  - Destruction missions
- **Objectives** system
- **Time limits** and rewards
- **Money and XP** progression

### 🗺️ Game World
- **Dynamic Map** with buildings and roads
- **AI Vehicles** patrolling the map
- **Collision System** for vehicles
- **Open World** exploration

### 🎨 Graphics & UI
- **Top-down view** with smooth camera
- **HUD** with player stats
- **Mission Markers** showing objectives
- **Vehicle Info** display
- **Mission Menu** for selecting objectives

## Installation

### Requirements
- Python 3.7+
- Pygame 2.1.3

### Setup
```bash
cd C:\Users\akoothup\gta_game
pip install -r requirements.txt
```

## How to Play

### Controls

| Key | Action |
|-----|--------|
| **W/A/S/D** | Move character / Drive vehicle |
| **E** | Enter/Exit vehicle |
| **Mouse** | Aim vehicle (when driving) |
| **M** | Open missions menu |
| **ESC** | Pause/Menu |
| **ENTER** | Accept mission |

### Game Loop

1. **Explore** the open world
2. **Press M** to open missions
3. **Select** a mission
4. **Complete** the objectives
5. **Earn** money and rewards
6. **Repeat!**

## Game Mechanics

### Player Movement
- Walk around the map freely
- Enter nearby vehicles with E
- Exit vehicles with E again

### Vehicle Driving
- Use WASD to accelerate in different directions
- Mouse controls steering direction
- Vehicles have health and fuel
- Physics-based movement with friction

### Missions
- **Delivery**: Reach specified location
- **Robbery**: Navigate to target location
- **Chase**: Catch the suspect
- **Destruction**: Destroy multiple targets

## File Structure

```
gta_game/
├── game.py              # Main game loop
├── game_world.py        # Game world, vehicles, physics
├── mission_system.py    # Missions and objectives
├── ui_system.py         # HUD and menus
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Game Classes

### game_world.py
- **Vector2** - 2D vector math
- **Vehicle** - Vehicle physics and rendering
- **Player** - Player character
- **GameWorld** - World management

### mission_system.py
- **Mission** - Mission structure
- **Objective** - Mission objectives
- **MissionManager** - Mission management

### ui_system.py
- **HUD** - Head-up display
- **MissionMenu** - Mission selection screen

### game.py
- **GTAGame** - Main game class
- **GameState** - Game state enum

## Gameplay Tips

1. **Money** is earned by completing missions
2. **Vehicles** offer faster transportation
3. **Different vehicles** have different speed/handling
4. **Fuel** depletes as you drive
5. **Health** decreases if you crash into buildings
6. **Time limits** on missions keep things challenging

## Future Enhancements

- [ ] Weapons system (shooting, guns)
- [ ] Multiplayer support
- [ ] More vehicle types
- [ ] Police AI and wanted system
- [ ] Pedestrians on streets
- [ ] Shops and item buying
- [ ] Difficulty levels
- [ ] Achievements system
- [ ] Sound effects and music
- [ ] More detailed maps
- [ ] Interior locations
- [ ] Gang wars and territories
- [ ] Save/Load system

## Performance

- **FPS**: 60 (capped)
- **Resolution**: 1600x900
- **Map Size**: 1600x900 pixels
- **Max Vehicles**: 5 AI + player
- **Optimized**: Simple collision, efficient rendering

## Controls Summary

```
Movement:
  W - Forward
  A - Left  
  S - Backward
  D - Right
  E - Enter/Exit Vehicle

Game:
  M - Missions Menu
  ESC - Pause/Back
  ENTER - Confirm Selection

Vehicle:
  WASD - Directional acceleration
  Mouse - Steering direction
```

## Known Issues

- Vehicles can get stuck on corners (can be fixed with physics)
- No collision between vehicles (planned feature)
- AI vehicles have simple behavior (planned enhancement)

## Customization

### Add More Vehicles
Edit `game_world.py` and add to `VehicleType` enum and `Vehicle.__init__()`.

### Add More Missions
Edit `mission_system.py` and add to `_generate_missions()` in `MissionManager`.

### Change World Size
Edit `game.py` - change `width=1600, height=900` parameters.

### Adjust Vehicle Speed
Edit `game_world.py` - modify `max_speed` and `acceleration_rate` in `Vehicle.__init__()`.

## Troubleshooting

### Game won't start
```bash
python -m py_compile game.py
```

### Pygame not found
```bash
pip install pygame==2.1.3
```

### Slow performance
- Reduce number of AI vehicles in `GameWorld._generate_world()`
- Lower FPS cap in `GTAGame.fps` (default 60)

### Controls not responding
- Make sure game window is focused
- Check keyboard layout

## Credits

Built with Pygame and Python 3
Inspired by Grand Theft Auto series

## License

MIT License - Feel free to use and modify!

---

**Enjoy the game! 🎮🚗**
