"""
Pygame-based Game Client with Graphics
Renders the multiplayer game with Pygame
"""

import pygame
import sys
import math
from client import GameClient, Player
from game_engine import GameEngine, Vector2, GameMode
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameRenderer:
    """Handles all game rendering"""
    
    def __init__(self, width: int = 1280, height: int = 720):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Mini Militia - Multiplayer")
        
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Colors
        self.COLOR_BG = (30, 30, 40)
        self.COLOR_PLATFORM = (100, 100, 120)
        self.COLOR_TEAM_1 = (255, 100, 100)
        self.COLOR_TEAM_2 = (100, 150, 255)
        self.COLOR_TEXT = (255, 255, 255)
        self.COLOR_HEALTH_BG = (100, 100, 100)
        self.COLOR_HEALTH = (100, 255, 100)
    
    def draw_game(self, game_engine: GameEngine, local_player: Player, remote_players: list):
        """Draw the game state"""
        self.screen.fill(self.COLOR_BG)
        
        self._draw_map(game_engine.game_map)
        self._draw_projectiles(game_engine.projectiles)
        self._draw_players(local_player, remote_players)
        self._draw_hud(local_player, remote_players)
        
        pygame.display.flip()
    
    def _draw_map(self, game_map):
        """Draw game map"""
        for platform_pos, platform_width, platform_height in game_map.platforms:
            rect = pygame.Rect(
                platform_pos.x - platform_width / 2,
                platform_pos.y - platform_height / 2,
                platform_width,
                platform_height
            )
            pygame.draw.rect(self.screen, self.COLOR_PLATFORM, rect)
        
        for obstacle_pos, obstacle_radius in game_map.obstacles:
            pygame.draw.circle(
                self.screen,
                (150, 150, 150),
                (int(obstacle_pos.x), int(obstacle_pos.y)),
                int(obstacle_radius)
            )
    
    def _draw_projectiles(self, projectiles):
        """Draw projectiles"""
        for projectile in projectiles:
            pygame.draw.circle(
                self.screen,
                (255, 255, 100),
                (int(projectile.position.x), int(projectile.position.y)),
                3
            )
    
    def _draw_players(self, local_player: Player, remote_players: list):
        """Draw all players"""
        if local_player:
            self._draw_player(local_player, is_local=True)
        
        for player in remote_players:
            self._draw_player(player, is_local=False)
    
    def _draw_player(self, player: Player, is_local: bool = False):
        """Draw a single player"""
        if not player.is_alive:
            return
        
        color = self.COLOR_TEAM_1 if player.team == 0 else self.COLOR_TEAM_2
        
        pygame.draw.circle(
            self.screen,
            color,
            (int(player.x), int(player.y)),
            15
        )
        
        if is_local:
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                (int(player.x), int(player.y)),
                15,
                2
            )
        
        health_bar_width = 30
        health_bar_height = 5
        health_bar_x = player.x - health_bar_width / 2
        health_bar_y = player.y - 25
        
        pygame.draw.rect(
            self.screen,
            self.COLOR_HEALTH_BG,
            (health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        )
        
        health_width = (player.health / 100) * health_bar_width
        pygame.draw.rect(
            self.screen,
            self.COLOR_HEALTH,
            (health_bar_x, health_bar_y, health_width, health_bar_height)
        )
        
        name_text = self.font_small.render(player.name, True, self.COLOR_TEXT)
        self.screen.blit(name_text, (player.x - 20, player.y - 40))
    
    def _draw_hud(self, local_player: Player, remote_players: list):
        """Draw heads-up display"""
        if not local_player:
            return
        
        stats_text = [
            f"Health: {local_player.health}",
            f"Ammo: {local_player.ammo}",
            f"Score: {local_player.score}"
        ]
        
        y_offset = self.height - 100
        for i, text in enumerate(stats_text):
            surface = self.font_small.render(text, True, self.COLOR_TEXT)
            self.screen.blit(surface, (10, y_offset + i * 30))
        
        y_offset = 10
        title = self.font_medium.render("Players", True, self.COLOR_TEXT)
        self.screen.blit(title, (self.width - 200, y_offset))
        
        y_offset += 40
        if local_player:
            text = f"{local_player.name} (You) - {local_player.score}"
            color = self.COLOR_TEAM_1 if local_player.team == 0 else self.COLOR_TEAM_2
            surface = self.font_small.render(text, True, color)
            self.screen.blit(surface, (self.width - 200, y_offset))
            y_offset += 25
        
        for player in remote_players:
            text = f"{player.name} - {player.score}"
            color = self.COLOR_TEAM_1 if player.team == 0 else self.COLOR_TEAM_2
            surface = self.font_small.render(text, True, color)
            self.screen.blit(surface, (self.width - 200, y_offset))
            y_offset += 25
    
    def draw_connecting(self):
        """Draw connecting screen"""
        self.screen.fill(self.COLOR_BG)
        
        text = self.font_large.render("Connecting to server...", True, self.COLOR_TEXT)
        self.screen.blit(text, (self.width // 2 - 250, self.height // 2 - 50))
        
        pygame.display.flip()
    
    def draw_waiting(self, player_count: int, max_players: int = 6):
        """Draw waiting for players screen"""
        self.screen.fill(self.COLOR_BG)
        
        text = self.font_large.render("Waiting for players...", True, self.COLOR_TEXT)
        self.screen.blit(text, (self.width // 2 - 250, self.height // 2 - 100))
        
        count_text = self.font_medium.render(f"{player_count}/{max_players}", True, self.COLOR_TEXT)
        self.screen.blit(count_text, (self.width // 2 - 50, self.height // 2 + 50))
        
        pygame.display.flip()


class PygameGameClient:
    """Pygame-based game client"""
    
    def __init__(self, server_host: str = "localhost", server_port: int = 5000, player_name: str = "Player"):
        pygame.init()
        
        self.renderer = GameRenderer()
        self.game_client = GameClient(server_host, server_port, player_name)
        self.game_engine = GameEngine(self.renderer.width, self.renderer.height, GameMode.TEAM_DEATHMATCH)
        
        self.running = True
        self.game_started = False
        self.player_velocity = Vector2(0, 0)
        self.is_jumping = False
        
        self.game_client.on_player_joined = self._on_player_joined
        self.game_client.on_player_left = self._on_player_left
        self.game_client.on_player_updated = self._on_player_updated
        self.game_client.on_game_started = self._on_game_started
        self.game_client.on_game_state = self._on_game_state
    
    def run(self):
        """Main game loop"""
        self.renderer.draw_connecting()
        if not self.game_client.connect():
            logger.error("Failed to connect to server")
            return
        
        while not self.game_started and self.running:
            self._handle_events()
            
            if self.game_client.local_player:
                self.renderer.draw_waiting(
                    len(self.game_client.get_all_players()),
                    6
                )
            else:
                self.renderer.draw_connecting()
            
            self.renderer.clock.tick(60)
        
        while self.running and self.game_started:
            self._handle_events()
            self._update_game()
            self._render_game()
            
            self.renderer.clock.tick(60)
        
        self.game_client.disconnect()
        pygame.quit()
    
    def _handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self._jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._shoot()
        
        keys = pygame.key.get_pressed()
        self._handle_movement(keys)
    
    def _handle_movement(self, keys):
        """Handle player movement"""
        if not self.game_client.local_player:
            return
        
        move_speed = 200
        
        if keys[pygame.K_a]:
            self.player_velocity.x = -move_speed
        elif keys[pygame.K_d]:
            self.player_velocity.x = move_speed
        else:
            self.player_velocity.x = 0
        
        new_x = self.game_client.local_player.x + self.player_velocity.x * (1 / 60)
        new_x = max(0, min(new_x, self.renderer.width))
        
        self.game_client.update_player_position(new_x, self.game_client.local_player.y)
    
    def _jump(self):
        """Handle jump"""
        if not self.game_client.local_player or self.is_jumping:
            return
        
        self.player_velocity.y = -300
        self.is_jumping = True
    
    def _shoot(self):
        """Handle shooting"""
        if not self.game_client.local_player:
            return
        
        nearest_enemy = None
        nearest_distance = float('inf')
        
        for player in self.game_client.get_remote_players():
            if player.team != self.game_client.local_player.team and player.is_alive:
                distance = math.sqrt(
                    (player.x - self.game_client.local_player.x) ** 2 +
                    (player.y - self.game_client.local_player.y) ** 2
                )
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_enemy = player
        
        if nearest_enemy:
            self.game_client.shoot(nearest_enemy.id, damage=10)
    
    def _update_game(self):
        """Update game state"""
        delta_time = 1 / 60
        
        self.player_velocity = self.game_engine.apply_gravity(self.player_velocity, delta_time)
        
        if self.game_client.local_player:
            if self.game_engine.game_map.is_on_platform(
                Vector2(self.game_client.local_player.x, self.game_client.local_player.y),
                15
            ):
                self.is_jumping = False
                self.player_velocity.y = 0
        
        self.game_engine.update(delta_time)
    
    def _render_game(self):
        """Render game"""
        self.renderer.draw_game(
            self.game_engine,
            self.game_client.local_player,
            self.game_client.get_remote_players()
        )
    
    def _on_player_joined(self, player: Player):
        logger.info(f"Player {player.name} joined")
    
    def _on_player_left(self, player: Player):
        logger.info(f"Player {player.name} left")
    
    def _on_player_updated(self, player: Player):
        pass
    
    def _on_game_started(self):
        logger.info("Game started!")
        self.game_started = True
    
    def _on_game_state(self, state: dict):
        pass


if __name__ == "__main__":
    server_host = "localhost"
    server_port = 5000
    player_name = "Player"
    
    if len(sys.argv) > 1:
        server_host = sys.argv[1]
    if len(sys.argv) > 2:
        server_port = int(sys.argv[2])
    if len(sys.argv) > 3:
        player_name = sys.argv[3]
    
    client = PygameGameClient(server_host, server_port, player_name)
    client.run()
