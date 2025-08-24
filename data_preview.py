"""
GrowMaster - Growing Knowledge Database Preview
Based on: The Marijuana Bible, University Extensions, Grower Forums, Manufacturer Guides
"""

# Sample of comprehensive growing database structure
GROWING_DATABASE_PREVIEW = {
    
    # ENVIRONMENTAL CONDITIONS
    "environmental_requirements": {
        "cannabis_indica": {
            "temperature": {
                "vegetative": {"day": (75, 85), "night": (65, 75), "unit": "°F"},
                "flowering": {"day": (70, 80), "night": (60, 70), "unit": "°F"},
                "optimal_range": (75, 82)
            },
            "humidity": {
                "seedling": (65, 80),
                "vegetative": (55, 70), 
                "flowering": (40, 50),  # Lower to prevent mold
                "late_flower": (30, 40)
            },
            "ph_levels": {
                "soil": (6.0, 7.0),
                "hydroponic": (5.5, 6.5),
                "coco_coir": (5.5, 6.5)
            },
            "light_requirements": {
                "seedling": {"ppfd": (100, 300), "hours": 18},
                "vegetative": {"ppfd": (300, 600), "hours": 18},
                "flowering": {"ppfd": (600, 1000), "hours": 12}
            }
        },
        "tomatoes": {
            "temperature": {
                "day": (70, 75), "night": (60, 65),
                "fruiting": (65, 75)
            },
            "humidity": (50, 70),
            "ph_levels": {"soil": (6.0, 6.8), "hydroponic": (5.5, 6.5)}
        }
    },

    # GROWTH STAGES & TIMELINES
    "growth_stages": {
        "cannabis_photoperiod": {
            "germination": {
                "duration_days": (3, 10),
                "conditions": {"temp": 78, "humidity": 80, "light_hours": 0},
                "tasks": [
                    {"day": 1, "task": "Place seeds in germination medium", "priority": "high"},
                    {"day": 3, "task": "Check for taproot emergence", "priority": "medium"},
                    {"day": 5, "task": "Plant sprouted seeds", "priority": "high"}
                ]
            },
            "seedling": {
                "duration_days": (14, 21),
                "conditions": {"temp": 75, "humidity": 70, "light_hours": 18},
                "tasks": [
                    {"day": 1, "task": "Provide gentle light (100-200 PPFD)", "priority": "high"},
                    {"day": 3, "task": "First watering with pH 6.0", "priority": "high"},
                    {"day": 7, "task": "Check for first true leaves", "priority": "medium"},
                    {"day": 14, "task": "Begin light nutrients (0.2-0.5 EC)", "priority": "medium"}
                ]
            },
            "vegetative": {
                "duration_days": (28, 84),  # 4-12 weeks flexible
                "conditions": {"temp": 78, "humidity": 60, "light_hours": 18},
                "tasks": [
                    {"week": 1, "task": "Increase light to 300-400 PPFD", "priority": "high"},
                    {"week": 2, "task": "Begin training (LST/topping)", "priority": "medium"},
                    {"week": 3, "task": "Full strength vegetative nutrients", "priority": "high"},
                    {"week": 4, "task": "Defoliation if needed", "priority": "low"}
                ],
                "feeding_schedule": {
                    "frequency": "every_2_days",
                    "nutrients": {
                        "nitrogen": "high",
                        "phosphorus": "medium", 
                        "potassium": "medium",
                        "cal_mag": "required"
                    }
                }
            },
            "flowering": {
                "duration_days": (49, 84),  # 7-12 weeks
                "conditions": {"temp": 75, "humidity": 45, "light_hours": 12},
                "phases": {
                    "transition": {
                        "weeks": (1, 2),
                        "tasks": [
                            {"day": 1, "task": "Switch to 12/12 light cycle", "priority": "critical"},
                            {"day": 3, "task": "Begin flowering nutrients", "priority": "high"},
                            {"day": 7, "task": "Remove lower growth", "priority": "medium"}
                        ]
                    },
                    "early_flower": {
                        "weeks": (3, 5),
                        "tasks": [
                            {"week": 3, "task": "Increase P-K nutrients", "priority": "high"},
                            {"week": 4, "task": "Support heavy branches", "priority": "medium"},
                            {"week": 5, "task": "Monitor for deficiencies", "priority": "high"}
                        ]
                    },
                    "late_flower": {
                        "weeks": (6, 8),
                        "tasks": [
                            {"week": 6, "task": "Reduce nitrogen", "priority": "high"},
                            {"week": 7, "task": "Check trichomes weekly", "priority": "critical"},
                            {"week": 8, "task": "Begin flush if ready", "priority": "high"}
                        ]
                    }
                }
            },
            "harvest": {
                "indicators": [
                    "Trichomes 20-30% amber",
                    "Pistils 70-80% brown",
                    "Fan leaves yellowing naturally"
                ],
                "tasks": [
                    {"day": -7, "task": "Begin final flush", "priority": "critical"},
                    {"day": 0, "task": "Harvest at optimal time", "priority": "critical"},
                    {"day": 1, "task": "Hang dry in controlled environment", "priority": "high"}
                ]
            },
            "curing": {
                "duration_days": (14, 30),
                "conditions": {"temp": 68, "humidity": 62},
                "tasks": [
                    {"day": 1, "task": "Trim and jar when stems snap", "priority": "high"},
                    {"day": 3, "task": "First burp - check moisture", "priority": "high"},
                    {"day": 7, "task": "Daily burping routine", "priority": "medium"},
                    {"day": 14, "task": "Weekly burping", "priority": "low"}
                ]
            }
        }
    },

    # NUTRIENT RECIPES & CALCULATIONS
    "nutrient_profiles": {
        "cannabis_hydro_lucas_formula": {
            "base_nutrients": {
                "micro": 8,  # ml/gal
                "bloom": 16,  # ml/gal
                "grow": 0    # Lucas formula uses only micro + bloom
            },
            "additives": {
                "cal_mag": 5,
                "silica": 2,
                "beneficial_bacteria": 2
            },
            "growth_stage_modifications": {
                "seedling": {"ratio": 0.25, "ec": (0.3, 0.6)},
                "vegetative": {"ratio": 0.75, "ec": (0.8, 1.2)},
                "early_flower": {"ratio": 1.0, "ec": (1.2, 1.6)},
                "late_flower": {"ratio": 1.25, "ec": (1.4, 1.8)}
            }
        },
        "general_hydroponics_flora_series": {
            "ratios": {
                "aggressive_vegetative": {"micro": 9, "grow": 9, "bloom": 6},
                "transition": {"micro": 6, "grow": 9, "bloom": 12},
                "aggressive_bloom": {"micro": 6, "grow": 6, "bloom": 15}
            }
        }
    },

    # LIGHTING SCHEDULES
    "lighting_schedules": {
        "photoperiod_standard": {
            "vegetative": {"hours_on": 18, "hours_off": 6},
            "flowering": {"hours_on": 12, "hours_off": 12}
        },
        "light_deprivation": {
            "natural_trigger": "cover_at_7pm_uncover_at_7am",
            "duration": "2_weeks_minimum"
        },
        "autoflower": {
            "full_cycle": {"hours_on": 20, "hours_off": 4}
        }
    },

    # PROBLEM DIAGNOSIS
    "problem_diagnosis": {
        "nutrient_deficiencies": {
            "nitrogen": {
                "symptoms": ["Lower leaves yellowing", "Slow growth", "Light green color"],
                "solution": "Increase nitrogen-rich nutrients",
                "stages_affected": ["vegetative"]
            },
            "phosphorus": {
                "symptoms": ["Purple stems", "Dark leaf tips", "Slow flower development"],
                "solution": "Increase P-K nutrients",
                "stages_affected": ["flowering"]
            }
        },
        "environmental_issues": {
            "light_burn": {
                "symptoms": ["Top leaves bleaching", "Crispy leaf edges"],
                "solution": "Increase light distance or reduce intensity"
            },
            "heat_stress": {
                "symptoms": ["Leaf curl up", "Wilting despite wet soil"],
                "solution": "Improve ventilation, reduce temperature"
            }
        }
    },

    # COST CALCULATIONS
    "cost_templates": {
        "indoor_2x4_tent": {
            "setup_costs": {
                "tent": 150,
                "led_light": 300,
                "ventilation": 200,
                "growing_medium": 50,
                "nutrients": 100,
                "misc_equipment": 200
            },
            "recurring_costs": {
                "electricity_per_month": 60,
                "nutrients_per_grow": 30,
                "water_per_grow": 10
            },
            "capacity": "4_plants",
            "cycle_duration": 120
        }
    }
}

# AUTOMATED TASK GENERATION LOGIC
def generate_grow_tasks(plant_type, grow_method, start_date, plant_count):
    """
    Automatically generates comprehensive task list based on:
    - Plant type and characteristics
    - Growing method (soil, hydro, etc.)
    - Environmental requirements
    - Feeding schedules
    - Training requirements
    """
    tasks = []
    
    # Get plant profile
    plant_profile = GROWING_DATABASE_PREVIEW["growth_stages"][plant_type]
    
    # Generate stage-based tasks
    for stage, stage_data in plant_profile.items():
        if stage == "germination":
            for task_data in stage_data["tasks"]:
                tasks.append({
                    "date": start_date + timedelta(days=task_data["day"]),
                    "task": task_data["task"],
                    "priority": task_data["priority"],
                    "stage": stage,
                    "plant_count": plant_count
                })
    
    return tasks

# SMART RECOMMENDATIONS SYSTEM
def get_smart_recommendations(current_conditions, plant_stage, issues=None):
    """
    Provides contextual recommendations based on:
    - Current environmental conditions
    - Plant growth stage
    - Any reported problems
    - Historical data
    """
    recommendations = []
    
    if current_conditions["humidity"] > 60 and plant_stage == "flowering":
        recommendations.append({
            "type": "warning",
            "message": "High humidity during flowering increases mold risk",
            "action": "Reduce humidity to 40-50% and increase air circulation",
            "priority": "high"
        })
    
    return recommendations

print("GrowMaster Database Preview - This shows the comprehensive knowledge base structure")
print("Features comprehensive information from multiple professional sources")
