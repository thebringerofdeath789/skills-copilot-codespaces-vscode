"""
Nutrient Calculator System
Advanced nutrient mixing and EC/PPM calculations
Based on educational hydroponic principles
"""

from typing import Dict, List, Tuple, Optional
import math
import logging

logger = logging.getLogger(__name__)

class NutrientCalculator:
    """Advanced nutrient calculation system"""
    
    def __init__(self):
        self.load_nutrient_data()
    
    def load_nutrient_data(self):
        """Initialize nutrient calculation parameters"""
        
        # Nutrient solution recipes (mL per gallon)
        self.recipes = {
            "lucas_formula": {
                "micro": 8,
                "bloom": 16, 
                "grow": 0,
                "target_ec": {"seedling": 0.4, "vegetative": 1.2, "flowering": 1.6}
            },
            "gh_flora_aggressive_veg": {
                "micro": 9,
                "grow": 9,
                "bloom": 6,
                "target_ec": {"vegetative": 1.4}
            },
            "gh_flora_transition": {
                "micro": 6,
                "grow": 9,
                "bloom": 12,
                "target_ec": {"transition": 1.5}
            },
            "gh_flora_aggressive_bloom": {
                "micro": 6,
                "grow": 6,
                "bloom": 15,
                "target_ec": {"flowering": 1.8}
            }
        }
        
        # Nutrient salt concentrations (approximate EC contribution per mL/gal)
        self.nutrient_ec_factors = {
            "micro": 0.15,  # Approximate EC contribution per mL/gallon
            "grow": 0.12,
            "bloom": 0.14,
            "cal_mag": 0.18,
            "silica": 0.25
        }
        
        # Growth stage EC ranges
        self.ec_ranges = {
            "seedling": (0.3, 0.6),
            "vegetative": (0.8, 1.4),
            "early_flower": (1.2, 1.8),
            "late_flower": (1.4, 2.0),
            "flush": (0.0, 0.3)
        }
        
        # PPM conversion factors
        self.ppm_conversions = {
            "500_scale": 500,  # 500 scale (Eutech, Oakton)
            "700_scale": 700   # 700 scale (Hanna, TDS-3)
        }
    
    def calculate_recipe(self, recipe_name: str, volume_gallons: float, 
                        growth_stage: str = "vegetative") -> Dict:
        """Calculate nutrient amounts for given volume and recipe"""
        
        if recipe_name not in self.recipes:
            raise ValueError(f"Recipe '{recipe_name}' not found")
        
        recipe = self.recipes[recipe_name]
        
        # Calculate nutrient amounts
        nutrients = {}
        total_ec = 0
        
        for nutrient, ml_per_gallon in recipe.items():
            if nutrient in ["target_ec"]:
                continue
                
            ml_needed = ml_per_gallon * volume_gallons
            nutrients[nutrient] = {
                "ml_per_gallon": ml_per_gallon,
                "total_ml": ml_needed,
                "teaspoons": ml_needed / 4.929,  # 1 tsp = 4.929 mL
                "tablespoons": ml_needed / 14.787  # 1 tbsp = 14.787 mL
            }
            
            # Calculate EC contribution
            if nutrient in self.nutrient_ec_factors:
                total_ec += ml_per_gallon * self.nutrient_ec_factors[nutrient]
        
        # Get target EC for stage
        target_ec = recipe.get("target_ec", {}).get(growth_stage, 1.2)
        
        return {
            "recipe_name": recipe_name,
            "volume_gallons": volume_gallons,
            "growth_stage": growth_stage,
            "nutrients": nutrients,
            "calculated_ec": round(total_ec, 2),
            "target_ec": target_ec,
            "ec_match": abs(total_ec - target_ec) < 0.2,
            "ppm_500_scale": round(total_ec * 500),
            "ppm_700_scale": round(total_ec * 700)
        }
    
    def adjust_recipe_for_ec(self, recipe_name: str, target_ec: float, 
                           volume_gallons: float = 1.0) -> Dict:
        """Adjust recipe proportions to hit target EC"""
        
        base_recipe = self.calculate_recipe(recipe_name, 1.0)  # Calculate for 1 gallon first
        current_ec = base_recipe["calculated_ec"]
        
        if current_ec == 0:
            return {"error": "Cannot calculate EC adjustment - no base EC"}
        
        # Calculate scaling factor
        scale_factor = target_ec / current_ec
        
        # Apply scaling to nutrients
        adjusted_nutrients = {}
        for nutrient, data in base_recipe["nutrients"].items():
            adjusted_ml_per_gal = data["ml_per_gallon"] * scale_factor
            total_ml = adjusted_ml_per_gal * volume_gallons
            
            adjusted_nutrients[nutrient] = {
                "ml_per_gallon": round(adjusted_ml_per_gal, 1),
                "total_ml": round(total_ml, 1),
                "teaspoons": round(total_ml / 4.929, 1),
                "tablespoons": round(total_ml / 14.787, 1)
            }
        
        return {
            "recipe_name": f"{recipe_name}_adjusted",
            "volume_gallons": volume_gallons,
            "target_ec": target_ec,
            "scale_factor": round(scale_factor, 2),
            "nutrients": adjusted_nutrients,
            "ppm_500_scale": round(target_ec * 500),
            "ppm_700_scale": round(target_ec * 700)
        }
    
    def calculate_reservoir_change(self, current_volume: float, current_ec: float,
                                 target_volume: float, target_ec: float) -> Dict:
        """Calculate how to adjust existing reservoir"""
        
        if current_volume <= 0:
            return {"error": "Current volume must be greater than 0"}
        
        # Calculate current total dissolved solids (TDS equivalent)
        current_tds = current_ec * current_volume
        target_tds = target_ec * target_volume
        
        volume_to_add = target_volume - current_volume
        
        if volume_to_add > 0:
            # Need to add solution
            if target_tds > current_tds:
                # Need to add concentrated solution
                required_tds_addition = target_tds - current_tds
                required_ec_addition = required_tds_addition / volume_to_add
                
                return {
                    "action": "add_concentrated_solution",
                    "volume_to_add": volume_to_add,
                    "required_ec_of_addition": round(required_ec_addition, 2),
                    "ppm_of_addition_500": round(required_ec_addition * 500),
                    "instructions": f"Add {volume_to_add} gallons of solution at EC {required_ec_addition:.2f}"
                }
            else:
                # Need to add water/weak solution
                required_ec_addition = (target_tds - current_tds) / volume_to_add if volume_to_add > 0 else 0
                
                return {
                    "action": "add_water_or_weak_solution",
                    "volume_to_add": volume_to_add,
                    "required_ec_of_addition": max(0, round(required_ec_addition, 2)),
                    "instructions": f"Add {volume_to_add} gallons of {'water' if required_ec_addition <= 0 else f'weak solution (EC {required_ec_addition:.2f})'}"
                }
        
        elif volume_to_add < 0:
            # Need to remove solution
            volume_to_remove = abs(volume_to_add)
            return {
                "action": "remove_solution",
                "volume_to_remove": volume_to_remove,
                "instructions": f"Remove {volume_to_remove} gallons and replace with appropriate solution"
            }
        
        else:
            # Same volume, just adjust EC
            if target_ec > current_ec:
                return {
                    "action": "add_concentrated_nutrients",
                    "instructions": "Add concentrated nutrients to increase EC"
                }
            elif target_ec < current_ec:
                return {
                    "action": "dilute_with_water",
                    "instructions": "Add water to decrease EC"
                }
            else:
                return {
                    "action": "no_change_needed",
                    "instructions": "Solution is already at target parameters"
                }
    
    def calculate_deficiency_correction(self, deficiency_type: str, 
                                      volume_gallons: float) -> Dict:
        """Calculate nutrient additions to correct specific deficiencies"""
        
        corrections = {
            "nitrogen": {
                "nutrient": "cal_mag_plus",
                "ml_per_gallon": 5,
                "description": "Increase nitrogen-rich base nutrients"
            },
            "phosphorus": {
                "nutrient": "bloom_booster",
                "ml_per_gallon": 3,
                "description": "Add phosphorus supplement"
            },
            "potassium": {
                "nutrient": "potassium_silicate",
                "ml_per_gallon": 2,
                "description": "Add potassium supplement"
            },
            "calcium": {
                "nutrient": "cal_mag",
                "ml_per_gallon": 5,
                "description": "Add calcium-magnesium supplement"
            },
            "magnesium": {
                "nutrient": "cal_mag",
                "ml_per_gallon": 3,
                "description": "Add calcium-magnesium supplement"
            }
        }
        
        if deficiency_type not in corrections:
            return {"error": f"Unknown deficiency type: {deficiency_type}"}
        
        correction = corrections[deficiency_type]
        total_ml = correction["ml_per_gallon"] * volume_gallons
        
        return {
            "deficiency_type": deficiency_type,
            "nutrient": correction["nutrient"],
            "ml_per_gallon": correction["ml_per_gallon"],
            "total_ml": total_ml,
            "teaspoons": round(total_ml / 4.929, 1),
            "description": correction["description"],
            "volume_gallons": volume_gallons
        }
    
    def get_feeding_schedule_ec(self, growth_stage: str, week_number: int) -> float:
        """Get recommended EC based on growth stage and week"""
        
        stage_progressions = {
            "seedling": {"weeks": 2, "start_ec": 0.3, "end_ec": 0.6},
            "vegetative": {"weeks": 8, "start_ec": 0.6, "end_ec": 1.4},
            "flowering": {"weeks": 8, "start_ec": 1.4, "end_ec": 1.8},
            "flush": {"weeks": 1, "start_ec": 0.0, "end_ec": 0.0}
        }
        
        if growth_stage not in stage_progressions:
            return 1.2  # Default EC
        
        stage = stage_progressions[growth_stage]
        
        if week_number <= 0:
            return stage["start_ec"]
        elif week_number >= stage["weeks"]:
            return stage["end_ec"]
        else:
            # Linear interpolation between start and end EC
            progress = week_number / stage["weeks"]
            return stage["start_ec"] + (stage["end_ec"] - stage["start_ec"]) * progress
