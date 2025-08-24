"""
Garden Model - Individual garden/grow space management
"""

from datetime import date, datetime
from typing import Optional, List, Dict, Any
from . import BaseModel, GrowingMethod

class Garden(BaseModel):
    """Individual garden/grow space model"""
    
    def __init__(self, name: str, growing_method: GrowingMethod, 
                 location: str = "", description: str = ""):
        super().__init__()
        self.name = name
        self.growing_method = growing_method
        self.location = location
        self.description = description
        self.is_active = True
        
        # Physical specifications
        self.dimensions = {
            "length": 0.0,  # feet or meters
            "width": 0.0,
            "height": 0.0
        }
        
        # Environmental settings
        self.environment = {
            "target_temp_day": 75.0,
            "target_temp_night": 65.0,
            "target_humidity": 60.0,
            "co2_ppm": 400,
            "air_circulation": True
        }
        
        # Lighting configuration
        self.lighting = {
            "type": "LED",  # LED, HPS, MH, CFL, Natural
            "wattage": 0,
            "ppfd": 0,  # Photosynthetic Photon Flux Density
            "daily_light_integral": 0,
            "photoperiod": {"hours_on": 18, "hours_off": 6}
        }
        
        # Growing medium and container info
        self.growing_medium = {
            "type": "soil",  # soil, coco, hydro, rockwool
            "brand": "",
            "container_size": 0,  # gallons or liters
            "container_count": 0,
            "ph_range": {"min": 6.0, "max": 7.0}
        }
        
        # Cost tracking
        self.setup_costs = {
            "equipment": 0.0,
            "infrastructure": 0.0, 
            "initial_supplies": 0.0
        }
        
        # Performance metrics
        self.metrics = {
            "total_harvests": 0,
            "total_yield": 0.0,
            "average_cycle_days": 0,
            "success_rate": 0.0,
            "cost_per_gram": 0.0
        }
        
        # Associated grow plans
        self.grow_plan_ids = []
        
        # Creation and modification tracking
        self.created_date = date.today()
        self.last_harvest_date = None
        self.next_cycle_date = None
    
    def calculate_growing_area(self) -> float:
        """Calculate total growing area in square feet/meters"""
        return self.dimensions["length"] * self.dimensions["width"]
    
    def calculate_volume(self) -> float:
        """Calculate total growing volume in cubic feet/meters"""
        return (self.dimensions["length"] * 
                self.dimensions["width"] * 
                self.dimensions["height"])
    
    def calculate_light_density(self) -> float:
        """Calculate watts per square foot/meter"""
        area = self.calculate_growing_area()
        if area > 0:
            return self.lighting["wattage"] / area
        return 0.0
    
    def update_performance_metrics(self, harvest_data: Dict):
        """Update garden performance metrics after harvest"""
        self.update_timestamp()
        
        if harvest_data:
            self.metrics["total_harvests"] += 1
            self.metrics["total_yield"] += harvest_data.get("yield", 0.0)
            
            cycle_days = harvest_data.get("cycle_days", 0)
            if cycle_days > 0:
                current_avg = self.metrics["average_cycle_days"]
                total_harvests = self.metrics["total_harvests"]
                self.metrics["average_cycle_days"] = (
                    (current_avg * (total_harvests - 1) + cycle_days) / total_harvests
                )
            
            # Update last harvest date
            self.last_harvest_date = date.today()
    
    def get_recommended_plant_count(self) -> int:
        """Calculate recommended plant count based on garden size and method"""
        area = self.calculate_growing_area()
        
        # Plants per square foot/meter based on growing method
        density_map = {
            GrowingMethod.SOIL_INDOOR: 0.25,    # 4 sq ft per plant
            GrowingMethod.SOIL_OUTDOOR: 0.11,   # 9 sq ft per plant
            GrowingMethod.HYDRO_DWC: 0.5,       # 2 sq ft per plant
            GrowingMethod.HYDRO_NFT: 1.0,       # 1 sq ft per plant
            GrowingMethod.HYDRO_EBB_FLOW: 0.33, # 3 sq ft per plant
            GrowingMethod.HYDRO_AERO: 0.5,      # 2 sq ft per plant
            GrowingMethod.GREENHOUSE: 0.2,      # 5 sq ft per plant
            GrowingMethod.MIXED_LIGHT: 0.25     # 4 sq ft per plant
        }
        
        density = density_map.get(self.growing_method, 0.25)
        return max(1, int(area * density))
    
    def estimate_power_consumption(self) -> Dict[str, float]:
        """Estimate monthly power consumption"""
        daily_hours = self.lighting["photoperiod"]["hours_on"]
        daily_kwh = (self.lighting["wattage"] / 1000) * daily_hours
        monthly_kwh = daily_kwh * 30
        
        # Add additional equipment (fans, pumps, etc.)
        additional_power = monthly_kwh * 0.3  # 30% additional
        
        return {
            "lighting_kwh": monthly_kwh,
            "additional_kwh": additional_power,
            "total_monthly_kwh": monthly_kwh + additional_power
        }
    
    def clone(self, new_name: str) -> 'Garden':
        """Create a copy of this garden with a new name"""
        new_garden = Garden(new_name, self.growing_method, self.location, self.description)
        new_garden.dimensions = self.dimensions.copy()
        new_garden.environment = self.environment.copy()
        new_garden.lighting = self.lighting.copy()
        new_garden.growing_medium = self.growing_medium.copy()
        new_garden.setup_costs = self.setup_costs.copy()
        return new_garden
