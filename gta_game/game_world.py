"""
GTA-like Game - Game Engine & Physics
Handles game world, physics, and logic
"""

import pygame
import math
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional


class VehicleType(Enum):
    CAR = "car"
    TRUCK = "truck"
    MOTORCYCLE = "motorcycle"
    POLICE_CAR = "police_car"


@dataclass
class Vector2:
    """2D Vector for physics"""
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)


class Vehicle:
    """Vehicle class for cars, trucks, etc"""
    
    def __init__(self, x, y, vehicle_type=VehicleType.CAR):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.rotation = 0
        self.vehicle_type = vehicle_type
        
        # Vehicle properties
        if vehicle_type == VehicleType.CAR:
            self.width = 40
            self.height = 20
            self.max_speed = 400
            self.acceleration_rate = 300
            self.friction = 0.92
            self.color = (200, 50, 50)
        elif vehicle_type == VehicleType.TRUCK:
            self.width = 60
            self.height = 30
            self.max_speed = 300
            self.acceleration_rate = 200
            self.friction = 0.90
            self.color = (150, 150, 50)
        elif vehicle_type == VehicleType.MOTORCYCLE:
            self.width = 30
            self.height = 15
            self.max_speed = 500
            self.acceleration_rate = 400
            self.friction = 0.88
            self.color = (100, 100, 100)
        else:  # POLICE_CAR
            self.width = 40
            self.height = 20
            self.max_speed = 450
            self.acceleration_rate = 350
            self.friction = 0.91
            self.color = (50, 50, 200)
        
        self.health = 100
        self.fuel = 100
        self.is_player = False
    
    def update(self, delta_time, map_width, map_height):
        """Update vehicle physics"""
        # Apply friction
        self.velocity.x *= self.friction
        self.velocity.y *= self.friction
        
        # Limit speed
        speed = self.velocity.magnitude()
        if speed > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed
        
        # Update position
        self.position = self.position + (self.velocity * delta_time)
        
        # Boundary checking
        self.position.x = max(self.width / 2, min(self.position.x, map_width - self.width / 2))
        self.position.y = max(self.height / 2, min(self.position.y, map_height - self.height / 2))
        
        # Consume fuel
        if speed > 50:
            self.fuel -= 0.05 * delta_time
            self.fuel = max(0, self.fuel)
    
    def accelerate(self, direction, delta_time):
        """Accelerate vehicle"""
        if self.fuel > 0:
            acc = direction * self.acceleration_rate
            self.velocity = self.velocity + (acc * delta_time)
    
    def steer(self, angle):
        """Steer vehicle"""
        self.rotation = angle
    
    def draw(self, surface):
        """Draw vehicle"""
        # Draw rectangle for vehicle body
        rect = pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width,
            self.height
        )
        pygame.draw.rect(surface, self.color, rect)
        
        # Draw direction indicator
        end_x = self.position.x + math.cos(self.rotation) * (self.width / 2)
        end_y = self.position.y + math.sin(self.rotation) * (self.height / 2)
        pygame.draw.line(surface, (255, 255, 255), (self.position.x, self.position.y), (end_x, end_y), 2)
        
        # Draw health bar
        health_bar_width = self.width
        health_bar_height = 3
        health_bar_x = self.position.x - health_bar_width / 2
        health_bar_y = self.position.y - self.height / 2 - 10
        
        # Background
        pygame.draw.rect(surface, (100, 100, 100), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        
        # Health
        health_width = (self.health / 100) * health_bar_width
        pygame.draw.rect(surface, (50, 255, 50), (health_bar_x, health_bar_y, health_width, health_bar_height))


class Player:
    """Player character"""
    
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.radius = 8
        self.speed = 200
        self.color = (255, 200, 100)
        self.health = 100
        self.money = 0
        self.current_vehicle: Optional[Vehicle] = None
        self.is_in_vehicle = False
    
    def update(self, delta_time, map_width, map_height):
        """Update player"""
        if not self.is_in_vehicle:
            # Player movement
            self.velocity.x *= 0.9
            self.velocity.y *= 0.9
            
            # Update position
            self.position = self.position + (self.velocity * delta_time)
            
            # Boundary checking
            self.position.x = max(self.radius, min(self.position.x, map_width - self.radius))
            self.position.y = max(self.radius, min(self.position.y, map_height - self.radius))
    
    def move(self, dx, dy):
        """Move player"""
        if not self.is_in_vehicle:
            direction = math.sqrt(dx ** 2 + dy ** 2)
            if direction > 0:
                self.velocity.x = (dx / direction) * self.speed
                self.velocity.y = (dy / direction) * self.speed
    
    def enter_vehicle(self, vehicle):
        """Enter a vehicle"""
        self.current_vehicle = vehicle
        self.is_in_vehicle = True
        self.position = vehicle.position
    
    def exit_vehicle(self):
        """Exit vehicle"""
        if self.current_vehicle:
            self.position.x = self.current_vehicle.position.x + 30
            self.position.y = self.current_vehicle.position.y
            self.current_vehicle = None
            self.is_in_vehicle = False
    
    def draw(self, surface):
        """Draw player"""
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        
        # Draw health
        health_bar_width = 20
        health_bar_height = 3
        health_bar_x = self.position.x - health_bar_width / 2
        health_bar_y = self.position.y - self.radius - 10
        
        pygame.draw.rect(surface, (100, 100, 100), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        health_width = (self.health / 100) * health_bar_width
        pygame.draw.rect(surface, (50, 255, 50), (health_bar_x, health_bar_y, health_width, health_bar_height))


class GameWorld:
    """Game world manager"""
    
    def __init__(self, width=1600, height=900):
        self.width = width
        self.height = height
        self.player = Player(width / 2, height / 2)
        self.vehicles: List[Vehicle] = []
        self.buildings: List[Tuple] = []
        self.missions: List['Mission'] = []
        self.current_mission: Optional['Mission'] = None
        
        self._generate_world()
    
    def _generate_world(self):
        """Generate game world"""
        # Add buildings
        building_positions = [
            (200, 200, 150, 150),
            (500, 150, 200, 100),
            (950, 200, 150, 200),
            (1300, 250, 150, 150),
            (200, 550, 200, 150),
            (700, 600, 150, 150),
            (1200, 650, 200, 100),
            (1450, 500, 100, 200),
        ]
        
        for pos in building_positions:
            self.buildings.append(pos)
        
        # Add AI vehicles
        vehicle_positions = [
            (300, 400, VehicleType.CAR),
            (600, 200, VehicleType.TRUCK),
            (1100, 500, VehicleType.CAR),
            (1400, 300, VehicleType.MOTORCYCLE),
            (400, 700, VehicleType.POLICE_CAR),
        ]
        
        for x, y, v_type in vehicle_positions:
            vehicle = Vehicle(x, y, v_type)
            vehicle.velocity = Vector2(random.uniform(-100, 100), random.uniform(-100, 100))
            self.vehicles.append(vehicle)
    
    def update(self, delta_time):
        """Update game world"""
        self.player.update(delta_time, self.width, self.height)
        
        for vehicle in self.vehicles:
            # Simple AI for vehicles
            if not vehicle.is_player:
                if random.random() < 0.01:
                    vehicle.accelerate(Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), delta_time)
            
            vehicle.update(delta_time, self.width, self.height)
            
            # Check collision with buildings
            for building in self.buildings:
                bx, by, bw, bh = building
                
                # Simple AABB collision
                if (vehicle.position.x - vehicle.width / 2 < bx + bw and
                    vehicle.position.x + vehicle.width / 2 > bx and
                    vehicle.position.y - vehicle.height / 2 < by + bh and
                    vehicle.position.y + vehicle.height / 2 > by):
                    
                    # Bounce back
                    vehicle.velocity.x *= -0.5
                    vehicle.velocity.y *= -0.5
                    vehicle.health -= 5
                    vehicle.health = max(0, vehicle.health)
    
    def draw(self, surface):
        """Draw world"""
        # Draw background
        surface.fill((50, 100, 50))
        
        # Draw roads (grid pattern)
        for x in range(0, self.width, 200):
            pygame.draw.line(surface, (100, 100, 100), (x, 0), (x, self.height), 3)
        
        for y in range(0, self.height, 200):
            pygame.draw.line(surface, (100, 100, 100), (0, y), (self.width, y), 3)
        
        # Draw buildings
        for building in self.buildings:
            bx, by, bw, bh = building
            pygame.draw.rect(surface, (150, 100, 50), (bx, by, bw, bh))
            pygame.draw.rect(surface, (200, 150, 100), (bx, by, bw, bh), 3)
            
            # Draw windows
            for wx in range(0, bw, 20):
                for wy in range(0, bh, 20):
                    pygame.draw.rect(surface, (255, 255, 100), (bx + wx + 2, by + wy + 2, 10, 10))
        
        # Draw vehicles
        for vehicle in self.vehicles:
            vehicle.draw(surface)
        
        # Draw player
        self.player.draw(surface)
