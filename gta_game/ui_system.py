"""
UI System for GTA-like Game
Handles HUD, menus, and displays
"""

import pygame
from typing import List


class HUD:
    """Head-Up Display"""
    
    def __init__(self, width=1600, height=900):
        self.width = width
        self.height = height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Colors
        self.color_text = (255, 255, 255)
        self.color_background = (20, 20, 20)
        self.color_accent = (255, 100, 0)
    
    def draw_player_stats(self, surface, player, mission_manager):
        """Draw player statistics"""
        # Money
        money_text = self.font_medium.render(f"Money: ${player.money}", True, self.color_text)
        surface.blit(money_text, (10, 10))
        
        # Health
        health_text = self.font_small.render(f"Health: {int(player.health)}", True, self.color_text)
        surface.blit(health_text, (10, 50))
        
        # Mission info
        if mission_manager.current_mission:
            mission = mission_manager.current_mission
            if not mission.completed and not mission.failed:
                mission_text = self.font_medium.render(mission.name, True, self.color_accent)
                surface.blit(mission_text, (10, 90))
                
                # Time remaining
                time_remaining = mission.get_time_remaining()
                time_text = self.font_small.render(f"Time: {int(time_remaining)}s", True, self.color_text)
                surface.blit(time_text, (10, 130))
                
                # Objectives
                for i, obj in enumerate(mission.objectives):
                    status = "✓" if obj.completed else "○"
                    obj_text = self.font_small.render(f"{status} {obj.description}", True, self.color_text)
                    surface.blit(obj_text, (10, 170 + i * 30))
    
    def draw_mission_markers(self, surface, mission_manager, camera_x, camera_y):
        """Draw mission markers on map"""
        if mission_manager.current_mission:
            for obj in mission_manager.current_mission.objectives:
                if not obj.completed:
                    marker_x = int(obj.target_x - camera_x)
                    marker_y = int(obj.target_y - camera_y)
                    
                    # Only draw if on screen
                    if 0 < marker_x < self.width and 0 < marker_y < self.height:
                        pygame.draw.circle(surface, (255, 0, 0), (marker_x, marker_y), 10)
                        pygame.draw.circle(surface, (255, 255, 0), (marker_x, marker_y), 12, 2)
    
    def draw_vehicle_info(self, surface, vehicle, font):
        """Draw vehicle information"""
        if vehicle:
            # Speed
            speed = (vehicle.velocity.x ** 2 + vehicle.velocity.y ** 2) ** 0.5
            speed_text = font.render(f"Speed: {int(speed)}", True, self.color_text)
            surface.blit(speed_text, (self.width - 300, 10))
            
            # Fuel
            fuel_text = font.render(f"Fuel: {int(vehicle.fuel)}%", True, self.color_text)
            surface.blit(fuel_text, (self.width - 300, 50))
            
            # Health
            health_text = font.render(f"Vehicle Health: {int(vehicle.health)}", True, self.color_text)
            surface.blit(health_text, (self.width - 300, 90))
    
    def draw_mission_complete(self, surface, mission, reward_money):
        """Draw mission complete screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Title
        title = self.font_large.render("MISSION COMPLETED", True, (0, 255, 0))
        surface.blit(title, (self.width // 2 - title.get_width() // 2, 200))
        
        # Mission name
        name = self.font_medium.render(mission.name, True, self.color_text)
        surface.blit(name, (self.width // 2 - name.get_width() // 2, 280))
        
        # Reward
        reward = self.font_medium.render(f"Reward: ${reward_money}", True, (0, 255, 0))
        surface.blit(reward, (self.width // 2 - reward.get_width() // 2, 350))


class MissionMenu:
    """Mission selection menu"""
    
    def __init__(self, width=1600, height=900):
        self.width = width
        self.height = height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.selected_mission_index = 0
        self.mission_list: List = []
    
    def set_missions(self, missions):
        """Set available missions"""
        self.mission_list = missions
        self.selected_mission_index = 0
    
    def update(self, keys):
        """Update menu based on input"""
        if keys[pygame.K_UP]:
            self.selected_mission_index = max(0, self.selected_mission_index - 1)
        elif keys[pygame.K_DOWN]:
            self.selected_mission_index = min(len(self.mission_list) - 1, self.selected_mission_index + 1)
    
    def draw(self, surface):
        """Draw mission menu"""
        # Background
        pygame.draw.rect(surface, (30, 30, 30), (100, 100, self.width - 200, self.height - 200))
        pygame.draw.rect(surface, (255, 100, 0), (100, 100, self.width - 200, self.height - 200), 3)
        
        # Title
        title = self.font_large.render("AVAILABLE MISSIONS", True, (255, 255, 255))
        surface.blit(title, (self.width // 2 - title.get_width() // 2, 130))
        
        # Mission list
        y_offset = 200
        for i, mission in enumerate(self.mission_list):
            color = (255, 100, 0) if i == self.selected_mission_index else (200, 200, 200)
            mission_text = self.font_medium.render(mission.name, True, color)
            surface.blit(mission_text, (150, y_offset))
            
            # Description
            desc_text = self.font_small.render(mission.description, True, (150, 150, 150))
            surface.blit(desc_text, (150, y_offset + 40))
            
            # Reward
            reward_text = self.font_small.render(f"Reward: ${mission.reward_money}", True, (0, 255, 0))
            surface.blit(reward_text, (150, y_offset + 70))
            
            y_offset += 130
        
        # Instructions
        instr_text = self.font_small.render("UP/DOWN to select, ENTER to start, ESC to cancel", True, (200, 200, 200))
        surface.blit(instr_text, (self.width // 2 - instr_text.get_width() // 2, self.height - 150))
