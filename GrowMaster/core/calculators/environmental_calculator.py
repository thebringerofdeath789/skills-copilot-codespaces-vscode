"""
Environmental Calculator System
VPD, climate control, and environmental optimization calculations
"""

from typing import Dict, List, Tuple, Optional
import math
import logging

logger = logging.getLogger(__name__)

class EnvironmentalCalculator:
    """Advanced environmental calculation system"""
    
    def __init__(self):
        self.load_environmental_data()
    
    def load_environmental_data(self):
        """Initialize environmental calculation parameters"""
        
        # Optimal VPD ranges by growth stage (kPa)
        self.vpd_ranges = {
            "seedling": {"min": 0.4, "optimal": 0.6, "max": 0.8},
            "vegetative": {"min": 0.8, "optimal": 1.0, "max": 1.2},
            "flowering": {"min": 1.0, "optimal": 1.2, "max": 1.4}
        }
        
        # Temperature and humidity ranges by stage
        self.climate_ranges = {
            "seedling": {
                "temperature": {"day": (75, 80), "night": (65, 70)},
                "humidity": {"min": 65, "max": 80}
            },
            "vegetative": {
                "temperature": {"day": (75, 85), "night": (65, 75)},
                "humidity": {"min": 55, "max": 70}
            },
            "flowering": {
                "temperature": {"day": (70, 80), "night": (60, 70)},
                "humidity": {"min": 40, "max": 50}
            }
        }
        
        # Air exchange requirements (CFM per cubic foot)
        self.air_exchange_rates = {
            "passive_intake": 1.0,  # 1 air exchange per minute minimum
            "active_exhaust": 1.5,  # 1.5 air exchanges per minute optimal
            "high_performance": 2.0  # 2+ air exchanges for CO2 supplementation
        }
        
        # CO2 levels and effects
        self.co2_levels = {
            "ambient": 400,  # Typical outdoor CO2 (ppm)
            "optimal_natural": 600,  # Indoor without supplementation
            "enhanced": 1000,  # With CO2 supplementation
            "maximum_safe": 1500  # Upper limit for plant health
        }
    
    def calculate_vpd(self, temperature_f: float, relative_humidity: float) -> Dict:
        """Calculate Vapor Pressure Deficit"""
        
        # Convert Fahrenheit to Celsius
        temp_c = (temperature_f - 32) * 5/9
        
        # Calculate saturated vapor pressure using Antoine equation
        # es = 0.6108 * exp(17.27 * T / (T + 237.3))
        es_kpa = 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
        
        # Calculate actual vapor pressure
        ea_kpa = es_kpa * (relative_humidity / 100)
        
        # Calculate VPD
        vpd_kpa = es_kpa - ea_kpa
        
        return {
            "temperature_f": temperature_f,
            "temperature_c": round(temp_c, 1),
            "relative_humidity": relative_humidity,
            "saturated_vapor_pressure_kpa": round(es_kpa, 3),
            "actual_vapor_pressure_kpa": round(ea_kpa, 3),
            "vpd_kpa": round(vpd_kpa, 2),
            "vpd_rating": self._rate_vpd(vpd_kpa)
        }
    
    def _rate_vpd(self, vpd: float) -> str:
        """Rate VPD value for plant health"""
        if vpd < 0.4:
            return "too_low"
        elif vpd <= 0.8:
            return "good_for_seedlings"
        elif vpd <= 1.2:
            return "good_for_vegetative"
        elif vpd <= 1.4:
            return "good_for_flowering"
        else:
            return "too_high"
    
    def find_optimal_humidity(self, temperature_f: float, growth_stage: str) -> Dict:
        """Find optimal humidity for target VPD at given temperature"""
        
        target_vpd = self.vpd_ranges[growth_stage]["optimal"]
        temp_c = (temperature_f - 32) * 5/9
        
        # Calculate saturated vapor pressure
        es_kpa = 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
        
        # Calculate required actual vapor pressure for target VPD
        ea_required = es_kpa - target_vpd
        
        # Calculate required relative humidity
        rh_optimal = (ea_required / es_kpa) * 100
        
        # Get acceptable VPD range
        vpd_min = self.vpd_ranges[growth_stage]["min"]
        vpd_max = self.vpd_ranges[growth_stage]["max"]
        
        # Calculate humidity range for acceptable VPD
        ea_max = es_kpa - vpd_min
        ea_min = es_kpa - vpd_max
        rh_max = (ea_max / es_kpa) * 100
        rh_min = (ea_min / es_kpa) * 100
        
        return {
            "temperature_f": temperature_f,
            "growth_stage": growth_stage,
            "target_vpd": target_vpd,
            "optimal_humidity": round(max(0, min(100, rh_optimal)), 1),
            "humidity_range": {
                "min": round(max(0, min(100, rh_min)), 1),
                "max": round(max(0, min(100, rh_max)), 1)
            },
            "climate_recommendations": self._get_climate_recommendations(temperature_f, rh_optimal, growth_stage)
        }
    
    def _get_climate_recommendations(self, temp_f: float, humidity: float, stage: str) -> List[str]:
        """Get climate adjustment recommendations"""
        recommendations = []
        
        climate_range = self.climate_ranges[stage]
        
        # Temperature recommendations
        if temp_f < climate_range["temperature"]["day"][0]:
            recommendations.append("Increase temperature - too cool for optimal growth")
        elif temp_f > climate_range["temperature"]["day"][1]:
            recommendations.append("Decrease temperature - may cause stress")
        
        # Humidity recommendations
        if humidity < climate_range["humidity"]["min"]:
            recommendations.append("Increase humidity - air may be too dry")
        elif humidity > climate_range["humidity"]["max"]:
            recommendations.append("Decrease humidity - risk of mold/mildew")
        
        return recommendations
    
    def calculate_air_exchange(self, tent_width_ft: float, tent_depth_ft: float, 
                             tent_height_ft: float, target_exchange_rate: str = "active_exhaust") -> Dict:
        """Calculate required air exchange for grow space"""
        
        # Calculate tent volume
        volume_cubic_ft = tent_width_ft * tent_depth_ft * tent_height_ft
        
        # Get target air exchange rate
        exchange_rate = self.air_exchange_rates.get(target_exchange_rate, 1.5)
        
        # Calculate required CFM
        required_cfm = volume_cubic_ft * exchange_rate
        
        # Account for resistance (carbon filter, ducting)
        resistance_factor = 1.25  # 25% additional CFM for typical resistance
        recommended_cfm = required_cfm * resistance_factor
        
        # Fan sizing recommendations
        fan_sizes = {
            "4inch": {"cfm_range": (150, 250), "suitable": recommended_cfm <= 200},
            "6inch": {"cfm_range": (250, 450), "suitable": 200 < recommended_cfm <= 400},
            "8inch": {"cfm_range": (450, 800), "suitable": recommended_cfm > 400}
        }
        
        recommended_fan = None
        for size, specs in fan_sizes.items():
            if specs["suitable"]:
                recommended_fan = size
                break
        
        return {
            "tent_dimensions": {
                "width_ft": tent_width_ft,
                "depth_ft": tent_depth_ft,
                "height_ft": tent_height_ft,
                "volume_cubic_ft": round(volume_cubic_ft, 1)
            },
            "air_exchange": {
                "target_rate": target_exchange_rate,
                "exchanges_per_minute": exchange_rate,
                "required_cfm_base": round(required_cfm),
                "recommended_cfm_with_resistance": round(recommended_cfm),
                "recommended_fan_size": recommended_fan
            },
            "fan_options": fan_sizes
        }
    
    def calculate_dehumidification_needs(self, tent_volume_cubic_ft: float, 
                                       current_humidity: float, target_humidity: float,
                                       temperature_f: float) -> Dict:
        """Calculate dehumidification requirements"""
        
        if current_humidity <= target_humidity:
            return {"message": "No dehumidification needed", "current_humidity": current_humidity, "target_humidity": target_humidity}
        
        temp_c = (temperature_f - 32) * 5/9
        
        # Calculate saturated vapor pressure
        es_kpa = 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
        
        # Current and target actual vapor pressures
        current_ea = es_kpa * (current_humidity / 100)
        target_ea = es_kpa * (target_humidity / 100)
        
        # Excess moisture to remove (kPa)
        excess_moisture_kpa = current_ea - target_ea
        
        # Convert to practical units (approximate)
        # This is a simplified calculation - actual dehumidification needs are complex
        excess_moisture_pints_per_day = excess_moisture_kpa * tent_volume_cubic_ft * 0.5
        
        # Dehumidifier sizing
        if excess_moisture_pints_per_day <= 20:
            dehumidifier_size = "small"
            capacity_needed = "20-30 pint"
        elif excess_moisture_pints_per_day <= 40:
            dehumidifier_size = "medium"
            capacity_needed = "40-50 pint"
        else:
            dehumidifier_size = "large"
            capacity_needed = "60+ pint"
        
        return {
            "current_conditions": {
                "humidity": current_humidity,
                "temperature_f": temperature_f,
                "current_vpd": self.calculate_vpd(temperature_f, current_humidity)["vpd_kpa"]
            },
            "target_conditions": {
                "humidity": target_humidity,
                "target_vpd": self.calculate_vpd(temperature_f, target_humidity)["vpd_kpa"]
            },
            "dehumidification": {
                "excess_moisture_kpa": round(excess_moisture_kpa, 3),
                "estimated_daily_removal_pints": round(excess_moisture_pints_per_day, 1),
                "recommended_dehumidifier": dehumidifier_size,
                "capacity_needed": capacity_needed
            }
        }
    
    def calculate_co2_supplementation(self, tent_volume_cubic_ft: float, 
                                    target_co2_ppm: int = 1000,
                                    air_exchanges_per_hour: float = 60) -> Dict:
        """Calculate CO2 supplementation requirements"""
        
        if target_co2_ppm <= self.co2_levels["ambient"]:
            return {"message": "No CO2 supplementation needed for target level"}
        
        # CO2 loss rate due to air exchange
        volume_liters = tent_volume_cubic_ft * 28.317  # Convert to liters
        air_exchange_liters_per_hour = volume_liters * air_exchanges_per_hour
        
        # CO2 needed to maintain target level
        co2_deficit_ppm = target_co2_ppm - self.co2_levels["ambient"]
        co2_needed_liters_per_hour = (air_exchange_liters_per_hour * co2_deficit_ppm) / 1000000
        
        # Convert to practical units
        co2_needed_cubic_ft_per_hour = co2_needed_liters_per_hour / 28.317
        
        # Tank sizing (20 lb CO2 tank ≈ 300 cubic feet of CO2)
        tank_20lb_duration_hours = 300 / co2_needed_cubic_ft_per_hour if co2_needed_cubic_ft_per_hour > 0 else float('inf')
        
        return {
            "tent_volume_cubic_ft": tent_volume_cubic_ft,
            "target_co2_ppm": target_co2_ppm,
            "air_exchanges_per_hour": air_exchanges_per_hour,
            "co2_requirements": {
                "deficit_ppm": co2_deficit_ppm,
                "needed_liters_per_hour": round(co2_needed_liters_per_hour, 2),
                "needed_cubic_ft_per_hour": round(co2_needed_cubic_ft_per_hour, 3)
            },
            "tank_usage": {
                "20lb_tank_duration_hours": round(tank_20lb_duration_hours, 1) if tank_20lb_duration_hours != float('inf') else "N/A",
                "20lb_tank_duration_days": round(tank_20lb_duration_hours / 24, 1) if tank_20lb_duration_hours != float('inf') else "N/A",
                "estimated_monthly_cost": "50-100" if tank_20lb_duration_hours < 720 else "25-50"  # Rough estimate
            },
            "recommendations": self._get_co2_recommendations(target_co2_ppm, air_exchanges_per_hour)
        }
    
    def _get_co2_recommendations(self, target_ppm: int, air_exchanges: float) -> List[str]:
        """Get CO2 supplementation recommendations"""
        recommendations = []
        
        if target_ppm > self.co2_levels["maximum_safe"]:
            recommendations.append(f"Target CO2 ({target_ppm} ppm) exceeds safe limits. Reduce to {self.co2_levels['maximum_safe']} ppm or lower.")
        
        if air_exchanges > 120:  # 2 exchanges per minute
            recommendations.append("High air exchange rate will waste CO2. Consider reducing ventilation during CO2 supplementation.")
        
        if target_ppm >= 1000:
            recommendations.append("CO2 supplementation most effective with sealed room setup and controlled air exchange.")
            recommendations.append("Ensure adequate ventilation when room is occupied for safety.")
        
        return recommendations
    
    def environmental_troubleshooting(self, temperature_f: float, humidity: float, 
                                    growth_stage: str) -> Dict:
        """Comprehensive environmental troubleshooting"""
        
        vpd_calc = self.calculate_vpd(temperature_f, humidity)
        optimal_conditions = self.find_optimal_humidity(temperature_f, growth_stage)
        
        issues = []
        solutions = []
        
        # VPD analysis
        if vpd_calc["vpd_kpa"] < 0.4:
            issues.append("VPD too low - may slow transpiration and nutrient uptake")
            solutions.append("Increase temperature or decrease humidity")
        elif vpd_calc["vpd_kpa"] > 1.6:
            issues.append("VPD too high - may cause plant stress and wilting")
            solutions.append("Decrease temperature or increase humidity")
        
        # Temperature analysis
        climate_range = self.climate_ranges[growth_stage]
        if temperature_f < climate_range["temperature"]["day"][0]:
            issues.append("Temperature too low for optimal growth")
            solutions.append("Add heating or reduce air exchange rate")
        elif temperature_f > climate_range["temperature"]["day"][1]:
            issues.append("Temperature too high - may cause heat stress")
            solutions.append("Increase air exchange or add cooling")
        
        # Humidity analysis
        if humidity < climate_range["humidity"]["min"]:
            issues.append("Humidity too low - may cause nutrient deficiencies")
            solutions.append("Add humidifier or reduce air exchange")
        elif humidity > climate_range["humidity"]["max"]:
            issues.append("Humidity too high - risk of mold and mildew")
            solutions.append("Add dehumidifier or increase air exchange")
        
        return {
            "current_conditions": {
                "temperature_f": temperature_f,
                "humidity": humidity,
                "vpd": vpd_calc["vpd_kpa"],
                "growth_stage": growth_stage
            },
            "optimal_conditions": optimal_conditions,
            "issues_identified": issues,
            "recommended_solutions": solutions,
            "priority": "high" if len(issues) > 2 else "medium" if len(issues) > 0 else "low"
        }
