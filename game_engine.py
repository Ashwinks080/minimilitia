"""
Game Engine - Handles game logic, physics, and rendering
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum


class GameMode(Enum):
    DEATHMATCH = "deathmatch"
    TEAM_DEATHMATCH = "team_deathmatch"
    CAPTURE_FLAG = "capture_flag"


@dataclass
class Vector2:
    """2D Vector for physics calculations"""
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)
    
    def distance_to(self, other):
        return (self - other).magnitude()


@dataclass
class Projectile:
    """Bullet/Projectile in the game"""
    id: str
    position: Vector2
    velocity: Vector2
    owner_id: str
    damage: int
    lifetime: float
    created_time: float
    
    def update(self, delta_time: float):
        """Update projectile position"""
        self.position = self.position + (self.velocity * delta_time)
        self.lifetime -= delta_time


class GamePhysics:
    """Physics engine for the game"""
    
    GRAVITY = 500  # pixels/second^2
    FRICTION = 0.95
    MAX_VELOCITY = 300
    
    @staticmethod
    def apply_gravity(velocity: Vector2, delta_time: float) -> Vector2:
        """Apply gravity to velocity"""
        velocity.y += GamePhysics.GRAVITY * delta_time
        
        # Cap velocity
        mag = velocity.magnitude()
        if mag > GamePhysics.MAX_VELOCITY:
            velocity = velocity.normalize() * GamePhysics.MAX_VELOCITY
        
        return velocity
    
    @staticmethod
    def apply_friction(velocity: Vector2) -> Vector2:
        """Apply friction to velocity"""
        return velocity * GamePhysics.FRICTION
    
    @staticmethod
    def check_collision(pos1: Vector2, radius1: float, pos2: Vector2, radius2: float) -> bool:
        """Check circle collision"""
        distance = pos1.distance_to(pos2)
        return distance < (radius1 + radius2)


class GameMap:
    """Game map with platforms and obstacles"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.platforms: List[Tuple[Vector2, float, float]] = []
        self.obstacles: List[Tuple[Vector2, float]] = []
        self._generate_default_map()
    
    def _generate_default_map(self):
        """Generate a default map layout"""
        # Ground platform
        self.platforms.append((Vector2(self.width / 2, self.height - 20), self.width, 40))
        
        # Floating platforms
        self.platforms.append((Vector2(self.width / 4, self.height - 150), 150, 20))
        self.platforms.append((Vector2(3 * self.width / 4, self.height - 150), 150, 20))
        self.platforms.append((Vector2(self.width / 2, self.height - 300), 200, 20))
        
        # Obstacles
        self.obstacles.append((Vector2(self.width / 3, self.height - 250), 30))
        self.obstacles.append((Vector2(2 * self.width / 3, self.height - 250), 30))
    
    def is_on_platform(self, position: Vector2, player_radius: float) -> bool:
        """Check if player is on a platform"""
        for platform_pos, platform_width, platform_height in self.platforms:
            if (abs(position.x - platform_pos.x) < platform_width / 2 and
                abs(position.y - platform_pos.y) < platform_height / 2):
                return True
        return False


class GameEngine:
    """Main game engine"""
    
    def __init__(self, map_width: int = 1280, map_height: int = 720, game_mode: GameMode = GameMode.TEAM_DEATHMATCH):
        self.map_width = map_width
        self.map_height = map_height
        self.game_mode = game_mode
        self.game_map = GameMap(map_width, map_height)
        
        self.players = {}
        self.projectiles: List[Projectile] = []
        self.game_time = 0
        self.max_game_time = 600  # 10 minutes
        
    def update(self, delta_time: float):
        """Update game state"""
        self.game_time += delta_time
        self._update_projectiles(delta_time)
        self._check_collisions()
    
    def _update_projectiles(self, delta_time: float):
        """Update all projectiles"""
        projectiles_to_remove = []
        
        for projectile in self.projectiles:
            projectile.update(delta_time)
            
            if projectile.lifetime <= 0:
                projectiles_to_remove.append(projectile)
            
            if (projectile.position.x < 0 or projectile.position.x > self.map_width or
                projectile.position.y < 0 or projectile.position.y > self.map_height):
                projectiles_to_remove.append(projectile)
        
        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)
    
    def _check_collisions(self):
        """Check for collisions between projectiles and players"""
        for projectile in list(self.projectiles):
            for player_id, player in self.players.items():
                if player_id == projectile.owner_id:
                    continue
                
                if GamePhysics.check_collision(
                    projectile.position, 5,
                    Vector2(player.x, player.y), 15
                ):
                    player.health -= projectile.damage
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    break
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        if self.game_time >= self.max_game_time:
            return True
        
        if self.game_mode == GameMode.TEAM_DEATHMATCH:
            teams_alive = set()
            for player in self.players.values():
                if player.is_alive:
                    teams_alive.add(player.team)
            
            return len(teams_alive) <= 1
        
        return False
