"""
GrowMaster - Inventory Management & Product Suggestion System
Integrated with task scheduling and cost calculations
"""

# PRODUCT DATABASE WITH INTEGRATED SUGGESTIONS
PRODUCT_DATABASE = {
    "nutrients": {
        "general_hydroponics_flora_trio": {
            "brand": "General Hydroponics",
            "name": "Flora Series Trio",
            "type": "base_nutrients",
            "size_options": {
                "quart_set": {"size": "1qt each", "price": 45.99, "yields_gallons": 100},
                "gallon_set": {"size": "1gal each", "price": 159.99, "yields_gallons": 400}
            },
            "usage_rate": {
                "seedling": {"micro": 2, "grow": 2, "bloom": 1},  # ml per gallon
                "vegetative": {"micro": 5, "grow": 10, "bloom": 5},
                "flowering": {"micro": 5, "grow": 5, "bloom": 10}
            },
            "compatible_systems": ["hydroponic", "coco", "soil"],
            "manufacturer_links": {
                "official": "https://generalhydroponics.com/flora-series",
                "retailers": ["amazon", "grow_store_local", "hydroponics_store"]
            },
            "reviews": {
                "rating": 4.7,
                "pros": ["Consistent results", "Wide availability", "Good for beginners"],
                "cons": ["Multiple bottles", "Can be expensive long-term"]
            }
        },
        "advanced_nutrients_ph_perfect": {
            "brand": "Advanced Nutrients",
            "name": "pH Perfect Grow/Micro/Bloom",
            "type": "base_nutrients",
            "size_options": {
                "500ml_set": {"size": "500ml each", "price": 89.99, "yields_gallons": 50},
                "1L_set": {"size": "1L each", "price": 149.99, "yields_gallons": 100}
            },
            "special_features": ["pH_auto_adjust", "premium_grade"],
            "usage_rate": {
                "vegetative": {"micro": 4, "grow": 4, "bloom": 4},
                "flowering": {"micro": 4, "grow": 4, "bloom": 4}
            }
        }
    },
    
    "lighting": {
        "mars_hydro_ts_1000": {
            "brand": "Mars Hydro",
            "name": "TS 1000",
            "type": "led_full_spectrum",
            "price": 139.99,
            "specifications": {
                "actual_power": 150,
                "ppfd": 645,
                "coverage": {"veg": "3x3", "flower": "2x2"},
                "spectrum": "full_spectrum_white"
            },
            "energy_cost_per_month": 32.40,  # @ $0.12/kWh, 18hrs/day
            "lifespan_hours": 50000,
            "recommended_for": ["2-4_plants", "beginner_friendly"]
        },
        "hlg_550_v2": {
            "brand": "Horticulture Lighting Group",
            "name": "HLG 550 V2",
            "type": "quantum_board_led",
            "price": 699.99,
            "specifications": {
                "actual_power": 480,
                "ppfd": 1152,
                "coverage": {"veg": "5x5", "flower": "4x4"},
                "spectrum": "3000k_with_660nm_red"
            },
            "energy_cost_per_month": 103.68,
            "recommended_for": ["4-9_plants", "commercial_grade"]
        }
    },
    
    "growing_medium": {
        "foxfarm_ocean_forest": {
            "brand": "FoxFarm",
            "name": "Ocean Forest Potting Soil",
            "type": "pre_fertilized_soil",
            "size_options": {
                "1.5_cubic_feet": {"size": "1.5 cu ft", "price": 19.99, "plants_supported": 2},
                "3_cubic_feet": {"size": "3.0 cu ft", "price": 34.99, "plants_supported": 4}
            },
            "ph_range": (6.3, 6.8),
            "feeding_schedule": "nutrients_after_3_weeks",
            "recommended_for": ["soil_growing", "beginner_friendly"]
        }
    },
    
    "supplements": {
        "cal_mag_plus": {
            "brand": "General Hydroponics",
            "name": "CALiMAGic",
            "type": "calcium_magnesium_supplement",
            "price": 24.99,
            "size": "1_gallon",
            "usage_rate": 5,  # ml per gallon
            "when_to_use": ["hydroponic", "coco", "ro_water", "led_lights"]
        }
    },
    
    "testing_equipment": {
        "apera_ph20": {
            "brand": "Apera Instruments",
            "name": "PH20 pH Meter",
            "type": "digital_ph_meter",
            "price": 49.99,
            "accuracy": "±0.1 pH",
            "calibration": "2_point_automatic",
            "essential_for": ["hydroponic", "nutrient_mixing"]
        }
    }
}

# INVENTORY MANAGEMENT SYSTEM
class InventoryManager:
    def __init__(self):
        self.current_inventory = {}
        self.consumption_tracking = {}
        self.low_stock_alerts = {}
        
    def track_consumption(self, product_id, amount_used, date, task_type):
        """Track product usage for predictive restocking"""
        if product_id not in self.consumption_tracking:
            self.consumption_tracking[product_id] = []
            
        self.consumption_tracking[product_id].append({
            "date": date,
            "amount": amount_used,
            "task": task_type,
            "remaining_stock": self.current_inventory.get(product_id, 0)
        })
        
        # Update current inventory
        if product_id in self.current_inventory:
            self.current_inventory[product_id] -= amount_used
            
    def predict_usage(self, product_id, days_ahead=30):
        """Predict future usage based on grow schedule and historical data"""
        if product_id not in self.consumption_tracking:
            return 0
            
        # Calculate average daily usage
        history = self.consumption_tracking[product_id]
        if len(history) < 3:
            return 0
            
        total_usage = sum(entry["amount"] for entry in history[-10:])  # Last 10 uses
        days_span = (history[-1]["date"] - history[-10]["date"]).days if len(history) >= 10 else 30
        
        daily_average = total_usage / max(days_span, 1)
        return daily_average * days_ahead
        
    def get_restock_recommendations(self):
        """Generate smart restocking recommendations"""
        recommendations = []
        
        for product_id, current_stock in self.current_inventory.items():
            predicted_usage = self.predict_usage(product_id, 30)
            
            if current_stock < predicted_usage * 1.2:  # 20% safety margin
                recommendations.append({
                    "product_id": product_id,
                    "current_stock": current_stock,
                    "predicted_usage_30_days": predicted_usage,
                    "recommended_quantity": predicted_usage * 2,  # 60 day supply
                    "urgency": "high" if current_stock < predicted_usage * 0.5 else "medium"
                })
                
        return recommendations

# SMART PRODUCT SUGGESTIONS SYSTEM
class ProductSuggestionEngine:
    def __init__(self, grow_method, plant_count, experience_level, budget_range):
        self.grow_method = grow_method
        self.plant_count = plant_count
        self.experience_level = experience_level
        self.budget_range = budget_range
        
    def suggest_complete_setup(self):
        """Suggest complete product setup based on grow parameters"""
        suggestions = {
            "essential": [],
            "recommended": [],
            "optional": [],
            "total_cost": 0
        }
        
        # Base nutrients suggestion
        if self.grow_method == "hydroponic":
            if self.experience_level == "beginner":
                suggestions["essential"].append({
                    "product": PRODUCT_DATABASE["nutrients"]["general_hydroponics_flora_trio"],
                    "reason": "Beginner-friendly with proven results",
                    "size_recommendation": "quart_set" if self.plant_count <= 4 else "gallon_set"
                })
            else:
                suggestions["essential"].append({
                    "product": PRODUCT_DATABASE["nutrients"]["advanced_nutrients_ph_perfect"],
                    "reason": "Auto pH adjustment saves time for experienced growers",
                    "size_recommendation": "1L_set"
                })
                
        # Lighting suggestions
        if self.plant_count <= 4:
            suggestions["essential"].append({
                "product": PRODUCT_DATABASE["lighting"]["mars_hydro_ts_1000"],
                "reason": "Perfect coverage for small grows, energy efficient"
            })
        else:
            suggestions["recommended"].append({
                "product": PRODUCT_DATABASE["lighting"]["hlg_550_v2"],
                "reason": "Commercial grade, higher PPFD for better yields"
            })
            
        # Supplements based on grow method
        if self.grow_method in ["hydroponic", "coco"]:
            suggestions["recommended"].append({
                "product": PRODUCT_DATABASE["supplements"]["cal_mag_plus"],
                "reason": "Essential for hydro/coco to prevent deficiencies"
            })
            
        # Testing equipment
        suggestions["essential"].append({
            "product": PRODUCT_DATABASE["testing_equipment"]["apera_ph20"],
            "reason": "Accurate pH monitoring critical for nutrient uptake"
        })
        
        return suggestions
        
    def suggest_for_task(self, task_type, current_grow_stage):
        """Suggest products needed for specific tasks"""
        suggestions = []
        
        if task_type == "feeding":
            if current_grow_stage == "vegetative":
                suggestions.append({
                    "product_type": "base_nutrients",
                    "specific_need": "high_nitrogen_formula",
                    "products": [p for p in PRODUCT_DATABASE["nutrients"].values() 
                               if "vegetative" in p.get("usage_rate", {})]
                })
                
        elif task_type == "pH_adjustment":
            suggestions.append({
                "product_type": "pH_control",
                "products": ["pH_up", "pH_down", "pH_meter"],
                "note": "Essential for nutrient uptake optimization"
            })
            
        return suggestions

# TASK-INVENTORY INTEGRATION
class TaskInventoryIntegration:
    def __init__(self, inventory_manager, product_db):
        self.inventory = inventory_manager
        self.products = product_db
        
    def check_task_feasibility(self, scheduled_tasks):
        """Check if inventory supports upcoming tasks"""
        feasibility_report = []
        
        for task in scheduled_tasks:
            required_products = self.get_products_for_task(task)
            
            for product_id, amount_needed in required_products.items():
                current_stock = self.inventory.current_inventory.get(product_id, 0)
                
                if current_stock < amount_needed:
                    feasibility_report.append({
                        "task": task,
                        "blocked_by": product_id,
                        "needed": amount_needed,
                        "available": current_stock,
                        "shortage": amount_needed - current_stock
                    })
                    
        return feasibility_report
        
    def auto_generate_shopping_list(self, next_30_days_tasks):
        """Generate shopping list based on upcoming tasks"""
        shopping_list = {}
        
        for task in next_30_days_tasks:
            required_products = self.get_products_for_task(task)
            
            for product_id, amount in required_products.items():
                if product_id in shopping_list:
                    shopping_list[product_id] += amount
                else:
                    shopping_list[product_id] = amount
                    
        # Add restock recommendations
        restock_recs = self.inventory.get_restock_recommendations()
        for rec in restock_recs:
            product_id = rec["product_id"]
            if product_id in shopping_list:
                shopping_list[product_id] = max(shopping_list[product_id], 
                                              rec["recommended_quantity"])
            else:
                shopping_list[product_id] = rec["recommended_quantity"]
                
        return shopping_list
        
    def get_products_for_task(self, task):
        """Map tasks to required products and quantities"""
        product_requirements = {}
        
        task_type = task.get("type", "")
        plant_count = task.get("plant_count", 1)
        
        if "feeding" in task_type.lower():
            # Calculate nutrient amounts needed
            grow_stage = task.get("growth_stage", "vegetative")
            if grow_stage == "vegetative":
                product_requirements["flora_trio_micro"] = 5 * plant_count  # ml
                product_requirements["flora_trio_grow"] = 10 * plant_count
                product_requirements["flora_trio_bloom"] = 5 * plant_count
                
        elif "ph" in task_type.lower():
            product_requirements["ph_test_solution"] = 1  # ml
            
        return product_requirements

# COST OPTIMIZATION WITH INVENTORY
def optimize_product_costs(grow_plan, budget_constraint):
    """Suggest cost-effective product alternatives"""
    suggestions = []
    
    # Analyze cost per gram/yield ratio
    for product_category in ["nutrients", "lighting"]:
        products = PRODUCT_DATABASE.get(product_category, {})
        
        cost_effectiveness = []
        for product_id, product_data in products.items():
            if product_category == "nutrients":
                # Calculate cost per gallon of nutrient solution
                size_data = product_data["size_options"]["quart_set"]
                cost_per_gallon = size_data["price"] / size_data["yields_gallons"]
                cost_effectiveness.append({
                    "product_id": product_id,
                    "cost_per_unit": cost_per_gallon,
                    "product": product_data
                })
                
        # Sort by cost effectiveness
        cost_effectiveness.sort(key=lambda x: x["cost_per_unit"])
        
        suggestions.append({
            "category": product_category,
            "most_cost_effective": cost_effectiveness[0],
            "alternatives": cost_effectiveness[1:3]
        })
        
    return suggestions

print("Inventory Management & Product Suggestion System Preview")
print("Features: Smart restocking, task-based suggestions, cost optimization")
