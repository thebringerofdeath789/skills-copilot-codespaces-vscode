"""
Task Scheduler System
Intelligent task scheduling based on growth stages and environmental conditions
"""

from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Any, Tuple
import logging
from enum import Enum

from ..models.task import Task, TaskType, Priority, TaskStatus
from ..models.garden import Garden, GrowthStage
from ...data.knowledge_base.growing_guides import growing_knowledge

logger = logging.getLogger(__name__)

class SchedulingRule(Enum):
    """Task scheduling rule types"""
    GROWTH_STAGE_BASED = "growth_stage"
    TIME_INTERVAL = "time_interval"
    ENVIRONMENTAL_TRIGGER = "environmental"
    DEPENDENCY_BASED = "dependency"
    SEASONAL = "seasonal"

class TaskScheduler:
    """Advanced task scheduling system"""
    
    def __init__(self, database_manager=None):
        self.db_manager = database_manager
        self.scheduling_rules = self.load_scheduling_rules()
        self.task_templates = self.load_task_templates()
    
    def load_scheduling_rules(self) -> Dict:
        """Load comprehensive scheduling rules"""
        return {
            "growth_stage_transitions": {
                "germination_to_seedling": {
                    "trigger_days": 7,
                    "tasks_to_create": ["transplant_seedlings", "adjust_lighting", "begin_light_feeding"]
                },
                "seedling_to_vegetative": {
                    "trigger_days": 14,
                    "tasks_to_create": ["increase_nutrients", "begin_training", "environmental_monitoring"]
                },
                "vegetative_to_flowering": {
                    "trigger_days": 56,  # 8 weeks default veg
                    "tasks_to_create": ["switch_light_cycle", "change_nutrients", "support_branches"]
                },
                "flowering_to_harvest": {
                    "trigger_conditions": ["trichome_check", "fade_completion"],
                    "tasks_to_create": ["begin_flush", "prepare_harvest", "trim_preparation"]
                }
            },
            "recurring_maintenance": {
                "daily": [
                    {"task": "environmental_check", "priority": "high"},
                    {"task": "visual_inspection", "priority": "medium"},
                    {"task": "water_level_check", "priority": "high"}
                ],
                "weekly": [
                    {"task": "nutrient_feeding", "priority": "critical"},
                    {"task": "ph_ec_measurement", "priority": "high"},
                    {"task": "pruning_check", "priority": "medium"},
                    {"task": "pest_inspection", "priority": "high"}
                ],
                "bi_weekly": [
                    {"task": "deep_environmental_clean", "priority": "medium"},
                    {"task": "equipment_maintenance", "priority": "medium"},
                    {"task": "growth_measurements", "priority": "low"}
                ],
                "monthly": [
                    {"task": "complete_garden_review", "priority": "medium"},
                    {"task": "supply_inventory", "priority": "low"},
                    {"task": "cost_analysis_update", "priority": "low"}
                ]
            },
            "environmental_triggers": {
                "high_temperature": {
                    "condition": "temperature > 85",
                    "tasks": ["increase_ventilation", "check_cooling", "stress_monitoring"]
                },
                "low_humidity": {
                    "condition": "humidity < 40",
                    "tasks": ["add_humidifier", "check_vpd", "leaf_inspection"]
                },
                "ph_drift": {
                    "condition": "abs(ph - target_ph) > 0.5",
                    "tasks": ["ph_adjustment", "reservoir_check", "nutrient_analysis"]
                }
            }
        }
    
    def load_task_templates(self) -> Dict:
        """Load comprehensive task templates"""
        return {
            "transplant_seedlings": {
                "title": "Transplant Seedlings",
                "description": "Move seedlings from starter medium to final containers",
                "task_type": TaskType.TRANSPLANTING,
                "priority": Priority.CRITICAL,
                "estimated_duration": 60,  # minutes
                "supplies_needed": ["containers", "growing_medium", "labels"],
                "instructions": [
                    "Prepare final containers with growing medium",
                    "Water containers lightly before transplanting", 
                    "Handle seedlings by cotyledon leaves only",
                    "Plant at same depth as in starter medium",
                    "Water gently after transplanting",
                    "Provide gentle light for first 24 hours"
                ]
            },
            "nutrient_feeding": {
                "title": "Nutrient Feeding",
                "description": "Mix and apply nutrient solution",
                "task_type": TaskType.FEEDING,
                "priority": Priority.CRITICAL,
                "estimated_duration": 30,
                "supplies_needed": ["nutrients", "ph_meter", "ec_meter", "measuring_tools"],
                "instructions": [
                    "Check water temperature (65-75°F optimal)",
                    "Add nutrients in proper order (usually micro, grow, bloom)",
                    "Mix thoroughly between additions",
                    "Check and adjust pH to 5.8-6.2 for soil, 5.5-6.5 for hydro",
                    "Record final EC/PPM readings",
                    "Apply solution evenly to plants"
                ]
            },
            "environmental_check": {
                "title": "Environmental Monitoring",
                "description": "Record temperature, humidity, and other environmental factors",
                "task_type": TaskType.MONITORING,
                "priority": Priority.HIGH,
                "estimated_duration": 10,
                "supplies_needed": ["thermometer", "hygrometer", "ph_meter"],
                "instructions": [
                    "Record temperature at canopy level",
                    "Record humidity at multiple locations",
                    "Check VPD calculation",
                    "Inspect air circulation",
                    "Note any environmental issues",
                    "Log readings in system"
                ]
            },
            "pest_inspection": {
                "title": "Pest and Disease Inspection",
                "description": "Thorough inspection for pests, diseases, and plant health issues",
                "task_type": TaskType.INSPECTION,
                "priority": Priority.HIGH,
                "estimated_duration": 20,
                "supplies_needed": ["magnifying_glass", "sticky_traps", "inspection_light"],
                "instructions": [
                    "Inspect undersides of leaves for pests",
                    "Look for webbing, eggs, or pest damage",
                    "Check for discoloration or unusual spots",
                    "Examine stems and branches",
                    "Document any issues with photos",
                    "Plan treatment if problems found"
                ]
            },
            "switch_light_cycle": {
                "title": "Switch to Flowering Light Cycle",
                "description": "Change lighting schedule to 12/12 for flowering stage",
                "task_type": TaskType.LIGHTING,
                "priority": Priority.CRITICAL,
                "estimated_duration": 15,
                "supplies_needed": ["timer", "light_meter"],
                "instructions": [
                    "Set timer to 12 hours on, 12 hours off",
                    "Ensure complete darkness during off period",
                    "Check for light leaks",
                    "Adjust light intensity if needed",
                    "Begin flowering nutrient regimen",
                    "Monitor plants for stress response"
                ]
            }
        }
    
    def create_growth_stage_schedule(self, plant_id: int, garden_id: int, 
                                   current_stage: GrowthStage, 
                                   stage_start_date: date) -> List[Dict]:
        """Create schedule for specific growth stage"""
        
        scheduled_tasks = []
        
        # Get stage-specific tasks from knowledge base
        stage_tasks = growing_knowledge.get_growth_stage_tasks("cannabis", current_stage.value)
        
        for task_info in stage_tasks:
            # Calculate due date
            if "day" in task_info:
                due_date = stage_start_date + timedelta(days=task_info["day"])
            elif "week" in task_info:
                due_date = stage_start_date + timedelta(weeks=task_info["week"])
            else:
                due_date = stage_start_date + timedelta(days=1)  # Default to next day
            
            # Create task data
            task_data = {
                "garden_id": garden_id,
                "plant_id": plant_id,
                "title": task_info["task"],
                "description": f"Growth stage task for {current_stage.value} phase",
                "task_type": self._determine_task_type(task_info["task"]),
                "priority": task_info.get("priority", "medium"),
                "due_date": due_date,
                "growth_stage": current_stage.value,
                "auto_generated": True
            }
            
            scheduled_tasks.append(task_data)
        
        return scheduled_tasks
    
    def _determine_task_type(self, task_description: str) -> str:
        """Determine task type from description"""
        task_keywords = {
            "water": TaskType.WATERING.value,
            "feed": TaskType.FEEDING.value,
            "nutrient": TaskType.FEEDING.value,
            "transplant": TaskType.TRANSPLANTING.value,
            "prune": TaskType.PRUNING.value,
            "train": TaskType.TRAINING.value,
            "harvest": TaskType.HARVESTING.value,
            "check": TaskType.MONITORING.value,
            "inspect": TaskType.INSPECTION.value,
            "light": TaskType.LIGHTING.value,
            "environment": TaskType.ENVIRONMENTAL.value
        }
        
        task_lower = task_description.lower()
        for keyword, task_type in task_keywords.items():
            if keyword in task_lower:
                return task_type
        
        return TaskType.GENERAL.value
    
    def schedule_recurring_tasks(self, garden_id: int, start_date: date, 
                               end_date: date) -> List[Dict]:
        """Schedule recurring maintenance tasks"""
        
        scheduled_tasks = []
        current_date = start_date
        
        while current_date <= end_date:
            # Daily tasks
            for task_template in self.scheduling_rules["recurring_maintenance"]["daily"]:
                task_data = {
                    "garden_id": garden_id,
                    "title": task_template["task"].replace("_", " ").title(),
                    "task_type": self._determine_task_type(task_template["task"]),
                    "priority": task_template["priority"],
                    "due_date": current_date,
                    "recurring_pattern": "daily",
                    "auto_generated": True
                }
                scheduled_tasks.append(task_data)
            
            # Weekly tasks (on Sundays)
            if current_date.weekday() == 6:  # Sunday
                for task_template in self.scheduling_rules["recurring_maintenance"]["weekly"]:
                    task_data = {
                        "garden_id": garden_id,
                        "title": task_template["task"].replace("_", " ").title(),
                        "task_type": self._determine_task_type(task_template["task"]),
                        "priority": task_template["priority"],
                        "due_date": current_date,
                        "recurring_pattern": "weekly",
                        "auto_generated": True
                    }
                    scheduled_tasks.append(task_data)
            
            # Monthly tasks (first day of month)
            if current_date.day == 1:
                for task_template in self.scheduling_rules["recurring_maintenance"]["monthly"]:
                    task_data = {
                        "garden_id": garden_id,
                        "title": task_template["task"].replace("_", " ").title(),
                        "task_type": self._determine_task_type(task_template["task"]),
                        "priority": task_template["priority"],
                        "due_date": current_date,
                        "recurring_pattern": "monthly",
                        "auto_generated": True
                    }
                    scheduled_tasks.append(task_data)
            
            current_date += timedelta(days=1)
        
        return scheduled_tasks
    
    def check_environmental_triggers(self, garden_id: int, 
                                   environmental_data: Dict) -> List[Dict]:
        """Check for environmental trigger conditions and create tasks"""
        
        triggered_tasks = []
        
        for trigger_name, trigger_config in self.scheduling_rules["environmental_triggers"].items():
            condition = trigger_config["condition"]
            
            # Simple condition evaluation (in production, use safer evaluation)
            try:
                # Replace variables in condition with actual values
                eval_condition = condition
                for key, value in environmental_data.items():
                    eval_condition = eval_condition.replace(key, str(value))
                
                # Add target values for comparison
                if "target_ph" in eval_condition:
                    eval_condition = eval_condition.replace("target_ph", "6.0")
                
                if eval(eval_condition):
                    # Trigger condition met, create tasks
                    for task_name in trigger_config["tasks"]:
                        task_data = {
                            "garden_id": garden_id,
                            "title": task_name.replace("_", " ").title(),
                            "description": f"Environmental trigger: {trigger_name}",
                            "task_type": self._determine_task_type(task_name),
                            "priority": "high",
                            "due_date": datetime.now().date(),
                            "environmental_trigger": trigger_name,
                            "auto_generated": True
                        }
                        triggered_tasks.append(task_data)
                        
            except Exception as e:
                logger.error(f"Error evaluating environmental trigger {trigger_name}: {e}")
        
        return triggered_tasks
    
    def optimize_task_schedule(self, tasks: List[Dict], 
                             constraints: Dict = None) -> List[Dict]:
        """Optimize task schedule based on constraints and dependencies"""
        
        if not constraints:
            constraints = {
                "max_daily_duration": 240,  # 4 hours max per day
                "preferred_times": {"morning": (8, 12), "afternoon": (12, 17)},
                "avoid_concurrent": ["feeding", "environmental_control"]
            }
        
        optimized_tasks = []
        
        # Group tasks by date
        tasks_by_date = {}
        for task in tasks:
            date_str = str(task["due_date"])
            if date_str not in tasks_by_date:
                tasks_by_date[date_str] = []
            tasks_by_date[date_str].append(task)
        
        # Optimize each day's schedule
        for date_str, daily_tasks in tasks_by_date.items():
            # Sort by priority and estimated duration
            daily_tasks.sort(key=lambda x: (
                self._priority_weight(x.get("priority", "medium")),
                -x.get("estimated_duration", 30)
            ))
            
            # Check total duration for the day
            total_duration = sum(task.get("estimated_duration", 30) for task in daily_tasks)
            
            if total_duration > constraints["max_daily_duration"]:
                # Reschedule some tasks to next available day
                current_duration = 0
                for i, task in enumerate(daily_tasks):
                    task_duration = task.get("estimated_duration", 30)
                    if current_duration + task_duration <= constraints["max_daily_duration"]:
                        current_duration += task_duration
                        optimized_tasks.append(task)
                    else:
                        # Move to next day
                        original_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        new_date = original_date + timedelta(days=1)
                        task["due_date"] = new_date
                        task["rescheduled"] = True
                        optimized_tasks.append(task)
            else:
                optimized_tasks.extend(daily_tasks)
        
        return optimized_tasks
    
    def _priority_weight(self, priority: str) -> int:
        """Convert priority to numeric weight for sorting"""
        weights = {
            "critical": 1,
            "high": 2,
            "medium": 3,
            "low": 4
        }
        return weights.get(priority, 3)
    
    def generate_feeding_schedule(self, plant_id: int, garden_id: int, 
                                growth_stage: GrowthStage, 
                                feeding_frequency_days: int = 7) -> List[Dict]:
        """Generate nutrient feeding schedule"""
        
        feeding_tasks = []
        
        # Get nutrient recipe for current stage
        recipe = growing_knowledge.get_nutrient_recipe("lucas_formula", growth_stage.value)
        
        # Calculate feeding dates for next 12 weeks
        start_date = datetime.now().date()
        for week in range(12):
            feeding_date = start_date + timedelta(weeks=week)
            
            task_data = {
                "garden_id": garden_id,
                "plant_id": plant_id,
                "title": f"Nutrient Feeding - Week {week + 1}",
                "description": f"Apply {growth_stage.value} nutrients using {recipe.get('recipe_name', 'standard')} recipe",
                "task_type": TaskType.FEEDING.value,
                "priority": Priority.CRITICAL.value,
                "due_date": feeding_date,
                "supplies_needed": list(recipe.get("nutrients", {}).keys()) if recipe else [],
                "feeding_recipe": recipe,
                "estimated_duration": 45,
                "recurring_pattern": f"every_{feeding_frequency_days}_days"
            }
            
            feeding_tasks.append(task_data)
        
        return feeding_tasks
    
    def create_harvest_schedule(self, plant_id: int, garden_id: int,
                              estimated_harvest_date: date) -> List[Dict]:
        """Create pre-harvest and harvest task schedule"""
        
        harvest_tasks = []
        
        # Pre-harvest tasks (2 weeks before)
        pre_harvest_date = estimated_harvest_date - timedelta(weeks=2)
        harvest_tasks.append({
            "garden_id": garden_id,
            "plant_id": plant_id,
            "title": "Begin Harvest Preparation",
            "description": "Start flush, check trichomes, prepare drying space",
            "task_type": TaskType.HARVESTING.value,
            "priority": Priority.HIGH.value,
            "due_date": pre_harvest_date,
            "estimated_duration": 60
        })
        
        # Trichome checks (weekly leading up to harvest)
        for week in range(3):
            check_date = pre_harvest_date + timedelta(weeks=week)
            harvest_tasks.append({
                "garden_id": garden_id,
                "plant_id": plant_id,
                "title": f"Trichome Check - Week {week + 1}",
                "description": "Examine trichomes with magnifying glass, document ripeness",
                "task_type": TaskType.INSPECTION.value,
                "priority": Priority.CRITICAL.value,
                "due_date": check_date,
                "estimated_duration": 15
            })
        
        # Main harvest task
        harvest_tasks.append({
            "garden_id": garden_id,
            "plant_id": plant_id,
            "title": "Harvest Day",
            "description": "Cut, weigh, and begin drying process",
            "task_type": TaskType.HARVESTING.value,
            "priority": Priority.CRITICAL.value,
            "due_date": estimated_harvest_date,
            "estimated_duration": 180,
            "supplies_needed": ["trimming_scissors", "scale", "drying_racks", "labels"]
        })
        
        # Post-harvest tasks
        harvest_tasks.append({
            "garden_id": garden_id,
            "plant_id": plant_id,
            "title": "Begin Curing Process",
            "description": "Move dried material to curing containers",
            "task_type": TaskType.PROCESSING.value,
            "priority": Priority.HIGH.value,
            "due_date": estimated_harvest_date + timedelta(days=7),
            "estimated_duration": 90
        })
        
        return harvest_tasks
