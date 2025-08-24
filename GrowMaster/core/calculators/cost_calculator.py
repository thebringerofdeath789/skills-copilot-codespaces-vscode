"""
Cost Calculator System
Comprehensive cost analysis and ROI calculations
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class CostCalculator:
    """Advanced cost calculation and analysis system"""
    
    def __init__(self):
        self.load_cost_data()
    
    def load_cost_data(self):
        """Initialize cost calculation parameters"""
        
        # Equipment categories and typical costs
        self.equipment_costs = {
            "grow_tent": {
                "2x2": {"min": 60, "avg": 80, "max": 120},
                "2x4": {"min": 80, "avg": 120, "max": 180},
                "4x4": {"min": 120, "avg": 180, "max": 280},
                "4x8": {"min": 200, "avg": 300, "max": 450}
            },
            "led_lighting": {
                "100w": {"min": 80, "avg": 120, "max": 180},
                "150w": {"min": 120, "avg": 180, "max": 250},
                "240w": {"min": 180, "avg": 280, "max": 400},
                "320w": {"min": 250, "avg": 380, "max": 550}
            },
            "ventilation": {
                "4inch_basic": {"min": 40, "avg": 70, "max": 120},
                "4inch_premium": {"min": 80, "avg": 130, "max": 200},
                "6inch_basic": {"min": 60, "avg": 100, "max": 160},
                "6inch_premium": {"min": 120, "avg": 200, "max": 300}
            },
            "growing_medium": {
                "soil_per_plant": {"min": 3, "avg": 5, "max": 8},
                "coco_per_plant": {"min": 2, "avg": 4, "max": 6},
                "hydroponic_per_plant": {"min": 5, "avg": 10, "max": 15}
            }
        }
        
        # Operating costs (per month)
        self.operating_costs = {
            "electricity": {
                "100w_light_18h": {"kwh": 54, "cost_range": (6.48, 11.88)},  # $0.12-0.22/kWh
                "150w_light_12h": {"kwh": 54, "cost_range": (6.48, 11.88)},
                "ventilation_24h": {"kwh": 36, "cost_range": (4.32, 7.92)}
            },
            "consumables": {
                "nutrients_per_plant_per_cycle": {"min": 5, "avg": 10, "max": 20},
                "ph_adjustment_per_cycle": {"min": 2, "avg": 5, "max": 10},
                "growing_medium_replacement": {"min": 3, "avg": 5, "max": 8}
            },
            "water": {
                "per_plant_per_cycle": {"gallons": 50, "cost_range": (0.50, 2.00)}
            }
        }
        
        # Market value estimates (educational purposes - varies by location)
        self.market_values = {
            "premium_flower": {"per_gram": (8, 12), "per_ounce": (224, 336)},
            "mid_grade_flower": {"per_gram": (5, 8), "per_ounce": (140, 224)},
            "trim_material": {"per_ounce": (20, 40)}
        }
        
        # Yield estimates by setup size and experience
        self.yield_estimates = {
            "2x2_tent": {
                "beginner": {"grams": (28, 56), "plants": 1},
                "intermediate": {"grams": (56, 112), "plants": 2},
                "advanced": {"grams": (84, 140), "plants": 2}
            },
            "2x4_tent": {
                "beginner": {"grams": (56, 140), "plants": 2},
                "intermediate": {"grams": (140, 280), "plants": 4},
                "advanced": {"grams": (280, 420), "plants": 4}
            },
            "4x4_tent": {
                "beginner": {"grams": (140, 280), "plants": 4},
                "intermediate": {"grams": (280, 560), "plants": 9},
                "advanced": {"grams": (560, 840), "plants": 9}
            }
        }
    
    def calculate_setup_costs(self, tent_size: str, lighting_wattage: str,
                            ventilation_tier: str = "4inch_basic",
                            growing_method: str = "soil") -> Dict:
        """Calculate initial setup costs for grow operation"""
        
        costs = {}
        total_min = 0
        total_max = 0
        
        # Tent costs
        if tent_size in self.equipment_costs["grow_tent"]:
            tent_cost = self.equipment_costs["grow_tent"][tent_size]
            costs["tent"] = tent_cost
            total_min += tent_cost["min"]
            total_max += tent_cost["max"]
        
        # Lighting costs
        if lighting_wattage in self.equipment_costs["led_lighting"]:
            light_cost = self.equipment_costs["led_lighting"][lighting_wattage]
            costs["lighting"] = light_cost
            total_min += light_cost["min"]
            total_max += light_cost["max"]
        
        # Ventilation costs
        if ventilation_tier in self.equipment_costs["ventilation"]:
            vent_cost = self.equipment_costs["ventilation"][ventilation_tier]
            costs["ventilation"] = vent_cost
            total_min += vent_cost["min"]
            total_max += vent_cost["max"]
        
        # Growing medium (estimate for max plant capacity)
        plant_capacity = self.yield_estimates.get(tent_size, {}).get("advanced", {}).get("plants", 4)
        medium_cost_per_plant = self.equipment_costs["growing_medium"][f"{growing_method}_per_plant"]
        medium_total_cost = {
            "min": medium_cost_per_plant["min"] * plant_capacity,
            "avg": medium_cost_per_plant["avg"] * plant_capacity,
            "max": medium_cost_per_plant["max"] * plant_capacity
        }
        costs["growing_medium"] = medium_total_cost
        total_min += medium_total_cost["min"]
        total_max += medium_total_cost["max"]
        
        # Additional equipment estimate (fans, timers, pH meter, etc.)
        additional_cost = {"min": 100, "avg": 200, "max": 400}
        costs["additional_equipment"] = additional_cost
        total_min += additional_cost["min"]
        total_max += additional_cost["max"]
        
        return {
            "setup_configuration": {
                "tent_size": tent_size,
                "lighting": lighting_wattage,
                "ventilation": ventilation_tier,
                "growing_method": growing_method,
                "estimated_plant_capacity": plant_capacity
            },
            "cost_breakdown": costs,
            "total_range": {"min": total_min, "avg": (total_min + total_max) / 2, "max": total_max},
            "cost_per_plant": {
                "min": round(total_min / plant_capacity, 2),
                "max": round(total_max / plant_capacity, 2)
            }
        }
    
    def calculate_operating_costs(self, lighting_schedule: str, plant_count: int,
                                cycles_per_year: int = 3, location_tier: str = "average") -> Dict:
        """Calculate annual operating costs"""
        
        # Electricity costs
        electricity_monthly = 0
        if "18h" in lighting_schedule:
            light_cost = self.operating_costs["electricity"]["100w_light_18h"]
            electricity_monthly += light_cost["cost_range"][0] if location_tier == "low" else light_cost["cost_range"][1]
        else:
            light_cost = self.operating_costs["electricity"]["150w_light_12h"]
            electricity_monthly += light_cost["cost_range"][0] if location_tier == "low" else light_cost["cost_range"][1]
        
        # Ventilation electricity
        vent_cost = self.operating_costs["electricity"]["ventilation_24h"]
        electricity_monthly += vent_cost["cost_range"][0] if location_tier == "low" else vent_cost["cost_range"][1]
        
        # Consumable costs per cycle
        nutrients_per_cycle = self.operating_costs["consumables"]["nutrients_per_plant_per_cycle"]["avg"] * plant_count
        ph_adjustment_per_cycle = self.operating_costs["consumables"]["ph_adjustment_per_cycle"]["avg"]
        medium_replacement = self.operating_costs["consumables"]["growing_medium_replacement"]["avg"] * plant_count
        
        consumables_per_cycle = nutrients_per_cycle + ph_adjustment_per_cycle + medium_replacement
        
        # Water costs per cycle
        water_per_cycle = self.operating_costs["water"]["per_plant_per_cycle"]["cost_range"][1] * plant_count
        
        # Annual calculations
        annual_electricity = electricity_monthly * 12
        annual_consumables = consumables_per_cycle * cycles_per_year
        annual_water = water_per_cycle * cycles_per_year
        annual_total = annual_electricity + annual_consumables + annual_water
        
        return {
            "plant_count": plant_count,
            "cycles_per_year": cycles_per_year,
            "monthly_costs": {
                "electricity": round(electricity_monthly, 2),
                "consumables_prorated": round(consumables_per_cycle / 4, 2),  # Assuming 4-month cycles
                "water_prorated": round(water_per_cycle / 4, 2)
            },
            "per_cycle_costs": {
                "consumables": round(consumables_per_cycle, 2),
                "water": round(water_per_cycle, 2)
            },
            "annual_costs": {
                "electricity": round(annual_electricity, 2),
                "consumables": round(annual_consumables, 2),
                "water": round(annual_water, 2),
                "total": round(annual_total, 2)
            },
            "cost_per_plant_per_year": round(annual_total / plant_count, 2)
        }
    
    def calculate_roi_analysis(self, setup_costs: Dict, operating_costs: Dict,
                             tent_size: str, experience_level: str = "intermediate") -> Dict:
        """Calculate ROI analysis including payback period"""
        
        # Get yield estimates
        yield_data = self.yield_estimates.get(tent_size, {}).get(experience_level, {})
        if not yield_data:
            return {"error": "Invalid tent size or experience level"}
        
        annual_yield_grams = (yield_data["grams"][0] + yield_data["grams"][1]) / 2 * operating_costs["cycles_per_year"]
        
        # Market value calculations (using mid-grade estimates)
        price_per_gram = (self.market_values["mid_grade_flower"]["per_gram"][0] + 
                         self.market_values["mid_grade_flower"]["per_gram"][1]) / 2
        annual_market_value = annual_yield_grams * price_per_gram
        
        # Calculate net profit
        total_setup_cost = setup_costs["total_range"]["avg"]
        annual_operating_cost = operating_costs["annual_costs"]["total"]
        annual_profit = annual_market_value - annual_operating_cost
        
        # Payback period
        payback_years = total_setup_cost / annual_profit if annual_profit > 0 else float('inf')
        
        # 3-year analysis
        three_year_profit = (annual_profit * 3) - total_setup_cost
        
        return {
            "setup_investment": round(total_setup_cost, 2),
            "annual_operating_costs": round(annual_operating_cost, 2),
            "yield_analysis": {
                "annual_yield_grams": round(annual_yield_grams, 1),
                "annual_yield_ounces": round(annual_yield_grams / 28.35, 1),
                "market_value_per_gram": round(price_per_gram, 2),
                "annual_market_value": round(annual_market_value, 2)
            },
            "profitability": {
                "annual_gross_profit": round(annual_market_value, 2),
                "annual_net_profit": round(annual_profit, 2),
                "profit_margin": round((annual_profit / annual_market_value) * 100, 1) if annual_market_value > 0 else 0,
                "payback_period_years": round(payback_years, 2) if payback_years != float('inf') else "N/A"
            },
            "three_year_projection": {
                "total_investment": round(total_setup_cost, 2),
                "total_operating_costs": round(annual_operating_cost * 3, 2),
                "total_market_value": round(annual_market_value * 3, 2),
                "net_profit": round(three_year_profit, 2),
                "roi_percentage": round((three_year_profit / total_setup_cost) * 100, 1) if total_setup_cost > 0 else 0
            },
            "cost_per_gram": {
                "setup_cost_per_gram": round(total_setup_cost / (annual_yield_grams * 3), 2),
                "operating_cost_per_gram": round(annual_operating_cost / annual_yield_grams, 2),
                "total_cost_per_gram": round((total_setup_cost / 3 + annual_operating_cost) / annual_yield_grams, 2)
            }
        }
    
    def compare_setup_options(self, tent_sizes: List[str], experience_level: str = "intermediate") -> Dict:
        """Compare multiple setup options for ROI"""
        
        comparisons = []
        
        for tent_size in tent_sizes:
            # Calculate costs for this setup
            setup_costs = self.calculate_setup_costs(tent_size, "150w", "4inch_basic", "soil")
            
            plant_count = self.yield_estimates.get(tent_size, {}).get(experience_level, {}).get("plants", 4)
            operating_costs = self.calculate_operating_costs("12h", plant_count, 3)
            
            roi_analysis = self.calculate_roi_analysis(setup_costs, operating_costs, tent_size, experience_level)
            
            comparisons.append({
                "tent_size": tent_size,
                "setup_cost": setup_costs["total_range"]["avg"],
                "annual_operating": operating_costs["annual_costs"]["total"],
                "annual_yield_grams": roi_analysis["yield_analysis"]["annual_yield_grams"],
                "annual_profit": roi_analysis["profitability"]["annual_net_profit"],
                "payback_years": roi_analysis["profitability"]["payback_period_years"],
                "three_year_roi": roi_analysis["three_year_projection"]["roi_percentage"],
                "cost_per_gram": roi_analysis["cost_per_gram"]["total_cost_per_gram"]
            })
        
        # Sort by ROI
        comparisons.sort(key=lambda x: x["three_year_roi"], reverse=True)
        
        return {
            "experience_level": experience_level,
            "comparison_results": comparisons,
            "best_roi": comparisons[0] if comparisons else None,
            "analysis_date": datetime.now().strftime("%Y-%m-%d")
        }
    
    def calculate_scaling_analysis(self, base_tent_size: str, scaling_factor: int) -> Dict:
        """Analyze costs and returns for scaling up operation"""
        
        base_setup = self.calculate_setup_costs(base_tent_size, "150w")
        base_plant_count = self.yield_estimates.get(base_tent_size, {}).get("intermediate", {}).get("plants", 4)
        
        # Scaled operation
        scaled_setup_cost = base_setup["total_range"]["avg"] * scaling_factor
        scaled_plant_count = base_plant_count * scaling_factor
        scaled_operating = self.calculate_operating_costs("12h", scaled_plant_count, 3)
        
        # Calculate efficiency gains (economies of scale)
        efficiency_factor = 1 - (0.1 * min(scaling_factor - 1, 5))  # Max 50% efficiency gain
        adjusted_operating_cost = scaled_operating["annual_costs"]["total"] * efficiency_factor
        
        # ROI comparison
        single_roi = self.calculate_roi_analysis(base_setup, 
                                                self.calculate_operating_costs("12h", base_plant_count, 3),
                                                base_tent_size)
        
        scaled_operating_adjusted = {**scaled_operating}
        scaled_operating_adjusted["annual_costs"]["total"] = adjusted_operating_cost
        
        scaled_roi = self.calculate_roi_analysis(
            {"total_range": {"avg": scaled_setup_cost}},
            scaled_operating_adjusted,
            base_tent_size
        )
        
        return {
            "base_operation": {
                "tent_count": 1,
                "setup_cost": base_setup["total_range"]["avg"],
                "annual_profit": single_roi["profitability"]["annual_net_profit"],
                "roi_3_year": single_roi["three_year_projection"]["roi_percentage"]
            },
            "scaled_operation": {
                "tent_count": scaling_factor,
                "setup_cost": scaled_setup_cost,
                "efficiency_gain": round((1 - efficiency_factor) * 100, 1),
                "annual_profit": scaled_roi["profitability"]["annual_net_profit"],
                "roi_3_year": scaled_roi["three_year_projection"]["roi_percentage"]
            },
            "scaling_benefits": {
                "profit_multiplier": round(scaled_roi["profitability"]["annual_net_profit"] / single_roi["profitability"]["annual_net_profit"], 2),
                "cost_efficiency_improvement": round(((1 - efficiency_factor) * 100), 1),
                "recommended": scaled_roi["three_year_projection"]["roi_percentage"] > single_roi["three_year_projection"]["roi_percentage"] * 1.2
            }
        }
