# Quick Start Guide - Mini Militia Multiplayer

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Find Your Server IP Address

### On Windows:
```bash
ipconfig
```
Look for "IPv4 Address" under your WiFi adapter (usually 192.168.x.x)

### On Mac/Linux:
```bash
ifconfig
```

## Step 3: Start the Server

On the machine that will host the game:

```bash
python server.py
```

You should see:
```
INFO:__main__:Game Server started on 0.0.0.0:5000
```

## Step 4: Connect Clients

On each player's device (must be on same WiFi):

```bash
python pygame_client.py <SERVER_IP> 5000 "PlayerName"
```

Example:
```bash
python pygame_client.py 192.168.1.100 5000 "Player1"
```

## Step 5: Play!

- Wait for 2+ players to connect
- Game starts automatically
- Use A/D to move, SPACE to jump, Click to shoot
- Press ESC to quit

## Network Requirements

- All devices on same WiFi network
- Port 5000 must be open/not blocked by firewall
- Stable WiFi connection recommended

## Troubleshooting

**"Connection refused"**
- Check server is running
- Verify correct IP address
- Check firewall settings

**"Lag/Stuttering"**
- Move closer to WiFi router
- Reduce number of players
- Close other network apps

**"Players not moving"**
- Check network connection
- Restart server and clients
- Verify all on same WiFi

## Game Tips

- Red team vs Blue team (automatic assignment)
- Eliminate enemy team to win
- Use platforms for cover
- Aim for nearest enemy
- Collect ammo and health

Enjoy the game! 🎮
