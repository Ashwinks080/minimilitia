"""
Mission System for GTA-like Game
Handles missions, objectives, and rewards
"""

import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Callable


class MissionType(Enum):
    DELIVERY = "delivery"
    ROBBERY = "robbery"
    CHASE = "chase"
    ESCORT = "escort"
    DESTRUCTION = "destruction"


class ObjectiveType(Enum):
    REACH_LOCATION = "reach_location"
    COLLECT_ITEM = "collect_item"
    DESTROY_TARGET = "destroy_target"
    ESCAPE = "escape"
    SURVIVE = "survive"


@dataclass
class Objective:
    """Mission objective"""
    objective_type: ObjectiveType
    target_x: float
    target_y: float
    description: str
    completed: bool = False
    progress: float = 0.0


class Mission:
    """Mission class"""
    
    def __init__(self, mission_id, name, mission_type, description, reward_money=1000):
        self.mission_id = mission_id
        self.name = name
        self.mission_type = mission_type
        self.description = description
        self.objectives: List[Objective] = []
        self.reward_money = reward_money
        self.reward_xp = 100
        self.started = False
        self.completed = False
        self.failed = False
        self.time_limit = 300  # 5 minutes
        self.time_elapsed = 0
        self.on_complete: Optional[Callable] = None
        self.on_fail: Optional[Callable] = None
    
    def add_objective(self, objective: Objective):
        """Add objective to mission"""
        self.objectives.append(objective)
    
    def start(self):
        """Start mission"""
        self.started = True
        self.time_elapsed = 0
    
    def update(self, delta_time, player_position):
        """Update mission"""
        if not self.started or self.completed or self.failed:
            return
        
        self.time_elapsed += delta_time
        
        # Check time limit
        if self.time_elapsed > self.time_limit:
            self.fail()
            return
        
        # Update objectives
        for objective in self.objectives:
            if not objective.completed:
                distance = ((player_position.x - objective.target_x) ** 2 + 
                           (player_position.y - objective.target_y) ** 2) ** 0.5
                
                # Marker radius
                if distance < 50:
                    objective.completed = True
        
        # Check if all objectives complete
        if all(obj.completed for obj in self.objectives):
            self.complete()
    
    def complete(self):
        """Complete mission"""
        self.completed = True
        if self.on_complete:
            self.on_complete()
    
    def fail(self):
        """Fail mission"""
        self.failed = True
        if self.on_fail:
            self.on_fail()
    
    def get_time_remaining(self):
        """Get remaining time"""
        remaining = self.time_limit - self.time_elapsed
        return max(0, remaining)


class MissionManager:
    """Manages all missions"""
    
    def __init__(self):
        self.missions: List[Mission] = []
        self.current_mission: Optional[Mission] = None
        self.completed_missions: List[Mission] = []
        self.total_money_earned = 0
        self.total_xp_earned = 0
        self._generate_missions()
    
    def _generate_missions(self):
        """Generate missions"""
        missions_data = [
            # Delivery missions
            ("M1", "Pizza Delivery", MissionType.DELIVERY, 
             "Deliver pizza to the docks", 500),
            ("M2", "Package Delivery", MissionType.DELIVERY,
             "Deliver packages across the city", 750),
            
            # Robbery missions
            ("M3", "Store Robbery", MissionType.ROBBERY,
             "Rob the convenience store", 1000),
            ("M4", "Bank Heist", MissionType.ROBBERY,
             "Steal from the bank vault", 2000),
            
            # Chase missions
            ("M5", "Car Chase", MissionType.CHASE,
             "Chase the suspect's vehicle", 800),
            ("M6", "Escaped Criminal", MissionType.CHASE,
             "Catch the escaped prisoner", 1200),
            
            # Destruction missions
            ("M7", "Vehicle Destruction", MissionType.DESTRUCTION,
             "Destroy 5 parked cars", 600),
            ("M8", "Property Damage", MissionType.DESTRUCTION,
             "Destroy the rival gang's hideout", 1500),
        ]
        
        for mission_id, name, m_type, desc, reward in missions_data:
            mission = Mission(mission_id, name, m_type, desc, reward)
            
            # Add objectives based on type
            if m_type == MissionType.DELIVERY:
                mission.add_objective(Objective(
                    ObjectiveType.REACH_LOCATION,
                    1500, 800,
                    "Go to the delivery location"
                ))
            elif m_type == MissionType.ROBBERY:
                mission.add_objective(Objective(
                    ObjectiveType.REACH_LOCATION,
                    random.randint(200, 1400),
                    random.randint(200, 800),
                    "Reach the robbery location"
                ))
            elif m_type == MissionType.CHASE:
                mission.add_objective(Objective(
                    ObjectiveType.REACH_LOCATION,
                    1200, 400,
                    "Catch the suspect"
                ))
            elif m_type == MissionType.DESTRUCTION:
                for i in range(3):
                    mission.add_objective(Objective(
                        ObjectiveType.DESTROY_TARGET,
                        random.randint(300, 1300),
                        random.randint(300, 700),
                        f"Destroy target {i+1}"
                    ))
            
            self.missions.append(mission)
    
    def get_available_missions(self):
        """Get available missions (not started)"""
        return [m for m in self.missions if not m.started and m not in self.completed_missions]
    
    def start_mission(self, mission_id):
        """Start a mission"""
        mission = next((m for m in self.missions if m.mission_id == mission_id), None)
        if mission:
            self.current_mission = mission
            mission.start()
            mission.on_complete = self._on_mission_complete
            mission.on_fail = self._on_mission_fail
            return True
        return False
    
    def update_current_mission(self, delta_time, player_position):
        """Update current mission"""
        if self.current_mission:
            self.current_mission.update(delta_time, player_position)
    
    def _on_mission_complete(self):
        """Called when mission completes"""
        if self.current_mission:
            self.completed_missions.append(self.current_mission)
            self.total_money_earned += self.current_mission.reward_money
            self.total_xp_earned += self.current_mission.reward_xp
    
    def _on_mission_fail(self):
        """Called when mission fails"""
        pass
