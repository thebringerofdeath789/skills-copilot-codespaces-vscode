"""
GrowMaster Pro - Core Data Models
Base classes and data structures for the application
"""

from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid
import json

class GrowingMethod(Enum):
    """Growing method enumeration"""
    SOIL_INDOOR = "soil_indoor"
    SOIL_OUTDOOR = "soil_outdoor" 
    HYDRO_DWC = "hydro_dwc"
    HYDRO_NFT = "hydro_nft"
    HYDRO_EBB_FLOW = "hydro_ebb_flow"
    HYDRO_AERO = "hydro_aero"
    GREENHOUSE = "greenhouse"
    MIXED_LIGHT = "mixed_light"

class GrowthStage(Enum):
    """Plant growth stage enumeration"""
    GERMINATION = "germination"
    SEEDLING = "seedling"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    HARVEST = "harvest"
    CURING = "curing"

class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high" 
    MEDIUM = "medium"
    LOW = "low"

class TaskStatus(Enum):
    """Task completion status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class BaseModel:
    """Base model class with common functionality"""
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def update_timestamp(self):
        """Update the last modified timestamp"""
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary representation"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, date):
                result[key] = value.isoformat()
            elif isinstance(value, Enum):
                result[key] = value.value
            elif hasattr(value, 'to_dict'):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in value]
            else:
                result[key] = value
        return result
    
    def from_dict(self, data: Dict[str, Any]):
        """Load model from dictionary representation"""
        for key, value in data.items():
            if key in ['created_at', 'updated_at'] and isinstance(value, str):
                setattr(self, key, datetime.fromisoformat(value))
            elif key.endswith('_date') and isinstance(value, str):
                setattr(self, key, date.fromisoformat(value))
            else:
                setattr(self, key, value)
    
    def save_to_json(self, filepath: str):
        """Save model to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
    
    @classmethod
    def load_from_json(cls, filepath: str):
        """Load model from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        instance = cls()
        instance.from_dict(data)
        return instance
