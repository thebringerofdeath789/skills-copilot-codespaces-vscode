"""
Lighting Calculator System
PPFD, DLI, and energy efficiency calculations
"""

from typing import Dict, List, Tuple, Optional
import math
import logging

logger = logging.getLogger(__name__)

class LightingCalculator:
    """Advanced lighting calculation system"""
    
    def __init__(self):
        self.load_lighting_data()
    
    def load_lighting_data(self):
        """Initialize lighting calculation parameters"""
        
        # PPFD requirements by growth stage (μmol/m²/s)
        self.ppfd_requirements = {
            "seedling": {"min": 100, "optimal": 200, "max": 300},
            "vegetative": {"min": 300, "optimal": 500, "max": 800},
            "flowering": {"min": 600, "optimal": 800, "max": 1200}
        }
        
        # DLI requirements by growth stage (mol/m²/day)
        self.dli_requirements = {
            "seedling": {"min": 6, "optimal": 12, "max": 18},
            "vegetative": {"min": 20, "optimal": 35, "max": 50},
            "flowering": {"min": 35, "optimal": 45, "max": 65}
        }
        
        # Light fixture specifications
        self.fixture_specs = {
            "spider_farmer_sf1000": {
                "wattage": 100,
                "ppfd_center": 1017,
                "coverage_area_sq_ft": {"veg": 9, "flower": 4},
                "efficiency_umol_j": 2.7,
                "beam_angle": 120
            },
            "mars_hydro_ts1000": {
                "wattage": 150,
                "ppfd_center": 1076,
                "coverage_area_sq_ft": {"veg": 9, "flower": 6.25},
                "efficiency_umol_j": 2.3
            },
            "hlg_135_v2": {
                "wattage": 135,
                "ppfd_center": 900,
                "coverage_area_sq_ft": {"veg": 9, "flower": 6.25},
                "efficiency_umol_j": 2.5
            }
        }
        
        # Energy costs (varies by location)
        self.energy_costs = {
            "us_average": 0.12,  # $/kWh
            "california": 0.22,
            "texas": 0.11,
            "new_york": 0.18
        }
    
    def calculate_ppfd_coverage(self, fixture_name: str, hanging_height: int, 
                               coverage_area_sq_ft: float) -> Dict:
        """Calculate PPFD coverage for given fixture and setup"""
        
        if fixture_name not in self.fixture_specs:
            raise ValueError(f"Fixture '{fixture_name}' not found in database")
        
        fixture = self.fixture_specs[fixture_name]
        
        # PPFD decreases with distance and area (inverse square law approximation)
        # This is simplified - real PPFD maps are more complex
        
        # Base PPFD at 18" height
        base_height = 18
        height_factor = (base_height / hanging_height) ** 2
        
        # Area dilution factor
        recommended_area = fixture["coverage_area_sq_ft"]["flower"]
        area_factor = recommended_area / coverage_area_sq_ft if coverage_area_sq_ft > 0 else 1
        
        # Calculate adjusted PPFD
        center_ppfd = fixture["ppfd_center"] * height_factor * area_factor
        edge_ppfd = center_ppfd * 0.6  # Typical edge reduction
        average_ppfd = (center_ppfd + edge_ppfd) / 2
        
        return {
            "fixture_name": fixture_name,
            "hanging_height": hanging_height,
            "coverage_area": coverage_area_sq_ft,
            "ppfd_center": round(center_ppfd),
            "ppfd_edge": round(edge_ppfd),
            "ppfd_average": round(average_ppfd),
            "height_factor": round(height_factor, 2),
            "area_factor": round(area_factor, 2),
            "uniformity": round((edge_ppfd / center_ppfd) * 100, 1)  # % uniformity
        }
    
    def calculate_dli(self, ppfd: float, photoperiod_hours: float) -> Dict:
        """Calculate Daily Light Integral from PPFD and photoperiod"""
        
        # DLI = PPFD × photoperiod × 3600 × (1×10⁻⁶) mol/m²/day
        dli = ppfd * photoperiod_hours * 3.6 / 1000  # Simplified conversion
        
        return {
            "ppfd": ppfd,
            "photoperiod_hours": photoperiod_hours,
            "dli": round(dli, 1),
            "dli_unit": "mol/m²/day"
        }
    
    def recommend_lighting_setup(self, grow_space_sq_ft: float, growth_stage: str,
                                budget: Optional[float] = None) -> Dict:
        """Recommend optimal lighting setup for given space and stage"""
        
        target_ppfd = self.ppfd_requirements[growth_stage]["optimal"]
        target_dli = self.dli_requirements[growth_stage]["optimal"]
        
        # Calculate required photoperiod for target DLI
        required_photoperiod = (target_dli * 1000) / (target_ppfd * 3.6)
        
        recommendations = []
        
        for fixture_name, specs in self.fixture_specs.items():
            # Check if fixture can cover the area
            recommended_coverage = specs["coverage_area_sq_ft"].get("flower", 4)
            fixtures_needed = math.ceil(grow_space_sq_ft / recommended_coverage)
            
            total_wattage = specs["wattage"] * fixtures_needed
            total_cost_estimate = fixtures_needed * 150  # Rough fixture cost estimate
            
            # Skip if over budget
            if budget and total_cost_estimate > budget:
                continue
            
            # Calculate coverage
            ppfd_calc = self.calculate_ppfd_coverage(fixture_name, 18, 
                                                   grow_space_sq_ft / fixtures_needed)
            
            recommendations.append({
                "fixture_name": fixture_name,
                "fixtures_needed": fixtures_needed,
                "total_wattage": total_wattage,
                "estimated_cost": total_cost_estimate,
                "ppfd_average": ppfd_calc["ppfd_average"],
                "meets_ppfd_requirement": ppfd_calc["ppfd_average"] >= target_ppfd * 0.8,
                "efficiency_rating": specs.get("efficiency_umol_j", 2.0),
                "coverage_per_fixture": recommended_coverage
            })
        
        # Sort by efficiency and cost
        recommendations.sort(key=lambda x: (x["meets_ppfd_requirement"], 
                                          x["efficiency_rating"], 
                                          -x["estimated_cost"]), reverse=True)
        
        return {
            "grow_space_sq_ft": grow_space_sq_ft,
            "growth_stage": growth_stage,
            "target_ppfd": target_ppfd,
            "target_dli": target_dli,
            "recommended_photoperiod": round(required_photoperiod, 1),
            "recommendations": recommendations[:3]  # Top 3 options
        }
    
    def calculate_energy_costs(self, fixture_name: str, fixtures_count: int,
                             photoperiod_hours: float, location: str = "us_average") -> Dict:
        """Calculate energy costs for lighting setup"""
        
        if fixture_name not in self.fixture_specs:
            raise ValueError(f"Fixture '{fixture_name}' not found")
        
        if location not in self.energy_costs:
            location = "us_average"
        
        fixture = self.fixture_specs[fixture_name]
        total_wattage = fixture["wattage"] * fixtures_count
        kwh_per_day = (total_wattage * photoperiod_hours) / 1000
        kwh_per_month = kwh_per_day * 30.44  # Average days per month
        
        cost_per_kwh = self.energy_costs[location]
        daily_cost = kwh_per_day * cost_per_kwh
        monthly_cost = kwh_per_month * cost_per_kwh
        annual_cost = monthly_cost * 12
        
        return {
            "fixture_name": fixture_name,
            "fixtures_count": fixtures_count,
            "total_wattage": total_wattage,
            "photoperiod_hours": photoperiod_hours,
            "location": location,
            "cost_per_kwh": cost_per_kwh,
            "kwh_per_day": round(kwh_per_day, 2),
            "kwh_per_month": round(kwh_per_month, 1),
            "daily_cost": round(daily_cost, 2),
            "monthly_cost": round(monthly_cost, 2),
            "annual_cost": round(annual_cost, 2)
        }
    
    def calculate_hanging_height(self, fixture_name: str, target_ppfd: float,
                               coverage_area_sq_ft: float) -> Dict:
        """Calculate optimal hanging height for target PPFD"""
        
        if fixture_name not in self.fixture_specs:
            raise ValueError(f"Fixture '{fixture_name}' not found")
        
        fixture = self.fixture_specs[fixture_name]
        
        # Work backwards from target PPFD
        # target_ppfd = fixture_ppfd * height_factor * area_factor
        recommended_area = fixture["coverage_area_sq_ft"]["flower"]
        area_factor = recommended_area / coverage_area_sq_ft if coverage_area_sq_ft > 0 else 1
        
        required_height_factor = target_ppfd / (fixture["ppfd_center"] * area_factor)
        
        if required_height_factor > 1:
            return {
                "error": "Target PPFD cannot be achieved - fixture not powerful enough",
                "max_achievable_ppfd": round(fixture["ppfd_center"] * area_factor)
            }
        
        # height_factor = (base_height / hanging_height)²
        # hanging_height = base_height / sqrt(height_factor)
        base_height = 18
        optimal_height = base_height / math.sqrt(required_height_factor)
        
        # Practical height limits
        min_height = 8  # Minimum safe distance
        max_height = 36  # Maximum practical height
        
        if optimal_height < min_height:
            optimal_height = min_height
            actual_ppfd = fixture["ppfd_center"] * area_factor * (base_height / min_height) ** 2
            warning = f"Height limited to {min_height}\" minimum - PPFD will be {actual_ppfd:.0f}"
        elif optimal_height > max_height:
            optimal_height = max_height
            actual_ppfd = fixture["ppfd_center"] * area_factor * (base_height / max_height) ** 2
            warning = f"Height limited to {max_height}\" maximum - PPFD will be {actual_ppfd:.0f}"
        else:
            warning = None
        
        return {
            "fixture_name": fixture_name,
            "target_ppfd": target_ppfd,
            "coverage_area": coverage_area_sq_ft,
            "optimal_height": round(optimal_height),
            "practical_range": (max(min_height, optimal_height - 2), 
                              min(max_height, optimal_height + 2)),
            "warning": warning
        }
    
    def compare_fixtures(self, grow_space_sq_ft: float, growth_stage: str) -> Dict:
        """Compare all fixtures for given space and requirements"""
        
        target_ppfd = self.ppfd_requirements[growth_stage]["optimal"]
        comparisons = []
        
        for fixture_name, specs in self.fixture_specs.items():
            # Calculate setup for this fixture
            coverage_calc = self.calculate_ppfd_coverage(fixture_name, 18, grow_space_sq_ft)
            energy_calc = self.calculate_energy_costs(fixture_name, 1, 18)  # 18h photoperiod
            
            # Calculate efficiency metrics
            ppfd_per_watt = coverage_calc["ppfd_average"] / specs["wattage"]
            meets_requirement = coverage_calc["ppfd_average"] >= target_ppfd * 0.8
            
            comparisons.append({
                "fixture_name": fixture_name,
                "wattage": specs["wattage"],
                "ppfd_average": coverage_calc["ppfd_average"],
                "ppfd_per_watt": round(ppfd_per_watt, 2),
                "efficiency_umol_j": specs.get("efficiency_umol_j", 0),
                "monthly_energy_cost": energy_calc["monthly_cost"],
                "meets_requirement": meets_requirement,
                "coverage_rating": "good" if meets_requirement else "insufficient"
            })
        
        # Sort by efficiency
        comparisons.sort(key=lambda x: x["efficiency_umol_j"], reverse=True)
        
        return {
            "grow_space_sq_ft": grow_space_sq_ft,
            "growth_stage": growth_stage,
            "target_ppfd": target_ppfd,
            "fixture_comparisons": comparisons
        }
