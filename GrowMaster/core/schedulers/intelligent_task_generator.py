"""
GrowMaster Pro - Intelligent Task Generation System
Automated task generation based on growth stages, growing methods, and plant requirements
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class GrowthStage(Enum):
    """Plant growth stages"""
    SEED = "seed"
    GERMINATION = "germination"
    SEEDLING = "seedling"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    HARVEST = "harvest"
    CURING = "curing"

class TaskType(Enum):
    """Task types for automated generation"""
    WATERING = "watering"
    FEEDING = "feeding"
    MONITORING = "monitoring"
    PRUNING = "pruning"
    TRAINING = "training"
    HARVESTING = "harvesting"
    MAINTENANCE = "maintenance"
    ENVIRONMENTAL = "environmental"

@dataclass
class TaskTemplate:
    """Template for generating tasks"""
    name: str
    description: str
    task_type: TaskType
    growth_stage: GrowthStage
    days_from_stage_start: int
    frequency_days: int
    priority: str
    estimated_duration: int  # minutes
    required_materials: List[str]
    instructions: str

class IntelligentTaskGenerator:
    """Automated task generation system"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.task_templates = self._load_task_templates()
        
    def _load_task_templates(self) -> Dict[str, List[TaskTemplate]]:
        """Load task templates for different growing methods"""
        return {
            "hydroponic": self._get_hydroponic_templates(),
            "soil": self._get_soil_templates(),
            "aeroponic": self._get_aeroponic_templates()
        }
    
    def _get_hydroponic_templates(self) -> List[TaskTemplate]:
        """Get task templates for hydroponic growing"""
        return [
            # Germination Stage (0-14 days)
            TaskTemplate(
                name="Check Seed Germination",
                description="Monitor seeds for germination progress",
                task_type=TaskType.MONITORING,
                growth_stage=GrowthStage.GERMINATION,
                days_from_stage_start=1,
                frequency_days=1,
                priority="High",
                estimated_duration=5,
                required_materials=["Magnifying glass"],
                instructions="Check for root emergence and remove ungerminated seeds after 7 days"
            ),
            TaskTemplate(
                name="Maintain Germination Environment",
                description="Ensure proper temperature and humidity for germination",
                task_type=TaskType.ENVIRONMENTAL,
                growth_stage=GrowthStage.GERMINATION,
                days_from_stage_start=0,
                frequency_days=1,
                priority="Critical",
                estimated_duration=10,
                required_materials=["Thermometer", "Humidity gauge"],
                instructions="Maintain 75-80°F temperature and 80-90% humidity"
            ),
            
            # Seedling Stage (14-28 days)
            TaskTemplate(
                name="First Nutrient Solution",
                description="Introduce diluted nutrient solution for seedlings",
                task_type=TaskType.FEEDING,
                growth_stage=GrowthStage.SEEDLING,
                days_from_stage_start=3,
                frequency_days=7,
                priority="High",
                estimated_duration=15,
                required_materials=["Nutrient solution", "EC meter", "pH meter"],
                instructions="Use 25% strength nutrient solution, EC 0.8-1.2, pH 5.5-6.5"
            ),
            TaskTemplate(
                name="Transplant to Growing System",
                description="Move seedlings to main hydroponic system",
                task_type=TaskType.MAINTENANCE,
                growth_stage=GrowthStage.SEEDLING,
                days_from_stage_start=14,
                frequency_days=0,  # One-time task
                priority="Critical",
                estimated_duration=30,
                required_materials=["Net pots", "Growing medium", "Support clips"],
                instructions="Carefully transplant when 2-3 true leaves are present"
            ),
            
            # Vegetative Stage (28-56 days)
            TaskTemplate(
                name="Weekly Nutrient Solution Change",
                description="Replace nutrient solution for optimal growth",
                task_type=TaskType.FEEDING,
                growth_stage=GrowthStage.VEGETATIVE,
                days_from_stage_start=0,
                frequency_days=7,
                priority="Critical",
                estimated_duration=45,
                required_materials=["Fresh nutrients", "pH adjuster", "Clean water"],
                instructions="Full solution change, EC 1.2-1.6, pH 5.5-6.5"
            ),
            TaskTemplate(
                name="Prune Lower Leaves",
                description="Remove lower yellowing leaves to focus energy",
                task_type=TaskType.PRUNING,
                growth_stage=GrowthStage.VEGETATIVE,
                days_from_stage_start=14,
                frequency_days=14,
                priority="Medium",
                estimated_duration=20,
                required_materials=["Clean scissors", "Sanitizer"],
                instructions="Remove yellowing lower leaves and any dead growth"
            ),
            TaskTemplate(
                name="LST (Low Stress Training)",
                description="Bend and tie branches to optimize light exposure",
                task_type=TaskType.TRAINING,
                growth_stage=GrowthStage.VEGETATIVE,
                days_from_stage_start=21,
                frequency_days=7,
                priority="Medium",
                estimated_duration=25,
                required_materials=["Soft ties", "Clips"],
                instructions="Gently bend branches to create even canopy"
            ),
            
            # Flowering Stage (56-112 days)
            TaskTemplate(
                name="Switch to Flowering Nutrients",
                description="Change to flowering-specific nutrient formula",
                task_type=TaskType.FEEDING,
                growth_stage=GrowthStage.FLOWERING,
                days_from_stage_start=0,
                frequency_days=0,  # One-time switch
                priority="Critical",
                estimated_duration=30,
                required_materials=["Flowering nutrients", "pH adjuster"],
                instructions="Switch to high P-K flowering formula, reduce nitrogen"
            ),
            TaskTemplate(
                name="Monitor Flower Development",
                description="Check flowering progress and identify issues",
                task_type=TaskType.MONITORING,
                growth_stage=GrowthStage.FLOWERING,
                days_from_stage_start=7,
                frequency_days=3,
                priority="High",
                estimated_duration=15,
                required_materials=["Magnifying glass", "Notebook"],
                instructions="Check for pistil development, pollen sacs, or hermaphrodites"
            ),
            TaskTemplate(
                name="Defoliation for Light Penetration",
                description="Remove fan leaves blocking bud sites",
                task_type=TaskType.PRUNING,
                growth_stage=GrowthStage.FLOWERING,
                days_from_stage_start=21,
                frequency_days=0,  # One-time task
                priority="Medium",
                estimated_duration=45,
                required_materials=["Clean scissors", "Sanitizer"],
                instructions="Remove large fan leaves blocking light to lower bud sites"
            ),
            
            # Harvest Stage
            TaskTemplate(
                name="Check Trichome Development",
                description="Monitor trichomes for harvest readiness",
                task_type=TaskType.MONITORING,
                growth_stage=GrowthStage.HARVEST,
                days_from_stage_start=0,
                frequency_days=2,
                priority="Critical",
                estimated_duration=10,
                required_materials=["60x magnifying glass", "Jeweler's loupe"],
                instructions="Look for milky white trichomes with some amber"
            ),
            TaskTemplate(
                name="Harvest Plants",
                description="Cut and prepare plants for drying",
                task_type=TaskType.HARVESTING,
                growth_stage=GrowthStage.HARVEST,
                days_from_stage_start=7,
                frequency_days=0,  # One-time task
                priority="Critical",
                estimated_duration=120,
                required_materials=["Sharp scissors", "Gloves", "Drying racks"],
                instructions="Cut at base, trim fan leaves, hang to dry in controlled environment"
            )
        ]
    
    def _get_soil_templates(self) -> List[TaskTemplate]:
        """Get task templates for soil growing"""
        return [
            TaskTemplate(
                name="Water Check - Soil",
                description="Check soil moisture and water if needed",
                task_type=TaskType.WATERING,
                growth_stage=GrowthStage.VEGETATIVE,
                days_from_stage_start=0,
                frequency_days=2,
                priority="High",
                estimated_duration=10,
                required_materials=["Watering can", "Moisture meter"],
                instructions="Water when top inch of soil is dry"
            ),
            # Add more soil-specific templates...
        ]
    
    def _get_aeroponic_templates(self) -> List[TaskTemplate]:
        """Get task templates for aeroponic growing"""
        return [
            TaskTemplate(
                name="Check Spray Nozzles",
                description="Ensure all spray nozzles are functioning",
                task_type=TaskType.MAINTENANCE,
                growth_stage=GrowthStage.VEGETATIVE,
                days_from_stage_start=0,
                frequency_days=3,
                priority="Critical",
                estimated_duration=15,
                required_materials=["Cleaning tools", "Replacement nozzles"],
                instructions="Clean or replace any clogged nozzles"
            ),
            # Add more aeroponic-specific templates...
        ]
    
    def generate_tasks_for_garden(self, garden_id: int) -> List[Dict[str, Any]]:
        """Generate tasks for a specific garden based on its current state"""
        try:
            # Get garden information
            garden_info = self._get_garden_info(garden_id)
            if not garden_info:
                logger.error(f"Garden {garden_id} not found")
                return []
            
            # Get current growth stage and days since planting
            current_stage = self._determine_growth_stage(garden_info)
            days_since_planting = self._calculate_days_since_planting(garden_info)
            
            # Get templates for growing method
            method = garden_info.get('growing_method', 'hydroponic').lower()
            templates = self.task_templates.get(method, self.task_templates['hydroponic'])
            
            # Generate tasks based on current stage
            generated_tasks = []
            for template in templates:
                if self._should_generate_task(template, current_stage, days_since_planting, garden_id):
                    task = self._create_task_from_template(template, garden_id, garden_info)
                    generated_tasks.append(task)
            
            logger.info(f"Generated {len(generated_tasks)} tasks for garden {garden_id}")
            return generated_tasks
            
        except Exception as e:
            logger.error(f"Error generating tasks for garden {garden_id}: {e}")
            return []
    
    def _get_garden_info(self, garden_id: int) -> Optional[Dict[str, Any]]:
        """Get garden information from database"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id, name, growing_method, plant_type, planted_date, 
                           current_stage, stage_start_date
                    FROM gardens 
                    WHERE id = ? AND is_active = 1
                """, (garden_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'name': row[1],
                        'growing_method': row[2],
                        'plant_type': row[3],
                        'planted_date': row[4],
                        'current_stage': row[5],
                        'stage_start_date': row[6]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error getting garden info: {e}")
            return None
    
    def _determine_growth_stage(self, garden_info: Dict[str, Any]) -> GrowthStage:
        """Determine current growth stage based on days since planting"""
        days_since_planting = self._calculate_days_since_planting(garden_info)
        
        # Default growth stage progression (can be customized per plant type)
        if days_since_planting < 7:
            return GrowthStage.GERMINATION
        elif days_since_planting < 21:
            return GrowthStage.SEEDLING
        elif days_since_planting < 56:
            return GrowthStage.VEGETATIVE
        elif days_since_planting < 112:
            return GrowthStage.FLOWERING
        else:
            return GrowthStage.HARVEST
    
    def _calculate_days_since_planting(self, garden_info: Dict[str, Any]) -> int:
        """Calculate days since garden was planted"""
        planted_date = datetime.fromisoformat(garden_info['planted_date'])
        return (datetime.now() - planted_date).days
    
    def _should_generate_task(self, template: TaskTemplate, current_stage: GrowthStage, 
                            days_since_planting: int, garden_id: int) -> bool:
        """Determine if a task should be generated based on template and garden state"""
        
        # Check if we're in the correct growth stage
        if template.growth_stage != current_stage:
            return False
        
        # Check if it's the right time to generate this task
        stage_days = self._calculate_days_in_current_stage(current_stage, days_since_planting)
        if stage_days < template.days_from_stage_start:
            return False
        
        # For recurring tasks, check if enough time has passed since last occurrence
        if template.frequency_days > 0:
            last_task = self._get_last_similar_task(garden_id, template.name)
            if last_task:
                days_since_last = (datetime.now() - datetime.fromisoformat(last_task['created_date'])).days
                if days_since_last < template.frequency_days:
                    return False
        
        # For one-time tasks, check if already completed
        elif template.frequency_days == 0:
            if self._task_already_exists(garden_id, template.name):
                return False
        
        return True
    
    def _calculate_days_in_current_stage(self, stage: GrowthStage, total_days: int) -> int:
        """Calculate how many days we've been in the current growth stage"""
        # Simplified calculation - in real implementation, this would use stage_start_date
        stage_starts = {
            GrowthStage.GERMINATION: 0,
            GrowthStage.SEEDLING: 7,
            GrowthStage.VEGETATIVE: 21,
            GrowthStage.FLOWERING: 56,
            GrowthStage.HARVEST: 112
        }
        
        return total_days - stage_starts.get(stage, 0)
    
    def _get_last_similar_task(self, garden_id: int, task_name: str) -> Optional[Dict[str, Any]]:
        """Get the most recent similar task for frequency checking"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT created_date FROM tasks
                    WHERE garden_id = ? AND title LIKE ?
                    ORDER BY created_date DESC LIMIT 1
                """, (garden_id, f"%{task_name}%"))
                
                row = cursor.fetchone()
                return {'created_date': row[0]} if row else None
                
        except Exception as e:
            logger.error(f"Error getting last similar task: {e}")
            return None
    
    def _task_already_exists(self, garden_id: int, task_name: str) -> bool:
        """Check if a one-time task already exists"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM tasks
                    WHERE garden_id = ? AND title = ?
                """, (garden_id, task_name))
                
                count = cursor.fetchone()[0]
                return count > 0
                
        except Exception as e:
            logger.error(f"Error checking task existence: {e}")
            return False
    
    def _create_task_from_template(self, template: TaskTemplate, garden_id: int, 
                                 garden_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create a task dictionary from template"""
        
        # Calculate due date based on template timing
        due_date = datetime.now() + timedelta(days=1)  # Default to tomorrow
        
        # Create detailed description with instructions
        full_description = f"{template.description}\n\n"
        full_description += f"Instructions: {template.instructions}\n"
        
        if template.required_materials:
            full_description += f"Required materials: {', '.join(template.required_materials)}\n"
        
        full_description += f"Estimated duration: {template.estimated_duration} minutes"
        
        return {
            'title': f"{template.name} - {garden_info['name']}",
            'description': full_description,
            'garden_id': garden_id,
            'task_type': template.task_type.value,
            'priority': template.priority,
            'due_date': due_date.isoformat(),
            'estimated_duration': template.estimated_duration,
            'is_completed': False,
            'created_date': datetime.now().isoformat(),
            'auto_generated': True
        }
    
    def generate_tasks_for_all_gardens(self) -> int:
        """Generate tasks for all active gardens"""
        total_generated = 0
        
        try:
            # Get all active gardens
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("SELECT id FROM gardens WHERE is_active = 1")
                gardens = cursor.fetchall()
            
            for garden in gardens:
                garden_id = garden[0]
                tasks = self.generate_tasks_for_garden(garden_id)
                
                # Save generated tasks to database
                for task in tasks:
                    self._save_task_to_database(task)
                    total_generated += 1
            
            logger.info(f"Generated {total_generated} total tasks for all gardens")
            return total_generated
            
        except Exception as e:
            logger.error(f"Error generating tasks for all gardens: {e}")
            return 0
    
    def _save_task_to_database(self, task: Dict[str, Any]) -> bool:
        """Save generated task to database"""
        try:
            with self.db_manager.get_connection() as conn:
                conn.execute("""
                    INSERT INTO tasks (title, description, garden_id, task_type, priority, 
                                     due_date, estimated_duration, is_completed, created_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    task['title'], task['description'], task['garden_id'],
                    task['task_type'], task['priority'], task['due_date'],
                    task['estimated_duration'], task['is_completed'], task['created_date']
                ))
                conn.commit()
                
            logger.debug(f"Saved auto-generated task: {task['title']}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving task to database: {e}")
            return False
