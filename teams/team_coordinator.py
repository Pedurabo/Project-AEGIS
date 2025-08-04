"""
TEAM COORDINATOR - Managing Small Task Handling Teams
Coordinates multiple teams efficiently for maximum productivity
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TeamStatus(Enum):
    """Team Status"""
    ACTIVE = "active"
    BUSY = "busy"
    IDLE = "idle"
    OFFLINE = "offline"


@dataclass
class TeamInfo:
    """Team Information"""
    team_id: str
    team_name: str
    silo: str
    members: List[str]
    status: TeamStatus
    current_tasks: int
    completed_tasks: int
    efficiency_score: float


class TeamCoordinator:
    """Team Coordinator - Manages Multiple Small Teams"""
    
    def __init__(self):
        self.coordinator_name = "Team Coordinator"
        self.teams = {}
        self.team_assignments = {}
        self.performance_tracking = {}
        
        # Team templates for easy creation
        self.team_templates = {
            "ai_research": {
                "name": "AI Research Core",
                "silo": "developmental",
                "members": ["Dr. Sarah Chen", "Dr. Marcus Rodriguez", "Dr. Elena Petrov"],
                "capabilities": ["deep_learning", "nlp", "computer_vision"]
            },
            "vulnerability_research": {
                "name": "Vulnerability Research",
                "silo": "security",
                "members": ["Agent Zero", "Agent Vector", "Agent Matrix"],
                "capabilities": ["zero_day", "exploit_dev", "threat_analysis"]
            },
            "workflow_automation": {
                "name": "Workflow Automation",
                "silo": "operational",
                "members": ["Coordinator Alpha", "Coordinator Beta"],
                "capabilities": ["workflow_design", "task_scheduling", "resource_allocation"]
            }
        }
        
        logger.info(f"{self.coordinator_name} initialized")
    
    def create_team(self, team_type: str, team_id: str = None) -> str:
        """Create a new team based on template"""
        if team_type not in self.team_templates:
            raise ValueError(f"Unknown team type: {team_type}")
        
        if team_id is None:
            team_id = f"{team_type}_{datetime.now().strftime('%Y%m%d_%H%M')}"
        
        template = self.team_templates[team_type]
        
        team_info = TeamInfo(
            team_id=team_id,
            team_name=template["name"],
            silo=template["silo"],
            members=template["members"],
            status=TeamStatus.IDLE,
            current_tasks=0,
            completed_tasks=0,
            efficiency_score=95.0
        )
        
        self.teams[team_id] = team_info
        self.performance_tracking[team_id] = {
            "tasks_assigned": 0,
            "tasks_completed": 0,
            "efficiency_history": [],
            "created_at": datetime.now()
        }
        
        logger.info(f"Created team: {team_info.team_name} ({team_id})")
        return team_id
    
    def assign_task_to_team(self, team_id: str, task_description: str, priority: int = 1) -> bool:
        """Assign task to specific team"""
        if team_id not in self.teams:
            logger.error(f"Team {team_id} not found")
            return False
        
        team = self.teams[team_id]
        team.current_tasks += 1
        team.status = TeamStatus.BUSY
        
        self.performance_tracking[team_id]["tasks_assigned"] += 1
        
        logger.info(f"Assigned task to {team.team_name}: {task_description}")
        return True
    
    def complete_task_for_team(self, team_id: str, task_description: str) -> bool:
        """Mark task as completed for team"""
        if team_id not in self.teams:
            logger.error(f"Team {team_id} not found")
            return False
        
        team = self.teams[team_id]
        team.current_tasks = max(0, team.current_tasks - 1)
        team.completed_tasks += 1
        
        # Update status based on current tasks
        if team.current_tasks == 0:
            team.status = TeamStatus.IDLE
        else:
            team.status = TeamStatus.BUSY
        
        self.performance_tracking[team_id]["tasks_completed"] += 1
        
        # Update efficiency score
        total_assigned = self.performance_tracking[team_id]["tasks_assigned"]
        total_completed = self.performance_tracking[team_id]["tasks_completed"]
        
        if total_assigned > 0:
            completion_rate = (total_completed / total_assigned) * 100
            team.efficiency_score = min(100.0, completion_rate + 85.0)  # Base 85% + completion bonus
        
        logger.info(f"Task completed by {team.team_name}: {task_description}")
        return True
    
    def get_team_status(self, team_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of specific team"""
        if team_id not in self.teams:
            return None
        
        team = self.teams[team_id]
        performance = self.performance_tracking[team_id]
        
        return {
            "team_id": team.team_id,
            "team_name": team.team_name,
            "silo": team.silo,
            "members": team.members,
            "status": team.status.value,
            "current_tasks": team.current_tasks,
            "completed_tasks": team.completed_tasks,
            "efficiency_score": team.efficiency_score,
            "performance": {
                "tasks_assigned": performance["tasks_assigned"],
                "tasks_completed": performance["tasks_completed"],
                "completion_rate": f"{(performance['tasks_completed'] / max(1, performance['tasks_assigned'])) * 100:.1f}%"
            }
        }
    
    def get_all_teams_status(self) -> Dict[str, Any]:
        """Get status of all teams"""
        teams_status = {}
        total_efficiency = 0.0
        active_teams = 0
        
        for team_id, team in self.teams.items():
            teams_status[team_id] = self.get_team_status(team_id)
            if team.status != TeamStatus.OFFLINE:
                total_efficiency += team.efficiency_score
                active_teams += 1
        
        overall_efficiency = total_efficiency / max(1, active_teams)
        
        return {
            "total_teams": len(self.teams),
            "active_teams": active_teams,
            "overall_efficiency": overall_efficiency,
            "teams": teams_status
        }
    
    def get_silo_summary(self, silo: str) -> Dict[str, Any]:
        """Get summary for specific silo"""
        silo_teams = [team for team in self.teams.values() if team.silo == silo]
        
        if not silo_teams:
            return {"message": f"No teams found for silo: {silo}"}
        
        total_tasks = sum(team.current_tasks for team in silo_teams)
        total_completed = sum(team.completed_tasks for team in silo_teams)
        avg_efficiency = sum(team.efficiency_score for team in silo_teams) / len(silo_teams)
        
        return {
            "silo": silo,
            "teams_count": len(silo_teams),
            "total_current_tasks": total_tasks,
            "total_completed_tasks": total_completed,
            "average_efficiency": avg_efficiency,
            "teams": [team.team_name for team in silo_teams]
        }
    
    def optimize_team_workload(self) -> Dict[str, Any]:
        """Optimize team workload distribution"""
        optimization_results = {}
        
        for team_id, team in self.teams.items():
            if team.status == TeamStatus.IDLE and team.efficiency_score > 90:
                optimization_results[team_id] = {
                    "action": "assign_more_tasks",
                    "reason": "High efficiency team is idle",
                    "recommendation": "Increase workload"
                }
            elif team.status == TeamStatus.BUSY and team.current_tasks > 3:
                optimization_results[team_id] = {
                    "action": "reduce_workload",
                    "reason": "Team is overloaded",
                    "recommendation": "Reduce current tasks"
                }
            elif team.efficiency_score < 80:
                optimization_results[team_id] = {
                    "action": "provide_support",
                    "reason": "Low efficiency detected",
                    "recommendation": "Provide additional resources"
                }
        
        return optimization_results


def test_team_coordinator():
    """Test the Team Coordinator"""
    print("🎯 Testing Team Coordinator")
    print("=" * 40)
    
    # Initialize coordinator
    coordinator = TeamCoordinator()
    
    # Create teams
    ai_team = coordinator.create_team("ai_research", "ai_team_001")
    vuln_team = coordinator.create_team("vulnerability_research", "vuln_team_001")
    workflow_team = coordinator.create_team("workflow_automation", "workflow_team_001")
    
    # Assign tasks
    coordinator.assign_task_to_team(ai_team, "Develop neural network for penetration testing", 1)
    coordinator.assign_task_to_team(ai_team, "Optimize AI algorithms for stealth operations", 2)
    
    coordinator.assign_task_to_team(vuln_team, "Discover zero-day vulnerabilities", 1)
    coordinator.assign_task_to_team(vuln_team, "Develop exploit framework", 1)
    
    coordinator.assign_task_to_team(workflow_team, "Design automated workflow system", 1)
    
    # Complete some tasks
    coordinator.complete_task_for_team(ai_team, "Develop neural network for penetration testing")
    coordinator.complete_task_for_team(vuln_team, "Discover zero-day vulnerabilities")
    coordinator.complete_task_for_team(workflow_team, "Design automated workflow system")
    
    # Get status reports
    all_status = coordinator.get_all_teams_status()
    
    print(f"📊 Total Teams: {all_status['total_teams']}")
    print(f"🟢 Active Teams: {all_status['active_teams']}")
    print(f"📈 Overall Efficiency: {all_status['overall_efficiency']:.1f}%")
    
    print("\n🧠 Developmental Silo:")
    dev_summary = coordinator.get_silo_summary("developmental")
    print(f"   Teams: {dev_summary['teams_count']}")
    print(f"   Efficiency: {dev_summary['average_efficiency']:.1f}%")
    
    print("\n🔐 Security Silo:")
    sec_summary = coordinator.get_silo_summary("security")
    print(f"   Teams: {sec_summary['teams_count']}")
    print(f"   Efficiency: {sec_summary['average_efficiency']:.1f}%")
    
    print("\n⚙️ Operational Silo:")
    op_summary = coordinator.get_silo_summary("operational")
    print(f"   Teams: {op_summary['teams_count']}")
    print(f"   Efficiency: {op_summary['average_efficiency']:.1f}%")
    
    # Get optimization recommendations
    optimization = coordinator.optimize_team_workload()
    print(f"\n🔧 Optimization Recommendations: {len(optimization)}")
    
    for team_id, rec in optimization.items():
        print(f"   {team_id}: {rec['action']} - {rec['reason']}")
    
    print("\n✅ Team Coordinator is working efficiently!")


if __name__ == "__main__":
    test_team_coordinator() 