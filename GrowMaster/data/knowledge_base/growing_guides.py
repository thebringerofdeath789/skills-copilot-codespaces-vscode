"""
GrowMaster Pro - Growing Knowledge Database
Comprehensive growing information from educational sources
Based on "The Marijuana Bible", University Extensions, and Professional Resources
"""

from datetime import date, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GrowingKnowledge:
    """Comprehensive growing knowledge database"""
    
    def __init__(self):
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Initialize comprehensive growing knowledge database"""
        
        # Environmental Requirements by Plant Type and Growing Method
        self.environmental_requirements = {
            "cannabis": {
                "general": {
                    "temperature": {
                        "seedling": {"day": (75, 80), "night": (65, 70)},
                        "vegetative": {"day": (75, 85), "night": (65, 75)},
                        "flowering": {"day": (70, 80), "night": (60, 70)},
                        "optimal_range": (75, 82)
                    },
                    "humidity": {
                        "seedling": (65, 80),
                        "vegetative": (55, 70),
                        "flowering": (40, 50),
                        "late_flower": (30, 40)
                    },
                    "ph_levels": {
                        "soil": (6.0, 7.0),
                        "hydroponic": (5.5, 6.5),
                        "coco_coir": (5.8, 6.2)
                    },
                    "light_requirements": {
                        "seedling": {"ppfd": (100, 300), "hours": 18},
                        "vegetative": {"ppfd": (300, 600), "hours": 18},
                        "flowering": {"ppfd": (600, 1000), "hours": 12}
                    }
                }
            },
            "tomatoes": {
                "general": {
                    "temperature": {"day": (70, 75), "night": (60, 65)},
                    "humidity": (50, 70),
                    "ph_levels": {"soil": (6.0, 6.8), "hydroponic": (5.5, 6.5)}
                }
            },
            "lettuce": {
                "general": {
                    "temperature": {"day": (65, 70), "night": (55, 60)},
                    "humidity": (45, 65),
                    "ph_levels": {"soil": (6.0, 7.0), "hydroponic": (5.5, 6.5)}
                }
            }
        }
        
        # Growth Stage Timelines and Tasks
        self.growth_stages = {
            "cannabis_photoperiod": {
                "germination": {
                    "duration_days": (3, 10),
                    "conditions": {"temp": 78, "humidity": 80, "light_hours": 0},
                    "tasks": [
                        {"day": 1, "task": "Place seeds in germination medium", "priority": "critical"},
                        {"day": 3, "task": "Check for taproot emergence", "priority": "high"},
                        {"day": 5, "task": "Monitor moisture levels", "priority": "high"},
                        {"day": 7, "task": "Plant sprouted seeds if ready", "priority": "critical"}
                    ]
                },
                "seedling": {
                    "duration_days": (14, 21),
                    "conditions": {"temp": 75, "humidity": 70, "light_hours": 18},
                    "tasks": [
                        {"day": 1, "task": "Provide gentle light (100-200 PPFD)", "priority": "critical"},
                        {"day": 3, "task": "First watering with pH 6.0", "priority": "high"},
                        {"day": 7, "task": "Check for first true leaves", "priority": "medium"},
                        {"day": 10, "task": "Begin light nutrients (0.2-0.5 EC)", "priority": "medium"},
                        {"day": 14, "task": "Monitor for stretching", "priority": "medium"}
                    ]
                },
                "vegetative": {
                    "duration_days": (28, 84),
                    "conditions": {"temp": 78, "humidity": 60, "light_hours": 18},
                    "tasks": [
                        {"week": 1, "task": "Increase light to 300-400 PPFD", "priority": "critical"},
                        {"week": 2, "task": "Begin training (LST/topping)", "priority": "high"},
                        {"week": 3, "task": "Full strength vegetative nutrients", "priority": "critical"},
                        {"week": 4, "task": "Defoliation if needed", "priority": "medium"},
                        {"week": 6, "task": "Prepare for flowering transition", "priority": "high"}
                    ]
                },
                "flowering": {
                    "duration_days": (49, 84),
                    "conditions": {"temp": 75, "humidity": 45, "light_hours": 12},
                    "phases": {
                        "transition": {
                            "weeks": (1, 2),
                            "tasks": [
                                {"day": 1, "task": "Switch to 12/12 light cycle", "priority": "critical"},
                                {"day": 3, "task": "Begin flowering nutrients", "priority": "critical"},
                                {"day": 7, "task": "Remove lower growth", "priority": "high"},
                                {"day": 14, "task": "Monitor for sex determination", "priority": "critical"}
                            ]
                        },
                        "early_flower": {
                            "weeks": (3, 5),
                            "tasks": [
                                {"week": 3, "task": "Increase P-K nutrients", "priority": "critical"},
                                {"week": 4, "task": "Support heavy branches", "priority": "high"},
                                {"week": 5, "task": "Monitor for deficiencies", "priority": "high"}
                            ]
                        },
                        "late_flower": {
                            "weeks": (6, 8),
                            "tasks": [
                                {"week": 6, "task": "Reduce nitrogen", "priority": "critical"},
                                {"week": 7, "task": "Check trichomes weekly", "priority": "critical"},
                                {"week": 8, "task": "Begin flush if ready", "priority": "critical"}
                            ]
                        }
                    }
                }
            }
        }
        
        # Nutrient Recipes and Feeding Schedules
        self.nutrient_profiles = {
            "lucas_formula": {
                "description": "Simplified hydroponic nutrient regimen",
                "base_nutrients": {"micro": 8, "bloom": 16, "grow": 0},
                "additives": {"cal_mag": 5, "silica": 2},
                "growth_stage_modifications": {
                    "seedling": {"ratio": 0.25, "ec": (0.3, 0.6)},
                    "vegetative": {"ratio": 0.75, "ec": (0.8, 1.2)},
                    "early_flower": {"ratio": 1.0, "ec": (1.2, 1.6)},
                    "late_flower": {"ratio": 1.25, "ec": (1.4, 1.8)}
                }
            },
            "general_hydroponics_flora": {
                "description": "Three-part nutrient system",
                "ratios": {
                    "aggressive_vegetative": {"micro": 9, "grow": 9, "bloom": 6},
                    "transition": {"micro": 6, "grow": 9, "bloom": 12},
                    "aggressive_bloom": {"micro": 6, "grow": 6, "bloom": 15}
                }
            }
        }
        
        # Integrated Pest Management Database
        self.pest_management = {
            "common_pests": {
                "spider_mites": {
                    "identification": ["Fine webbing", "Yellow stippling on leaves", "Tiny moving dots"],
                    "prevention": ["Maintain humidity 50-60%", "Good air circulation", "Regular inspection"],
                    "organic_treatments": ["Neem oil spray", "Predatory mites", "Insecticidal soap"],
                    "application_schedule": "Every 3 days for 2 weeks",
                    "environmental_conditions": "Apply in evening, avoid high temps"
                },
                "aphids": {
                    "identification": ["Small soft-bodied insects", "Honeydew deposits", "Curled leaves"],
                    "prevention": ["Companion planting", "Regular inspection", "Beneficial insects"],
                    "organic_treatments": ["Ladybugs release", "Neem oil", "Soap spray"],
                    "application_schedule": "Weekly until controlled"
                },
                "fungus_gnats": {
                    "identification": ["Small flying insects", "Larvae in soil", "Adults around plants"],
                    "prevention": ["Allow soil to dry between waterings", "Yellow sticky traps"],
                    "treatments": ["Beneficial nematodes", "Mosquito dunks", "Diatomaceous earth"]
                }
            },
            "diseases": {
                "powdery_mildew": {
                    "identification": ["White powdery coating on leaves", "Reduced photosynthesis"],
                    "prevention": ["Good air circulation", "Avoid overhead watering", "Proper spacing"],
                    "treatments": ["Milk spray (1:10 ratio)", "Potassium bicarbonate", "UV light"],
                    "environmental_control": "Reduce humidity below 50%"
                },
                "bud_rot": {
                    "identification": ["Brown, mushy buds", "Gray mold", "Sweet smell"],
                    "prevention": ["Low humidity in flower", "Good air circulation", "Proper pruning"],
                    "immediate_action": "Remove affected areas immediately"
                }
            }
        }
        
        # Product Database from Educational Sources
        self.product_database = {
            "nutrients": {
                "general_hydroponics_flora_series": {
                    "type": "base_nutrients",
                    "components": ["FloraGro", "FloraBloom", "FloraMicro"],
                    "mixing_ratios": {"seedling": (0.5, 0.5, 1), "veg": (2, 1, 3), "flower": (1, 3, 2)},
                    "source": "The Marijuana Bible",
                    "application_method": "Dilute in water, pH adjust to 5.5-6.5"
                },
                "advanced_nutrients_ph_perfect": {
                    "type": "base_nutrients", 
                    "components": ["Grow", "Micro", "Bloom"],
                    "auto_ph": True,
                    "mixing_ratios": {"equal_parts": (1, 1, 1)},
                    "source": "Manufacturer specifications"
                }
            },
            "growing_media": {
                "foxfarm_ocean_forest": {
                    "type": "soil",
                    "ph_range": (6.3, 6.8),
                    "nutrient_content": "Pre-charged with organic nutrients",
                    "feeding_schedule": "Water only first 3-4 weeks",
                    "source": "University extension recommendations"
                },
                "general_hydroponics_rapid_rooter": {
                    "type": "starter_plugs",
                    "ph_neutral": True,
                    "application": "Seed starting and cloning",
                    "transplant_timing": "When roots emerge from sides"
                }
            }
        }
        
        # Cost Analysis Templates
        self.cost_templates = {
            "indoor_2x4_tent": {
                "setup_costs": {
                    "tent": 150, "led_light": 300, "ventilation": 200,
                    "growing_medium": 50, "nutrients": 100, "misc_equipment": 200
                },
                "recurring_costs": {
                    "electricity_per_month": 60, "nutrients_per_grow": 30, "water_per_grow": 10
                },
                "capacity": {"max_plants": 4, "cycle_duration": 120}
            }
        }
    
    def get_environmental_requirements(self, plant_type: str, growth_stage: str) -> Dict:
        """Get environmental requirements for specific plant and stage"""
        try:
            return self.environmental_requirements[plant_type]["general"]
        except KeyError:
            logger.warning(f"Environmental data not found for {plant_type}")
            return {}
    
    def get_growth_stage_tasks(self, plant_type: str, growth_stage: str) -> List[Dict]:
        """Get tasks for specific growth stage"""
        try:
            stage_key = f"{plant_type}_photoperiod"  # Default to photoperiod
            return self.growth_stages[stage_key][growth_stage]["tasks"]
        except KeyError:
            logger.warning(f"Growth stage tasks not found for {plant_type} - {growth_stage}")
            return []
    
    def get_nutrient_recipe(self, recipe_name: str, growth_stage: str) -> Dict:
        """Get nutrient mixing recipe for specific stage"""
        try:
            recipe = self.nutrient_profiles[recipe_name]
            if "growth_stage_modifications" in recipe:
                stage_mod = recipe["growth_stage_modifications"].get(growth_stage, {})
                return {**recipe, **stage_mod}
            return recipe
        except KeyError:
            logger.warning(f"Nutrient recipe not found: {recipe_name}")
            return {}
    
    def get_pest_treatment_plan(self, pest_name: str) -> Dict:
        """Get treatment plan for specific pest"""
        return self.pest_management.get("common_pests", {}).get(pest_name, {})
    
    def generate_feeding_schedule(self, plant_count: int, growth_stage: str, 
                                nutrient_recipe: str = "lucas_formula") -> List[Dict]:
        """Generate feeding schedule based on parameters"""
        recipe = self.get_nutrient_recipe(nutrient_recipe, growth_stage)
        schedule = []
        
        # Generate weekly feeding tasks
        for week in range(1, 13):  # 12 week cycle
            if growth_stage == "vegetative" and week <= 8:
                task = {
                    "week": week,
                    "task": f"Feed {plant_count} plants - Vegetative nutrients",
                    "recipe": recipe,
                    "notes": f"EC: {recipe.get('ec', (1.0, 1.4))[0]}-{recipe.get('ec', (1.0, 1.4))[1]}"
                }
                schedule.append(task)
        
        return schedule

# Global knowledge base instance
growing_knowledge = GrowingKnowledge()
