"""
GTA-like Game - Main Game Loop
A top-down action game with vehicles, missions, and gameplay
"""

import pygame
import sys
import math
from game_world import GameWorld, Player, Vehicle, VehicleType, Vector2
from mission_system import MissionManager, ObjectiveType
from ui_system import HUD, MissionMenu


class GameState:
    PLAYING = "playing"
    MISSION_SELECT = "mission_select"
    MISSION_COMPLETE = "mission_complete"
    GAME_OVER = "game_over"
    PAUSED = "paused"


class GTAGame:
    def __init__(self, width=1600, height=900):
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("GTA-like Game")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # Game components
        self.world = GameWorld(width, height)
        self.mission_manager = MissionManager()
        self.hud = HUD(width, height)
        self.mission_menu = MissionMenu(width, height)
        
        # Game state
        self.state = GameState.PLAYING
        self.camera_x = 0
        self.camera_y = 0
        self.show_mission_complete_timer = 0
        self.completed_mission = None
        
        # Controls
        self.keys_pressed = {}
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed[event.key] = True
                self._handle_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_pressed[event.key] = False
    
    def _handle_keydown(self, key):
        """Handle key press"""
        if key == pygame.K_ESCAPE:
            if self.state == GameState.MISSION_SELECT:
                self.state = GameState.PLAYING
            elif self.state == GameState.PLAYING:
                self.state = GameState.MISSION_SELECT
            elif self.state == GameState.MISSION_COMPLETE:
                self.state = GameState.PLAYING
                self.completed_mission = None
        
        elif key == pygame.K_RETURN:
            if self.state == GameState.MISSION_SELECT:
                mission = self.mission_menu.mission_list[self.mission_menu.selected_mission_index]
                self.mission_manager.start_mission(mission.mission_id)
                self.state = GameState.PLAYING
        
        elif key == pygame.K_e:
            # Enter/exit vehicle
            if self.state == GameState.PLAYING:
                if not self.world.player.is_in_vehicle:
                    # Find nearby vehicle
                    for vehicle in self.world.vehicles:
                        distance = self.world.player.position.distance_to(vehicle.position)
                        if distance < 50:
                            self.world.player.enter_vehicle(vehicle)
                            vehicle.is_player = True
                            break
                else:
                    self.world.player.exit_vehicle()
        
        elif key == pygame.K_m:
            # Open mission menu
            if self.state == GameState.PLAYING:
                self.mission_menu.set_missions(
                    self.mission_manager.get_available_missions()
                )
                self.state = GameState.MISSION_SELECT
    
    def update(self):
        """Update game state"""
        delta_time = 1.0 / self.fps
        
        if self.state == GameState.PLAYING:
            # Handle player input
            self._handle_player_input()
            
            # Update world
            self.world.update(delta_time)
            
            # Update missions
            self.mission_manager.update_current_mission(delta_time, self.world.player.position)
            
            # Check mission status
            if self.mission_manager.current_mission:
                if self.mission_manager.current_mission.completed:
                    self.state = GameState.MISSION_COMPLETE
                    self.completed_mission = self.mission_manager.current_mission
                    self.show_mission_complete_timer = 3.0
                elif self.mission_manager.current_mission.failed:
                    self.mission_manager.current_mission = None
            
            # Update camera
            self._update_camera()
        
        elif self.state == GameState.MISSION_SELECT:
            self.mission_menu.update(self.keys_pressed)
        
        elif self.state == GameState.MISSION_COMPLETE:
            self.show_mission_complete_timer -= delta_time
            if self.show_mission_complete_timer <= 0:
                self.state = GameState.PLAYING
                self.world.player.money += self.completed_mission.reward_money
    
    def _handle_player_input(self):
        """Handle player input"""
        player = self.world.player
        
        if player.is_in_vehicle:
            # Vehicle controls
            vehicle = player.current_vehicle
            
            # Movement
            if self.keys_pressed.get(pygame.K_w):
                vehicle.accelerate(Vector2(0, -1), 1.0 / self.fps)
            if self.keys_pressed.get(pygame.K_s):
                vehicle.accelerate(Vector2(0, 1), 1.0 / self.fps)
            if self.keys_pressed.get(pygame.K_a):
                vehicle.accelerate(Vector2(-1, 0), 1.0 / self.fps)
            if self.keys_pressed.get(pygame.K_d):
                vehicle.accelerate(Vector2(1, 0), 1.0 / self.fps)
            
            # Steering
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(
                mouse_y - self.height // 2,
                mouse_x - self.width // 2
            )
            vehicle.steer(angle)
        
        else:
            # Player movement
            dx = 0
            dy = 0
            
            if self.keys_pressed.get(pygame.K_w):
                dy -= 1
            if self.keys_pressed.get(pygame.K_s):
                dy += 1
            if self.keys_pressed.get(pygame.K_a):
                dx -= 1
            if self.keys_pressed.get(pygame.K_d):
                dx += 1
            
            player.move(dx, dy)
    
    def _update_camera(self):
        """Update camera to follow player"""
        player = self.world.player
        
        # Smooth camera follow
        target_x = player.position.x - self.width / 2
        target_y = player.position.y - self.height / 2
        
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        # Clamp camera
        self.camera_x = max(0, min(self.camera_x, self.world.width - self.width))
        self.camera_y = max(0, min(self.camera_y, self.world.height - self.height))
    
    def draw(self):
        """Draw game"""
        self.screen.fill((30, 30, 30))
        
        if self.state == GameState.PLAYING:
            self._draw_game_world()
        
        elif self.state == GameState.MISSION_SELECT:
            self._draw_game_world()
            self.mission_menu.draw(self.screen)
        
        elif self.state == GameState.MISSION_COMPLETE:
            self._draw_game_world()
            if self.completed_mission:
                self.hud.draw_mission_complete(
                    self.screen,
                    self.completed_mission,
                    self.completed_mission.reward_money
                )
        
        pygame.display.flip()
    
    def _draw_game_world(self):
        """Draw the game world"""
        # Create a surface for the world
        world_surface = pygame.Surface((self.world.width, self.world.height))
        
        # Draw world
        self.world.draw(world_surface)
        
        # Draw mission markers
        self.hud.draw_mission_markers(world_surface, self.mission_manager, 0, 0)
        
        # Blit world to screen with camera offset
        self.screen.blit(
            world_surface,
            (-self.camera_x, -self.camera_y)
        )
        
        # Draw HUD
        self.hud.draw_player_stats(self.screen, self.world.player, self.mission_manager)
        
        # Draw vehicle info if in vehicle
        if self.world.player.is_in_vehicle:
            self.hud.draw_vehicle_info(self.screen, self.world.player.current_vehicle, self.hud.font_small)
        
        # Draw crosshair for vehicle steering
        if self.world.player.is_in_vehicle:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pygame.draw.circle(self.screen, (255, 100, 0), (mouse_x, mouse_y), 5)
            pygame.draw.circle(self.screen, (255, 100, 0), (mouse_x, mouse_y), 15, 1)
        
        # Draw instructions
        font = pygame.font.Font(None, 20)
        instr = font.render("W/A/S/D: Move | E: Enter/Exit Vehicle | M: Missions | ESC: Menu", True, (200, 200, 200))
        self.screen.blit(instr, (10, self.height - 30))
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = GTAGame()
    game.run()
