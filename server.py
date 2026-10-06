"""
Multiplayer Game Server
Handles game state, player management, and network communication
"""

import socket
import threading
import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameState(Enum):
    WAITING = "waiting"
    RUNNING = "running"
    PAUSED = "paused"
    ENDED = "ended"


@dataclass
class Player:
    """Player data structure"""
    id: str
    name: str
    x: float
    y: float
    health: int
    ammo: int
    team: int
    is_alive: bool
    score: int
    
    def to_dict(self):
        return asdict(self)


@dataclass
class GameMessage:
    """Message structure for network communication"""
    msg_type: str  # "player_update", "shoot", "join", "leave", "game_state"
    player_id: str
    data: dict
    timestamp: float
    
    def to_json(self):
        return json.dumps({
            "msg_type": self.msg_type,
            "player_id": self.player_id,
            "data": self.data,
            "timestamp": self.timestamp
        })
    
    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return GameMessage(
            msg_type=data["msg_type"],
            player_id=data["player_id"],
            data=data["data"],
            timestamp=data["timestamp"]
        )


class GameServer:
    """Main game server handling multiplayer logic"""
    
    def __init__(self, host="0.0.0.0", port=5000, max_players=6):
        self.host = host
        self.port = port
        self.max_players = max_players
        self.players: Dict[str, Player] = {}
        self.client_sockets: Dict[str, socket.socket] = {}
        self.game_state = GameState.WAITING
        self.server_socket = None
        self.running = False
        self.lock = threading.Lock()
        self.game_start_time = None
        
    def start(self):
        """Start the game server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_players)
        self.running = True
        
        logger.info(f"Game Server started on {self.host}:{self.port}")
        
        # Start accepting connections
        accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
        accept_thread.start()
        
        # Start game loop
        game_thread = threading.Thread(target=self._game_loop, daemon=True)
        game_thread.start()
        
    def _accept_connections(self):
        """Accept incoming client connections"""
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                logger.info(f"New connection from {client_address}")
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
            except Exception as e:
                logger.error(f"Error accepting connection: {e}")
    
    def _handle_client(self, client_socket: socket.socket, client_address):
        """Handle individual client connection"""
        player_id = None
        
        try:
            while self.running:
                data = client_socket.recv(4096).decode('utf-8')
                
                if not data:
                    break
                
                try:
                    message = GameMessage.from_json(data)
                    player_id = message.player_id
                    
                    # Route message based on type
                    if message.msg_type == "join":
                        self._handle_player_join(message, client_socket)
                    elif message.msg_type == "player_update":
                        self._handle_player_update(message)
                    elif message.msg_type == "shoot":
                        self._handle_shoot(message)
                    elif message.msg_type == "leave":
                        self._handle_player_leave(message)
                    
                except json.JSONDecodeError:
                    logger.error("Invalid JSON received")
                    
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            if player_id and player_id in self.players:
                self._handle_player_leave(GameMessage(
                    msg_type="leave",
                    player_id=player_id,
                    data={},
                    timestamp=time.time()
                ))
            client_socket.close()
    
    def _handle_player_join(self, message: GameMessage, client_socket: socket.socket):
        """Handle player joining the game"""
        with self.lock:
            if len(self.players) >= self.max_players:
                response = GameMessage(
                    msg_type="join_response",
                    player_id="server",
                    data={"success": False, "reason": "Server full"},
                    timestamp=time.time()
                )
                client_socket.send(response.to_json().encode('utf-8'))
                return
            
            player_id = message.player_id
            player_name = message.data.get("name", f"Player_{player_id}")
            team = len(self.players) % 2  # Alternate teams
            
            player = Player(
                id=player_id,
                name=player_name,
                x=100 + len(self.players) * 50,
                y=100,
                health=100,
                ammo=30,
                team=team,
                is_alive=True,
                score=0
            )
            
            self.players[player_id] = player
            self.client_sockets[player_id] = client_socket
            
            logger.info(f"Player {player_name} joined. Total players: {len(self.players)}")
            
            # Send join confirmation
            response = GameMessage(
                msg_type="join_response",
                player_id="server",
                data={
                    "success": True,
                    "player": player.to_dict(),
                    "all_players": [p.to_dict() for p in self.players.values()]
                },
                timestamp=time.time()
            )
            client_socket.send(response.to_json().encode('utf-8'))
            
            # Broadcast new player to all clients
            self._broadcast_message(GameMessage(
                msg_type="player_joined",
                player_id="server",
                data={"player": player.to_dict()},
                timestamp=time.time()
            ), exclude_player=player_id)
            
            # Start game if we have enough players
            if len(self.players) >= 2 and self.game_state == GameState.WAITING:
                self._start_game()
    
    def _handle_player_update(self, message: GameMessage):
        """Handle player position/state update"""
        with self.lock:
            if message.player_id in self.players:
                player = self.players[message.player_id]
                player.x = message.data.get("x", player.x)
                player.y = message.data.get("y", player.y)
                player.health = message.data.get("health", player.health)
                player.ammo = message.data.get("ammo", player.ammo)
                
                # Broadcast update to all other players
                self._broadcast_message(message, exclude_player=message.player_id)
    
    def _handle_shoot(self, message: GameMessage):
        """Handle shooting event"""
        with self.lock:
            shooter_id = message.player_id
            target_id = message.data.get("target_id")
            damage = message.data.get("damage", 10)
            
            if target_id in self.players:
                target = self.players[target_id]
                target.health -= damage
                
                if target.health <= 0:
                    target.is_alive = False
                    self.players[shooter_id].score += 10
                
                # Broadcast shoot event
                self._broadcast_message(message)
    
    def _handle_player_leave(self, message: GameMessage):
        """Handle player leaving the game"""
        with self.lock:
            player_id = message.player_id
            if player_id in self.players:
                del self.players[player_id]
            if player_id in self.client_sockets:
                del self.client_sockets[player_id]
            
            logger.info(f"Player {player_id} left. Remaining players: {len(self.players)}")
            
            # Broadcast player left
            self._broadcast_message(GameMessage(
                msg_type="player_left",
                player_id="server",
                data={"player_id": player_id},
                timestamp=time.time()
            ))
    
    def _start_game(self):
        """Start the game"""
        with self.lock:
            self.game_state = GameState.RUNNING
            self.game_start_time = time.time()
            logger.info("Game started!")
            
            self._broadcast_message(GameMessage(
                msg_type="game_started",
                player_id="server",
                data={"players": [p.to_dict() for p in self.players.values()]},
                timestamp=time.time()
            ))
    
    def _game_loop(self):
        """Main game loop - sends periodic state updates"""
        while self.running:
            if self.game_state == GameState.RUNNING:
                with self.lock:
                    # Send game state to all players
                    game_state_msg = GameMessage(
                        msg_type="game_state",
                        player_id="server",
                        data={
                            "players": [p.to_dict() for p in self.players.values()],
                            "game_state": self.game_state.value,
                            "elapsed_time": time.time() - self.game_start_time
                        },
                        timestamp=time.time()
                    )
                    self._broadcast_message(game_state_msg)
            
            time.sleep(0.05)  # 20 updates per second
    
    def _broadcast_message(self, message: GameMessage, exclude_player: Optional[str] = None):
        """Broadcast message to all connected clients"""
        msg_json = message.to_json().encode('utf-8')
        
        for player_id, client_socket in list(self.client_sockets.items()):
            if exclude_player and player_id == exclude_player:
                continue
            
            try:
                client_socket.send(msg_json)
            except Exception as e:
                logger.error(f"Error sending to {player_id}: {e}")
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        logger.info("Server stopped")


if __name__ == "__main__":
    server = GameServer(host="0.0.0.0", port=5000, max_players=6)
    server.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
