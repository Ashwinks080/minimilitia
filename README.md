# Mini Militia - Multiplayer Game

A networked multiplayer game similar to Mini Militia with support for 4-6 players connected via WiFi.

## Features

- **Multiplayer Support**: Connect up to 6 players on the same WiFi network
- **Team-based Gameplay**: Automatic team assignment (Team 1 vs Team 2)
- **Real-time Synchronization**: Player positions, health, ammo, and scores synced across all clients
- **Physics Engine**: Gravity, collision detection, and projectile physics
- **Game Map**: Multiple platforms and obstacles for strategic gameplay
- **Score Tracking**: Real-time score updates and player statistics

## Architecture

### Components

1. **server.py** - Game server handling:
   - Player connection management
   - Game state synchronization
   - Message routing between clients
   - Game logic coordination

2. **client.py** - Game client handling:
   - Network communication with server
   - Local game state management
   - Event callbacks for game updates

3. **game_engine.py** - Game logic including:
   - Physics simulation (gravity, collision, friction)
   - Projectile management
   - Map layout and collision detection
   - Game mode logic

4. **pygame_client.py** - Graphics and input handling:
   - Pygame-based rendering
   - Player input processing
   - HUD display
   - Game menu

## Installation

### Requirements
- Python 3.7+
- Pygame 2.1.3

### Setup

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the Game

### Start the Server

```bash
python server.py
```

The server will start on `0.0.0.0:5000` and wait for clients to connect.

### Start Clients

On each device connected to the same WiFi network:

```bash
# Find the server's IP address first
python pygame_client.py <SERVER_IP> 5000 <PLAYER_NAME>
```

Example:
```bash
python pygame_client.py 192.168.1.100 5000 "Player1"
```

## Network Communication

### Message Types

- **join**: Player joins the game
- **join_response**: Server confirms join
- **player_update**: Player position/state update
- **player_joined**: Broadcast when new player joins
- **player_left**: Broadcast when player leaves
- **shoot**: Shooting event
- **game_started**: Game has started
- **game_state**: Periodic game state update

### Message Format

```json
{
  "msg_type": "player_update",
  "player_id": "abc123",
  "data": {
    "x": 640,
    "y": 360,
    "health": 85,
    "ammo": 25
  },
  "timestamp": 1234567890.123
}
```

## Game Controls

- **A/D**: Move left/right
- **SPACE**: Jump
- **Left Click**: Shoot nearest enemy
- **ESC**: Quit game

## Game Mechanics

### Player Stats
- **Health**: 100 HP (dies at 0)
- **Ammo**: 30 rounds per magazine
- **Score**: Points earned by eliminating enemies

### Teams
- **Team 1** (Red): Players 1, 3, 5
- **Team 2** (Blue): Players 2, 4, 6

### Gameplay
- Game starts when 2+ players are connected
- Team Deathmatch mode: Eliminate all enemy team members
- Game ends when only one team has alive players or time runs out
- Scores are tracked and displayed in real-time

## Network Architecture

```
┌─────────────┐
│   Server    │
│  (5000)     │
└──────┬──────┘
       │
   ┌───┼───┬───┬───┐
   │   │   │   │   │
┌──▼─┐ │ ┌─▼─┐ │ ┌─▼─┐
│ C1 │ │ │ C2│ │ │ C3│
└────┘ │ └───┘ │ └───┘
       │       │
    ┌──▼─┐  ┌──▼─┐
    │ C4 │  │ C5 │
    └────┘  └────┘
```

## Performance Considerations

- **Update Rate**: 20 updates per second from server
- **Network Protocol**: TCP sockets for reliable delivery
- **Latency**: Optimized for LAN play (< 50ms)
- **Bandwidth**: ~1-2 KB per second per player

## Future Enhancements

- [ ] UDP for lower latency
- [ ] Lag compensation and prediction
- [ ] More game modes (Capture the Flag, King of the Hill)
- [ ] Power-ups and special weapons
- [ ] Mobile client support
- [ ] Voice chat integration
- [ ] Replay system
- [ ] Leaderboards

## Troubleshooting

### Can't connect to server
- Ensure server is running: `python server.py`
- Check firewall allows port 5000
- Verify all devices are on same WiFi network
- Use correct server IP address

### Lag or stuttering
- Check WiFi signal strength
- Reduce number of players
- Close other network-intensive applications
- Try moving closer to WiFi router

### Players not syncing
- Check network connection
- Restart server and clients
- Verify no firewall blocking port 5000

## License

MIT License - Feel free to use and modify for your projects!

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
