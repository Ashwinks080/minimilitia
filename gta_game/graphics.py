"""
Graphics Enhancement Module
Provides better visuals and particle effects
"""

import pygame
import math
import random


class ParticleEffect:
    """Particle effect system"""
    
    def __init__(self, x, y, color, lifetime=1.0):
        self.x = x
        self.y = y
        self.vx = random.uniform(-100, 100)
        self.vy = random.uniform(-100, 100)
        self.color = color
        self.lifetime = lifetime
        self.age = 0
        self.size = 5
    
    def update(self, delta_time):
        """Update particle"""
        self.age += delta_time
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        
        # Fade out
        self.vy += 50 * delta_time  # Gravity
        self.size = max(1, 5 * (1 - self.age / self.lifetime))
    
    def draw(self, surface, camera_x, camera_y):
        """Draw particle"""
        if self.age < self.lifetime:
            screen_x = int(self.x - camera_x)
            screen_y = int(self.y - camera_y)
            
            # Alpha blending (fade)
            alpha = int(255 * (1 - self.age / self.lifetime))
            if 0 < screen_x < surface.get_width() and 0 < screen_y < surface.get_height():
                pygame.draw.circle(surface, self.color, (screen_x, screen_y), int(self.size))
    
    def is_alive(self):
        """Check if particle is still alive"""
        return self.age < self.lifetime


class VehicleRenderer:
    """Enhanced vehicle rendering"""
    
    @staticmethod
    def draw_car(surface, vehicle):
        """Draw car with better graphics"""
        # Main body
        rect = pygame.Rect(
            vehicle.position.x - vehicle.width / 2,
            vehicle.position.y - vehicle.height / 2,
            vehicle.width,
            vehicle.height
        )
        pygame.draw.rect(surface, vehicle.color, rect)
        pygame.draw.rect(surface, (50, 50, 50), rect, 2)
        
        # Windows
        window_color = (100, 150, 200)
        pygame.draw.rect(surface, window_color, (
            rect.x + 2,
            rect.y + 2,
            vehicle.width - 4,
            vehicle.height / 3
        ))
        
        # Wheels (front and back)
        wheel_size = 3
        wheel_y1 = rect.y + 3
        wheel_y2 = rect.y + rect.height - 3
        
        # Front wheels
        pygame.draw.circle(surface, (50, 50, 50), (int(rect.x + 8), int(wheel_y1)), wheel_size)
        pygame.draw.circle(surface, (50, 50, 50), (int(rect.x + rect.width - 8), int(wheel_y1)), wheel_size)
        
        # Back wheels
        pygame.draw.circle(surface, (50, 50, 50), (int(rect.x + 8), int(wheel_y2)), wheel_size)
        pygame.draw.circle(surface, (50, 50, 50), (int(rect.x + rect.width - 8), int(wheel_y2)), wheel_size)
    
    @staticmethod
    def draw_truck(surface, vehicle):
        """Draw truck with better graphics"""
        rect = pygame.Rect(
            vehicle.position.x - vehicle.width / 2,
            vehicle.position.y - vehicle.height / 2,
            vehicle.width,
            vehicle.height
        )
        
        # Truck bed
        pygame.draw.rect(surface, vehicle.color, rect)
        pygame.draw.rect(surface, (100, 100, 50), rect, 3)
        
        # Cabin
        cabin_width = vehicle.width * 0.4
        pygame.draw.rect(surface, (180, 100, 50), (
            rect.x + rect.width - cabin_width,
            rect.y,
            cabin_width,
            rect.height
        ))
        
        # Wheels
        wheel_size = 4
        for wx in [rect.x + 8, rect.x + rect.width - 8]:
            pygame.draw.circle(surface, (30, 30, 30), (int(wx), int(rect.y + 3)), wheel_size)
            pygame.draw.circle(surface, (30, 30, 30), (int(wx), int(rect.y + rect.height - 3)), wheel_size)
    
    @staticmethod
    def draw_motorcycle(surface, vehicle):
        """Draw motorcycle with better graphics"""
        # Body
        pygame.draw.line(surface, vehicle.color, 
            (vehicle.position.x - 10, vehicle.position.y - 5),
            (vehicle.position.x + 10, vehicle.position.y + 5), 3)
        
        # Wheels
        pygame.draw.circle(surface, (50, 50, 50), 
            (int(vehicle.position.x - 12), int(vehicle.position.y)), 3)
        pygame.draw.circle(surface, (50, 50, 50),
            (int(vehicle.position.x + 12), int(vehicle.position.y)), 3)


class EffectManager:
    """Manages all particle effects"""
    
    def __init__(self):
        self.particles = []
    
    def create_explosion(self, x, y, intensity=10):
        """Create explosion effect"""
        colors = [(255, 100, 0), (255, 200, 0), (255, 100, 50)]
        for _ in range(intensity):
            color = random.choice(colors)
            particle = ParticleEffect(x, y, color, lifetime=random.uniform(0.5, 1.5))
            self.particles.append(particle)
    
    def create_dust(self, x, y, intensity=5):
        """Create dust effect"""
        for _ in range(intensity):
            color = (150, 150, 150)
            particle = ParticleEffect(x, y, color, lifetime=random.uniform(0.3, 0.8))
            self.particles.append(particle)
    
    def create_spark(self, x, y, intensity=15):
        """Create spark effect"""
        colors = [(255, 200, 100), (255, 255, 200)]
        for _ in range(intensity):
            color = random.choice(colors)
            particle = ParticleEffect(x, y, color, lifetime=random.uniform(0.2, 0.6))
            self.particles.append(particle)
    
    def update(self, delta_time):
        """Update all particles"""
        for particle in self.particles:
            particle.update(delta_time)
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]
    
    def draw(self, surface, camera_x, camera_y):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(surface, camera_x, camera_y)


class RoadRenderer:
    """Renders roads and streets"""
    
    @staticmethod
    def draw_roads(surface, map_width, map_height):
        """Draw road grid"""
        road_width = 3
        road_color = (100, 100, 100)
        
        # Vertical roads
        for x in range(0, map_width, 200):
            pygame.draw.line(surface, road_color, (x, 0), (x, map_height), road_width)
        
        # Horizontal roads
        for y in range(0, map_height, 200):
            pygame.draw.line(surface, road_color, (0, y), (map_width, y), road_width)
    
    @staticmethod
    def draw_grass(surface, map_width, map_height):
        """Draw grass areas"""
        grass_color = (40, 120, 40)
        surface.fill(grass_color)
