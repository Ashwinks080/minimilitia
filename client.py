import socket
import threading
import json
import time
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, Optional, Callable
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


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


@dataclass
class GameMessage:
    """Message structure for network communication"""
    msg_type: str
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


class GameClient:
    """Game client for multiplayer connectivity"""
    
    def __init__(self, server_host: str, server_port: int, player_name: str = "Player"):
        self.server_host = server_host
        self.server_port = server_port
        self.player_name = player_name
        self.player_id = str(uuid.uuid4())[:8]
        
        self.socket = None
        self.connected = False
        self.running = False
        
        self.local_player: Optional[Player] = None
        self.remote_players: Dict[str, Player] = {}
        
        self.on_player_joined: Optional[Callable] = None
        self.on_player_left: Optional[Callable] = None
        self.on_player_updated: Optional[Callable] = None
        self.on_game_started: Optional[Callable] = None
        self.on_game_state: Optional[Callable] = None
        self.on_shoot: Optional[Callable] = None
        
    def connect(self) -> bool:
        """Connect to the game server"""
        try:
            logger.info(f"Attempting to connect to {self.server_host}:{self.server_port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.server_host, self.server_port))
            self.socket.settimeout(None)
            self.connected = True
            self.running = True
            
            logger.info(f"Connected to server at {self.server_host}:{self.server_port}")
            
            receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
            receive_thread.start()
            
            self._send_join_message()
            
            return True
        except socket.timeout:
            logger.error(f"Connection timeout: Server not responding at {self.server_host}:{self.server_port}")
            self.connected = False
            return False
        except ConnectionRefusedError:
            logger.error(f"Connection refused: No server running at {self.server_host}:{self.server_port}")
            self.connected = False
            return False
        except Exception as e:
            logger.error(f"Failed to connect to server: {e}")
            self.connected = False
            return False
    
    def _send_join_message(self):
        """Send join message to server"""
        message = GameMessage(
            msg_type="join",
            player_id=self.player_id,
            data={"name": self.player_name},
            timestamp=time.time()
        )
        self._send_message(message)
        logger.info(f"Sent join request as {self.player_name}")
    
    def _receive_messages(self):
        """Receive and process messages from server"""
        buffer = ""
        
        while self.running and self.connected:
            try:
                data = self.socket.recv(4096).decode("utf-8")
                
                if not data:
                    logger.warning("Connection closed by server")
                    self.connected = False
                    break
                
                buffer += data
                
                while buffer:
                    try:
                        if not buffer.startswith("{"):
                            buffer = buffer.lstrip()
                            if not buffer or not buffer.startswith("{"):
                                break
                        
                        brace_count = 0
                        end_idx = -1
                        for i, char in enumerate(buffer):
                            if char == "{":
                                brace_count += 1
                            elif char == "}":
                                brace_count -= 1
                                if brace_count == 0:
                                    end_idx = i + 1
                                    break
                        
                        if end_idx == -1:
                            break
                        
                        message_str = buffer[:end_idx]
                        buffer = buffer[end_idx:]
                        
                        try:
                            message = GameMessage.from_json(message_str)
                            self._process_message(message)
                        except json.JSONDecodeError as je:
                            logger.error(f"Failed to parse JSON: {je}")
                            
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        buffer = ""
                        break
                        
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                self.connected = False
                break
    
    def _process_message(self, message: GameMessage):
        """Process received message"""
        msg_type = message.msg_type
        
        if msg_type == "join_response":
            self._handle_join_response(message)
        elif msg_type == "player_joined":
            self._handle_player_joined(message)
        elif msg_type == "player_left":
            self._handle_player_left(message)
        elif msg_type == "player_update":
            self._handle_player_update(message)
        elif msg_type == "game_started":
            self._handle_game_started(message)
        elif msg_type == "game_state":
            self._handle_game_state(message)
        elif msg_type == "shoot":
            self._handle_shoot(message)
    
    def _handle_join_response(self, message: GameMessage):
        """Handle join response from server"""
        if message.data.get("success"):
            player_data = message.data.get("player")
            self.local_player = Player(**player_data)
            
            for player_data in message.data.get("all_players", []):
                if player_data["id"] != self.player_id:
                    player = Player(**player_data)
                    self.remote_players[player.id] = player
            
            logger.info(f"Successfully joined game as {self.local_player.name} (Team {self.local_player.team})")
        else:
            logger.error(f"Failed to join: {message.data.get('reason')}")
            self.connected = False
    
    def _handle_player_joined(self, message: GameMessage):
        """Handle new player joining"""
        player_data = message.data.get("player")
        player = Player(**player_data)
        self.remote_players[player.id] = player
        
        logger.info(f"Player {player.name} joined (Team {player.team})")
        if self.on_player_joined:
            self.on_player_joined(player)
    
    def _handle_player_left(self, message: GameMessage):
        """Handle player leaving"""
        player_id = message.data.get("player_id")
        if player_id in self.remote_players:
            player = self.remote_players.pop(player_id)
            logger.info(f"Player {player.name} left")
            if self.on_player_left:
                self.on_player_left(player)
    
    def _handle_player_update(self, message: GameMessage):
        """Handle player position/state update"""
        player_id = message.player_id
        if player_id in self.remote_players:
            player = self.remote_players[player_id]
            player.x = message.data.get("x", player.x)
            player.y = message.data.get("y", player.y)
            player.health = message.data.get("health", player.health)
            player.ammo = message.data.get("ammo", player.ammo)
            
            if self.on_player_updated:
                self.on_player_updated(player)
    
    def _handle_game_started(self, message: GameMessage):
        """Handle game start"""
        logger.info("Game started!")
        if self.on_game_started:
            self.on_game_started()
    
    def _handle_game_state(self, message: GameMessage):
        """Handle game state update"""
        players_data = message.data.get("players", [])
        
        for player_data in players_data:
            if player_data["id"] != self.player_id:
                if player_data["id"] in self.remote_players:
                    player = self.remote_players[player_data["id"]]
                    player.x = player_data["x"]
                    player.y = player_data["y"]
                    player.health = player_data["health"]
                    player.ammo = player_data["ammo"]
                    player.is_alive = player_data["is_alive"]
                    player.score = player_data["score"]
            else:
                if self.local_player:
                    self.local_player.x = player_data["x"]
                    self.local_player.y = player_data["y"]
                    self.local_player.health = player_data["health"]
                    self.local_player.ammo = player_data["ammo"]
                    self.local_player.is_alive = player_data["is_alive"]
                    self.local_player.score = player_data["score"]
        
        if self.on_game_state:
            self.on_game_state(message.data)
    
    def _handle_shoot(self, message: GameMessage):
        """Handle shoot event"""
        if self.on_shoot:
            self.on_shoot(message.data)
    
    def update_player_position(self, x: float, y: float):
        """Update local player position"""
        if not self.connected or not self.local_player:
            return
        
        self.local_player.x = x
        self.local_player.y = y
        
        message = GameMessage(
            msg_type="player_update",
            player_id=self.player_id,
            data={"x": x, "y": y},
            timestamp=time.time()
        )
        self._send_message(message)
    
    def update_player_health(self, health: int):
        """Update local player health"""
        if not self.connected or not self.local_player:
            return
        
        self.local_player.health = health
        
        message = GameMessage(
            msg_type="player_update",
            player_id=self.player_id,
            data={"health": health},
            timestamp=time.time()
        )
        self._send_message(message)
    
    def update_player_ammo(self, ammo: int):
        """Update local player ammo"""
        if not self.connected or not self.local_player:
            return
        
        self.local_player.ammo = ammo
        
        message = GameMessage(
            msg_type="player_update",
            player_id=self.player_id,
            data={"ammo": ammo},
            timestamp=time.time()
        )
        self._send_message(message)
    
    def shoot(self, target_id: str, damage: int = 10):
        """Send shoot event"""
        if not self.connected:
            return
        
        message = GameMessage(
            msg_type="shoot",
            player_id=self.player_id,
            data={"target_id": target_id, "damage": damage},
            timestamp=time.time()
        )
        self._send_message(message)
    
    def _send_message(self, message: GameMessage):
        """Send message to server"""
        try:
            self.socket.send(message.to_json().encode("utf-8"))
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.connected = False
    
    def disconnect(self):
        """Disconnect from server"""
        if self.connected:
            message = GameMessage(
                msg_type="leave",
                player_id=self.player_id,
                data={},
                timestamp=time.time()
            )
            self._send_message(message)
        
        self.running = False
        self.connected = False
        
        if self.socket:
            self.socket.close()
        
        logger.info("Disconnected from server")
    
    def get_all_players(self) -> list:
        """Get all players (local + remote)"""
        players = []
        if self.local_player:
            players.append(self.local_player)
        players.extend(self.remote_players.values())
        return players
    
    def get_remote_players(self) -> list:
        """Get only remote players"""
        return list(self.remote_players.values())
