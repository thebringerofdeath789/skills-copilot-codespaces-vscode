"""
Task Model - Individual task management and scheduling
"""

from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from . import BaseModel, TaskPriority, TaskStatus

class Task(BaseModel):
    """Individual task model with comprehensive tracking"""
    
    def __init__(self, title: str, description: str = "", 
                 garden_id: str = "", grow_plan_id: str = ""):
        super().__init__()
        self.title = title
        self.description = description
        self.garden_id = garden_id
        self.grow_plan_id = grow_plan_id
        
        # Scheduling
        self.scheduled_date = date.today()
        self.due_date = date.today()
        self.completed_date = None
        self.estimated_duration = 30  # minutes
        
        # Status and priority
        self.status = TaskStatus.PENDING
        self.priority = TaskPriority.MEDIUM
        self.progress_percent = 0
        
        # Task categorization
        self.category = "general"  # watering, feeding, training, monitoring, etc.
        self.tags = []
        
        # Dependencies
        self.depends_on = []  # List of task IDs that must complete first
        self.blocks = []      # List of task IDs that depend on this task
        
        # Recurring task settings
        self.is_recurring = False
        self.recurrence_pattern = {
            "type": "none",  # daily, weekly, monthly, custom
            "interval": 1,   # every N days/weeks/months
            "end_date": None,
            "max_occurrences": None
        }
        
        # Resources and costs
        self.required_resources = []  # List of inventory items needed
        self.estimated_cost = 0.0
        self.actual_cost = 0.0
        
        # Weather dependency (for outdoor tasks)
        self.weather_dependent = False
        self.weather_requirements = {
            "min_temp": None,
            "max_temp": None,
            "max_humidity": None,
            "no_precipitation": False,
            "min_wind_speed": None,
            "max_wind_speed": None
        }
        
        # Documentation
        self.notes = ""
        self.photo_paths = []
        self.attachments = []
        
        # Completion tracking
        self.completion_notes = ""
        self.completion_photos = []
        self.actual_duration = None
        
        # Notification settings
        self.reminder_settings = {
            "enabled": True,
            "advance_days": 0,
            "advance_hours": 2,
            "repeat_notifications": False
        }
    
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        return (self.status != TaskStatus.COMPLETED and 
                self.due_date < date.today())
    
    def days_until_due(self) -> int:
        """Calculate days until task is due"""
        return (self.due_date - date.today()).days
    
    def can_start(self, completed_task_ids: List[str]) -> bool:
        """Check if all dependencies are satisfied"""
        return all(dep_id in completed_task_ids for dep_id in self.depends_on)
    
    def mark_completed(self, notes: str = "", actual_duration: Optional[int] = None):
        """Mark task as completed with optional completion details"""
        self.status = TaskStatus.COMPLETED
        self.completed_date = date.today()
        self.progress_percent = 100
        self.completion_notes = notes
        if actual_duration:
            self.actual_duration = actual_duration
        self.update_timestamp()
    
    def mark_in_progress(self, progress_percent: int = 0):
        """Mark task as in progress"""
        self.status = TaskStatus.IN_PROGRESS
        self.progress_percent = max(0, min(100, progress_percent))
        self.update_timestamp()
    
    def cancel_task(self, reason: str = ""):
        """Cancel the task"""
        self.status = TaskStatus.CANCELLED
        self.completion_notes = f"Cancelled: {reason}"
        self.update_timestamp()
    
    def reschedule(self, new_date: date, reason: str = ""):
        """Reschedule task to a new date"""
        old_date = self.scheduled_date
        self.scheduled_date = new_date
        self.due_date = new_date
        if reason:
            self.notes += f"\\nRescheduled from {old_date} to {new_date}: {reason}"
        self.update_timestamp()
    
    def add_dependency(self, task_id: str):
        """Add a task dependency"""
        if task_id not in self.depends_on:
            self.depends_on.append(task_id)
            self.update_timestamp()
    
    def remove_dependency(self, task_id: str):
        """Remove a task dependency"""
        if task_id in self.depends_on:
            self.depends_on.remove(task_id)
            self.update_timestamp()
    
    def add_required_resource(self, resource_id: str, quantity: float = 1.0):
        """Add a required resource for this task"""
        resource = {"resource_id": resource_id, "quantity": quantity}
        if resource not in self.required_resources:
            self.required_resources.append(resource)
            self.update_timestamp()
    
    def estimate_cost(self, resource_costs: Dict[str, float]) -> float:
        """Calculate estimated cost based on required resources"""
        total_cost = 0.0
        for resource in self.required_resources:
            resource_id = resource["resource_id"]
            quantity = resource["quantity"]
            unit_cost = resource_costs.get(resource_id, 0.0)
            total_cost += quantity * unit_cost
        
        self.estimated_cost = total_cost
        return total_cost
    
    def create_next_occurrence(self) -> Optional['Task']:
        """Create the next occurrence of a recurring task"""
        if not self.is_recurring or self.recurrence_pattern["type"] == "none":
            return None
        
        # Calculate next occurrence date
        pattern = self.recurrence_pattern
        interval = pattern["interval"]
        
        if pattern["type"] == "daily":
            next_date = self.scheduled_date + timedelta(days=interval)
        elif pattern["type"] == "weekly":
            next_date = self.scheduled_date + timedelta(weeks=interval)
        elif pattern["type"] == "monthly":
            # Approximate monthly recurrence
            next_date = self.scheduled_date + timedelta(days=30 * interval)
        else:
            return None
        
        # Check if we've reached the end date or max occurrences
        if pattern["end_date"] and next_date > pattern["end_date"]:
            return None
        
        # Create new task instance
        next_task = Task(self.title, self.description, self.garden_id, self.grow_plan_id)
        next_task.scheduled_date = next_date
        next_task.due_date = next_date
        next_task.category = self.category
        next_task.priority = self.priority
        next_task.estimated_duration = self.estimated_duration
        next_task.tags = self.tags.copy()
        next_task.required_resources = self.required_resources.copy()
        next_task.weather_dependent = self.weather_dependent
        next_task.weather_requirements = self.weather_requirements.copy()
        next_task.is_recurring = True
        next_task.recurrence_pattern = self.recurrence_pattern.copy()
        
        return next_task
    
    def get_color_by_priority(self) -> str:
        """Get color code based on task priority"""
        color_map = {
            TaskPriority.CRITICAL: "#d32f2f",
            TaskPriority.HIGH: "#f57c00",
            TaskPriority.MEDIUM: "#1976d2",
            TaskPriority.LOW: "#388e3c"
        }
        return color_map.get(self.priority, "#1976d2")
    
    def get_color_by_status(self) -> str:
        """Get color code based on task status"""
        color_map = {
            TaskStatus.PENDING: "#757575",
            TaskStatus.IN_PROGRESS: "#1976d2",
            TaskStatus.COMPLETED: "#4caf50",
            TaskStatus.OVERDUE: "#d32f2f",
            TaskStatus.CANCELLED: "#9e9e9e"
        }
        return color_map.get(self.status, "#757575")
