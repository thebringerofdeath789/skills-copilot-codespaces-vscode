"""
Product and Supplier Database
Comprehensive database of growing supplies, equipment, and pricing
Educational resource compilation for cost analysis and planning
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class ProductDatabase:
    """Comprehensive product and pricing database"""
    
    def __init__(self):
        self.load_product_database()
    
    def load_product_database(self):
        """Initialize comprehensive product database"""
        
        # LED Lighting Systems
        self.lighting_systems = {
            "spider_farmer_sf1000": {
                "type": "quantum_board",
                "wattage": 100,
                "coverage": {"vegetative": "3x3", "flowering": "2x2"},
                "ppfd_max": 1017,
                "price_range": (120, 150),
                "efficiency": "2.7 umol/J",
                "spectrum": "full_spectrum",
                "dimmer": True,
                "lifespan_hours": 50000
            },
            "mars_hydro_ts1000": {
                "type": "quantum_board", 
                "wattage": 150,
                "coverage": {"vegetative": "3x3", "flowering": "2.5x2.5"},
                "ppfd_max": 1076,
                "price_range": (130, 160),
                "efficiency": "2.3 umol/J"
            },
            "hlg_135_v2": {
                "type": "quantum_board",
                "wattage": 135,
                "coverage": {"vegetative": "3x3", "flowering": "2x2.5"},
                "price_range": (180, 220),
                "efficiency": "2.5 umol/J",
                "quality_tier": "premium"
            }
        }
        
        # Growing Tents and Enclosures
        self.tent_systems = {
            "vivosun_2x4x5": {
                "dimensions": {"width": 24, "depth": 48, "height": 60},
                "material": "600D mylar",
                "price_range": (80, 120),
                "plant_capacity": {"small": 6, "medium": 4, "large": 2},
                "ventilation_ports": 4,
                "observation_window": True
            },
            "ac_infinity_cloudlab_2x4": {
                "dimensions": {"width": 24, "depth": 48, "height": 72},
                "material": "1680D canvas",
                "price_range": (150, 200),
                "premium_features": ["reinforced_poles", "tool_pockets", "thick_canvas"],
                "plant_capacity": {"small": 8, "medium": 4, "large": 2}
            }
        }
        
        # Ventilation and Climate Control
        self.ventilation_systems = {
            "ac_infinity_cloudline_t4": {
                "cfm_rating": 205,
                "noise_level": "quiet",
                "speed_control": "automatic",
                "price_range": (100, 130),
                "duct_size": 4,
                "controller_included": True
            },
            "vivosun_4inch_inline": {
                "cfm_rating": 190,
                "price_range": (40, 60),
                "speed_control": "manual",
                "duct_size": 4,
                "budget_option": True
            }
        }
        
        # Growing Media Options
        self.growing_media = {
            "foxfarm_ocean_forest": {
                "type": "organic_soil",
                "bag_size_cu_ft": 1.5,
                "price_range": (15, 20),
                "ph_range": (6.3, 6.8),
                "nutrient_charge": "3-4_weeks",
                "ingredients": ["composted_bark", "sphagnum_moss", "perlite", "earthworm_castings"]
            },
            "foxfarm_happy_frog": {
                "type": "organic_soil",
                "bag_size_cu_ft": 2.0,
                "price_range": (12, 18),
                "ph_range": (6.3, 6.8),
                "nutrient_charge": "2-3_weeks",
                "gentler_option": True
            },
            "coco_coir_compressed": {
                "type": "soilless_medium",
                "expansion_ratio": "1:7",
                "price_range": (8, 15),
                "ph_range": (5.8, 6.2),
                "requires_calmag": True,
                "reusable": True
            },
            "perlite_coarse": {
                "type": "amendment",
                "bag_size_cu_ft": 2.0,
                "price_range": (10, 15),
                "use": "drainage_improvement"
            }
        }
        
        # Nutrient Systems
        self.nutrient_systems = {
            "general_hydroponics_flora_trio": {
                "components": ["FloraGro", "FloraBloom", "FloraMicro"],
                "bottle_size": "1_quart",
                "price_range": (25, 35),
                "makes_gallons": 189,
                "cost_per_gallon": 0.18,
                "ph_adjustment_needed": True
            },
            "foxfarm_trio": {
                "components": ["Grow_Big", "Big_Bloom", "Tiger_Bloom"],
                "bottle_size": "1_pint",
                "price_range": (25, 30),
                "organic_based": True,
                "soil_focused": True
            },
            "advanced_nutrients_ph_perfect": {
                "components": ["Grow", "Micro", "Bloom"],
                "bottle_size": "1_liter",
                "price_range": (35, 50),
                "auto_ph_buffering": True,
                "premium_option": True
            }
        }
        
        # Monitoring Equipment
        self.monitoring_equipment = {
            "apera_ph20": {
                "type": "ph_meter",
                "accuracy": "±0.1_ph",
                "price_range": (35, 45),
                "waterproof": True,
                "calibration_required": True
            },
            "hanna_ec_tds": {
                "type": "ec_tds_meter",
                "price_range": (25, 35),
                "auto_temperature_compensation": True,
                "waterproof": True
            },
            "govee_hygrometer": {
                "type": "temperature_humidity",
                "price_range": (8, 15),
                "bluetooth_connectivity": True,
                "data_logging": True,
                "app_alerts": True
            },
            "pulse_one": {
                "type": "environmental_monitor",
                "measurements": ["temp", "humidity", "vpd", "light", "co2"],
                "price_range": (200, 250),
                "wifi_connectivity": True,
                "professional_grade": True
            }
        }
        
        # Complete Setup Packages
        self.setup_packages = {
            "beginner_2x4_complete": {
                "tent": "vivosun_2x4x5",
                "light": "spider_farmer_sf1000",
                "ventilation": "vivosun_4inch_inline",
                "growing_medium": "foxfarm_happy_frog",
                "nutrients": "foxfarm_trio",
                "monitoring": ["apera_ph20", "govee_hygrometer"],
                "total_cost_range": (400, 550),
                "plant_capacity": 4,
                "experience_level": "beginner"
            },
            "intermediate_2x4_complete": {
                "tent": "ac_infinity_cloudlab_2x4",
                "light": "mars_hydro_ts1000", 
                "ventilation": "ac_infinity_cloudline_t4",
                "growing_medium": "foxfarm_ocean_forest",
                "nutrients": "general_hydroponics_flora_trio",
                "monitoring": ["apera_ph20", "hanna_ec_tds", "govee_hygrometer"],
                "total_cost_range": (600, 800),
                "plant_capacity": 4,
                "experience_level": "intermediate"
            }
        }
        
        # Recurring Supply Costs
        self.recurring_costs = {
            "electricity": {
                "led_100w_18_hour_cycle": {"monthly_kwh": 54, "cost_per_kwh": 0.12, "monthly_cost": 6.48},
                "led_150w_12_hour_cycle": {"monthly_kwh": 54, "cost_per_kwh": 0.12, "monthly_cost": 6.48},
                "ventilation_fan_24_hour": {"monthly_kwh": 36, "cost_per_kwh": 0.12, "monthly_cost": 4.32}
            },
            "consumables_per_cycle": {
                "nutrients_4_plants": {"cost": 25, "frequency": "per_cycle"},
                "ph_adjustment": {"cost": 5, "frequency": "per_cycle"},
                "growing_medium_refresh": {"cost": 40, "frequency": "every_2_cycles"}
            }
        }
        
        # Supplier Information
        self.suppliers = {
            "amazon": {
                "shipping": "prime_2_day",
                "return_policy": "30_days",
                "price_tier": "competitive",
                "availability": "high"
            },
            "grow_generation": {
                "specialization": "hydroponic_supplies",
                "shipping": "standard",
                "expertise": "high",
                "price_tier": "msrp"
            },
            "buildasoil": {
                "specialization": "organic_amendments",
                "shipping": "standard_heavy",
                "expertise": "organic_focus",
                "price_tier": "premium"
            }
        }
    
    def get_product_info(self, category: str, product_id: str) -> Optional[Dict]:
        """Get detailed product information"""
        category_mapping = {
            "lighting": self.lighting_systems,
            "tents": self.tent_systems,
            "ventilation": self.ventilation_systems,
            "media": self.growing_media,
            "nutrients": self.nutrient_systems,
            "monitoring": self.monitoring_equipment
        }
        
        if category in category_mapping:
            return category_mapping[category].get(product_id)
        return None
    
    def calculate_setup_cost(self, package_name: str) -> Dict:
        """Calculate detailed setup costs for a package"""
        package = self.setup_packages.get(package_name)
        if not package:
            return {}
        
        cost_breakdown = {}
        total_min = 0
        total_max = 0
        
        # Calculate individual component costs
        for component_type, product_id in package.items():
            if component_type in ["total_cost_range", "plant_capacity", "experience_level"]:
                continue
                
            if isinstance(product_id, list):
                # Handle multiple monitoring devices
                component_cost_min = 0
                component_cost_max = 0
                for item in product_id:
                    product = self.get_product_info("monitoring", item)
                    if product and "price_range" in product:
                        component_cost_min += product["price_range"][0]
                        component_cost_max += product["price_range"][1]
                cost_breakdown[component_type] = (component_cost_min, component_cost_max)
            else:
                # Single component
                for category in ["lighting", "tents", "ventilation", "media", "nutrients"]:
                    product = self.get_product_info(category, product_id)
                    if product and "price_range" in product:
                        cost_breakdown[component_type] = product["price_range"]
                        break
        
        # Calculate totals
        for cost_range in cost_breakdown.values():
            if isinstance(cost_range, tuple):
                total_min += cost_range[0]
                total_max += cost_range[1]
        
        return {
            "breakdown": cost_breakdown,
            "total_range": (total_min, total_max),
            "package_info": package
        }
    
    def get_monthly_operating_costs(self, setup_type: str = "intermediate_2x4_complete") -> Dict:
        """Calculate monthly operating costs"""
        electricity_costs = 0
        
        # LED lighting costs
        electricity_costs += self.recurring_costs["electricity"]["led_150w_12_hour_cycle"]["monthly_cost"]
        
        # Ventilation costs  
        electricity_costs += self.recurring_costs["electricity"]["ventilation_fan_24_hour"]["monthly_cost"]
        
        # Prorated consumable costs
        cycle_costs = sum([item["cost"] for item in self.recurring_costs["consumables_per_cycle"].values() 
                          if item["frequency"] == "per_cycle"])
        monthly_consumable_cost = cycle_costs / 4  # 4 month cycle average
        
        return {
            "electricity": electricity_costs,
            "consumables": monthly_consumable_cost,
            "total_monthly": electricity_costs + monthly_consumable_cost
        }

# Global product database instance
product_database = ProductDatabase()
