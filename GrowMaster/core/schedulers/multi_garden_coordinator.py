"""
GrowMaster Pro - Multi-Garden Task Coordinator
Cross-garden task optimization, resource sharing, and batch processing
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import heapq
from collections import defaultdict

logger = logging.getLogger(__name__)

class ResourceType(Enum):
    """Types of resources that can be shared"""
    NUTRIENTS = "nutrients"
    WATER = "water" 
    EQUIPMENT = "equipment"
    LIGHTING = "lighting"
    TIME = "time"
    SPACE = "space"

class TaskConflictType(Enum):
    """Types of task conflicts"""
    RESOURCE_CONFLICT = "resource_conflict"
    TIMING_CONFLICT = "timing_conflict"
    DEPENDENCY_CONFLICT = "dependency_conflict"
    SPACE_CONFLICT = "space_conflict"

@dataclass
class ResourceRequirement:
    """Resource requirements for a task"""
    resource_type: ResourceType
    quantity: float
    duration_minutes: int
    flexibility_minutes: int = 60  # How flexible timing is

@dataclass
class TaskBatch:
    """Group of tasks that can be executed together"""
    tasks: List[Dict[str, Any]]
    total_duration: int
    shared_resources: List[ResourceType]
    optimal_start_time: datetime
    efficiency_score: float

class MultiGardenTaskCoordinator:
    """Coordinates tasks across multiple gardens for optimal efficiency"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.resource_inventory = self._load_resource_inventory()
        
    def _load_resource_inventory(self) -> Dict[ResourceType, Dict[str, Any]]:
        """Load available resources from database"""
        return {
            ResourceType.NUTRIENTS: {
                'available': True,
                'capacity': 100,  # liters
                'current_usage': 0
            },
            ResourceType.WATER: {
                'available': True,
                'capacity': 500,  # liters
                'current_usage': 0
            },
            ResourceType.EQUIPMENT: {
                'available': True,
                'items': ['pH meter', 'EC meter', 'pruning shears', 'measuring cups']
            },
            ResourceType.TIME: {
                'available': True,
                'daily_capacity': 480,  # 8 hours in minutes
                'current_usage': 0
            }
        }
    
    def coordinate_daily_tasks(self, target_date: datetime = None) -> Dict[str, Any]:
        """Coordinate all tasks for a given date across all gardens"""
        if target_date is None:
            target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        try:
            # Get all pending tasks for the date
            pending_tasks = self._get_pending_tasks_for_date(target_date)
            if not pending_tasks:
                return {'batches': [], 'conflicts': [], 'total_tasks': 0}
            
            # Analyze resource requirements
            task_resources = self._analyze_resource_requirements(pending_tasks)
            
            # Detect and resolve conflicts
            conflicts = self._detect_conflicts(pending_tasks, task_resources)
            resolved_tasks = self._resolve_conflicts(pending_tasks, conflicts)
            
            # Create optimal task batches
            task_batches = self._create_task_batches(resolved_tasks, task_resources)
            
            # Optimize execution order
            optimized_batches = self._optimize_execution_order(task_batches)
            
            # Calculate resource sharing opportunities
            sharing_opportunities = self._identify_sharing_opportunities(optimized_batches)
            
            coordination_result = {
                'date': target_date.isoformat(),
                'total_tasks': len(pending_tasks),
                'batches': optimized_batches,
                'conflicts_detected': len(conflicts),
                'conflicts_resolved': conflicts,
                'sharing_opportunities': sharing_opportunities,
                'estimated_time_saved': self._calculate_time_savings(optimized_batches),
                'resource_efficiency': self._calculate_resource_efficiency(optimized_batches)
            }
            
            logger.info(f"Coordinated {len(pending_tasks)} tasks into {len(optimized_batches)} optimized batches")
            return coordination_result
            
        except Exception as e:
            logger.error(f"Error coordinating daily tasks: {e}")
            return {'error': str(e)}
    
    def _get_pending_tasks_for_date(self, target_date: datetime) -> List[Dict[str, Any]]:
        """Get all pending tasks for a specific date"""
        try:
            start_date = target_date.strftime('%Y-%m-%d')
            end_date = (target_date + timedelta(days=1)).strftime('%Y-%m-%d')
            
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT t.id, t.title, t.description, t.garden_id, t.task_type, 
                           t.priority, t.due_date, t.estimated_duration,
                           g.name as garden_name, g.growing_method, g.location
                    FROM tasks t
                    JOIN gardens g ON t.garden_id = g.id
                    WHERE t.is_completed = 0 
                    AND t.due_date >= ? 
                    AND t.due_date < ?
                    AND g.is_active = 1
                    ORDER BY t.priority DESC, t.due_date ASC
                """, (start_date, end_date))
                
                tasks = []
                for row in cursor.fetchall():
                    tasks.append({
                        'id': row[0],
                        'title': row[1],
                        'description': row[2],
                        'garden_id': row[3],
                        'task_type': row[4],
                        'priority': row[5],
                        'due_date': row[6],
                        'estimated_duration': row[7],
                        'garden_name': row[8],
                        'growing_method': row[9],
                        'location': row[10]
                    })
                
                return tasks
                
        except Exception as e:
            logger.error(f"Error getting pending tasks: {e}")
            return []
    
    def _analyze_resource_requirements(self, tasks: List[Dict[str, Any]]) -> Dict[int, List[ResourceRequirement]]:
        """Analyze resource requirements for each task"""
        task_resources = {}
        
        for task in tasks:
            task_id = task['id']
            task_type = task['task_type']
            duration = task['estimated_duration']
            
            resources = []
            
            # Determine resource requirements based on task type
            if task_type == 'feeding':
                resources.extend([
                    ResourceRequirement(ResourceType.NUTRIENTS, 2.0, duration),
                    ResourceRequirement(ResourceType.WATER, 10.0, duration),
                    ResourceRequirement(ResourceType.EQUIPMENT, 1.0, duration),
                    ResourceRequirement(ResourceType.TIME, duration, duration, flexibility_minutes=30)
                ])
            elif task_type == 'watering':
                resources.extend([
                    ResourceRequirement(ResourceType.WATER, 5.0, duration),
                    ResourceRequirement(ResourceType.TIME, duration, duration, flexibility_minutes=60)
                ])
            elif task_type == 'pruning':
                resources.extend([
                    ResourceRequirement(ResourceType.EQUIPMENT, 1.0, duration),
                    ResourceRequirement(ResourceType.TIME, duration, duration, flexibility_minutes=120)
                ])
            elif task_type == 'monitoring':
                resources.extend([
                    ResourceRequirement(ResourceType.EQUIPMENT, 1.0, duration),
                    ResourceRequirement(ResourceType.TIME, duration, duration, flexibility_minutes=180)
                ])
            else:
                # Default resource requirements
                resources.append(
                    ResourceRequirement(ResourceType.TIME, duration, duration, flexibility_minutes=60)
                )
            
            task_resources[task_id] = resources
        
        return task_resources
    
    def _detect_conflicts(self, tasks: List[Dict[str, Any]], 
                         task_resources: Dict[int, List[ResourceRequirement]]) -> List[Dict[str, Any]]:
        """Detect conflicts between tasks"""
        conflicts = []
        
        # Check for resource conflicts
        resource_usage = defaultdict(list)
        
        for task in tasks:
            task_id = task['id']
            due_time = datetime.fromisoformat(task['due_date'])
            
            for resource_req in task_resources.get(task_id, []):
                resource_usage[resource_req.resource_type].append({
                    'task_id': task_id,
                    'task_title': task['title'],
                    'start_time': due_time,
                    'end_time': due_time + timedelta(minutes=resource_req.duration_minutes),
                    'quantity': resource_req.quantity,
                    'flexibility': resource_req.flexibility_minutes
                })
        
        # Check for overlapping resource usage
        for resource_type, usages in resource_usage.items():
            # Sort by start time
            usages.sort(key=lambda x: x['start_time'])
            
            for i in range(len(usages) - 1):
                current = usages[i]
                next_usage = usages[i + 1]
                
                # Check if there's an overlap
                if current['end_time'] > next_usage['start_time']:
                    conflicts.append({
                        'type': TaskConflictType.RESOURCE_CONFLICT.value,
                        'resource': resource_type.value,
                        'tasks': [current['task_id'], next_usage['task_id']],
                        'task_titles': [current['task_title'], next_usage['task_title']],
                        'overlap_minutes': (current['end_time'] - next_usage['start_time']).total_seconds() / 60,
                        'flexibility': min(current['flexibility'], next_usage['flexibility'])
                    })
        
        # Check for garden location conflicts (if tasks require physical presence)
        location_conflicts = self._check_location_conflicts(tasks)
        conflicts.extend(location_conflicts)
        
        return conflicts
    
    def _check_location_conflicts(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for conflicts when tasks require physical presence at different locations"""
        conflicts = []
        physical_tasks = []
        
        # Identify tasks that require physical presence
        for task in tasks:
            if task['task_type'] in ['pruning', 'training', 'harvesting', 'maintenance']:
                physical_tasks.append(task)
        
        # Check for location conflicts
        physical_tasks.sort(key=lambda x: datetime.fromisoformat(x['due_date']))
        
        for i in range(len(physical_tasks) - 1):
            current = physical_tasks[i]
            next_task = physical_tasks[i + 1]
            
            # If different locations and overlapping times
            if (current['location'] != next_task['location'] and
                current['location'] is not None and next_task['location'] is not None):
                
                current_end = (datetime.fromisoformat(current['due_date']) + 
                              timedelta(minutes=current['estimated_duration']))
                next_start = datetime.fromisoformat(next_task['due_date'])
                
                # Add travel time buffer (15 minutes between locations)
                if (next_start - current_end).total_seconds() < 900:  # 15 minutes
                    conflicts.append({
                        'type': TaskConflictType.SPACE_CONFLICT.value,
                        'tasks': [current['id'], next_task['id']],
                        'task_titles': [current['title'], next_task['title']],
                        'locations': [current['location'], next_task['location']],
                        'travel_time_needed': 15
                    })
        
        return conflicts
    
    def _resolve_conflicts(self, tasks: List[Dict[str, Any]], 
                          conflicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Resolve conflicts by rescheduling tasks"""
        resolved_tasks = tasks.copy()
        
        for conflict in conflicts:
            if conflict['type'] == TaskConflictType.RESOURCE_CONFLICT.value:
                self._resolve_resource_conflict(resolved_tasks, conflict)
            elif conflict['type'] == TaskConflictType.SPACE_CONFLICT.value:
                self._resolve_space_conflict(resolved_tasks, conflict)
        
        return resolved_tasks
    
    def _resolve_resource_conflict(self, tasks: List[Dict[str, Any]], conflict: Dict[str, Any]):
        """Resolve resource conflicts by rescheduling"""
        task_ids = conflict['tasks']
        flexibility = conflict['flexibility']
        
        # Find the tasks involved
        involved_tasks = [task for task in tasks if task['id'] in task_ids]
        
        if len(involved_tasks) != 2:
            return
        
        # Reschedule the lower priority task
        task1, task2 = involved_tasks
        priority_order = {'Critical': 3, 'High': 2, 'Medium': 1, 'Low': 0}
        
        if priority_order.get(task1['priority'], 0) >= priority_order.get(task2['priority'], 0):
            task_to_reschedule = task2
        else:
            task_to_reschedule = task1
        
        # Reschedule by adding flexibility minutes
        current_due = datetime.fromisoformat(task_to_reschedule['due_date'])
        new_due = current_due + timedelta(minutes=flexibility)
        task_to_reschedule['due_date'] = new_due.isoformat()
        
        logger.info("Rescheduled task %s by %s minutes", task_to_reschedule['title'], flexibility)
    
    def _resolve_space_conflict(self, tasks: List[Dict[str, Any]], conflict: Dict[str, Any]):
        """Resolve space/location conflicts"""
        task_ids = conflict['tasks']
        travel_time = conflict['travel_time_needed']
        
        involved_tasks = [task for task in tasks if task['id'] in task_ids]
        if len(involved_tasks) == 2:
            # Add travel time to the second task
            second_task = involved_tasks[1]
            current_due = datetime.fromisoformat(second_task['due_date'])
            new_due = current_due + timedelta(minutes=travel_time)
            second_task['due_date'] = new_due.isoformat()
    
    def _create_task_batches(self, tasks: List[Dict[str, Any]], task_resources: Dict[int, List[ResourceRequirement]]) -> List[TaskBatch]:
        """Create optimal batches of tasks that can be executed together"""
        batches = []
        remaining_tasks = tasks.copy()
        
        while remaining_tasks:
            # Find the best batch starting with the highest priority task
            remaining_tasks.sort(key=lambda x: (
                {'Critical': 3, 'High': 2, 'Medium': 1, 'Low': 0}.get(x['priority'], 0),
                datetime.fromisoformat(x['due_date'])
            ), reverse=True)
            
            seed_task = remaining_tasks[0]
            batch_tasks = [seed_task]
            remaining_tasks.remove(seed_task)
            
            # Find compatible tasks to add to the batch
            compatible_tasks = []
            for task in remaining_tasks[:]:
                if self._are_tasks_batchable(seed_task, task, task_resources):
                    compatible_tasks.append(task)
            
            # Add most compatible tasks to batch (up to reasonable limit)
            compatibility_scores = []
            for task in compatible_tasks:
                score = self._calculate_compatibility_score(seed_task, task, task_resources)
                compatibility_scores.append((score, task))
            
            compatibility_scores.sort(reverse=True)
            
            # Add top compatible tasks to batch (max 5 tasks per batch)
            for score, task in compatibility_scores[:4]:  # 4 + seed = 5 max
                batch_tasks.append(task)
                remaining_tasks.remove(task)
            
            # Create batch object
            batch = self._create_batch_object(batch_tasks, task_resources)
            batches.append(batch)
        
        return batches
    
    def _are_tasks_batchable(self, task1: Dict[str, Any], task2: Dict[str, Any],
                           task_resources: Dict[int, List[ResourceRequirement]]) -> bool:
        """Check if two tasks can be batched together"""
        
        # Check if tasks are for the same garden or nearby locations
        if task1['location'] != task2['location'] and task1['location'] is not None:
            return False
        
        # Check if tasks share resources efficiently
        task1_resources = {req.resource_type for req in task_resources.get(task1['id'], [])}
        task2_resources = {req.resource_type for req in task_resources.get(task2['id'], [])}
        
        # Tasks should share at least one resource type for efficiency
        if not task1_resources & task2_resources:
            return False
        
        # Check time compatibility
        time1 = datetime.fromisoformat(task1['due_date'])
        time2 = datetime.fromisoformat(task2['due_date'])
        time_diff = abs((time2 - time1).total_seconds() / 60)
        
        # Tasks should be within 2 hours of each other
        if time_diff > 120:
            return False
        
        return True
    
    def _calculate_compatibility_score(self, task1: Dict[str, Any], task2: Dict[str, Any],
                                     task_resources: Dict[int, List[ResourceRequirement]]) -> float:
        """Calculate compatibility score between two tasks"""
        score = 0.0
        
        # Same garden bonus
        if task1['garden_id'] == task2['garden_id']:
            score += 10.0
        
        # Same location bonus
        if task1['location'] == task2['location']:
            score += 5.0
        
        # Shared resources bonus
        task1_resources = {req.resource_type for req in task_resources.get(task1['id'], [])}
        task2_resources = {req.resource_type for req in task_resources.get(task2['id'], [])}
        shared_resources = task1_resources & task2_resources
        score += len(shared_resources) * 2.0
        
        # Time proximity bonus
        time1 = datetime.fromisoformat(task1['due_date'])
        time2 = datetime.fromisoformat(task2['due_date'])
        time_diff = abs((time2 - time1).total_seconds() / 60)
        score += max(0, 60 - time_diff) * 0.1  # Closer times get higher scores
        
        # Task type compatibility
        compatible_types = {
            ('feeding', 'monitoring'): 3.0,
            ('pruning', 'training'): 4.0,
            ('watering', 'monitoring'): 2.0
        }
        
        type_pair = (task1['task_type'], task2['task_type'])
        if type_pair in compatible_types:
            score += compatible_types[type_pair]
        elif (type_pair[1], type_pair[0]) in compatible_types:
            score += compatible_types[(type_pair[1], type_pair[0])]
        
        return score
    
    def _create_batch_object(self, tasks: List[Dict[str, Any]], 
                           task_resources: Dict[int, List[ResourceRequirement]]) -> TaskBatch:
        """Create a TaskBatch object from a list of tasks"""
        
        total_duration = sum(task['estimated_duration'] for task in tasks)
        
        # Find shared resources
        all_resource_types = set()
        for task in tasks:
            for req in task_resources.get(task['id'], []):
                all_resource_types.add(req.resource_type)
        
        shared_resources = list(all_resource_types)
        
        # Calculate optimal start time (earliest due date)
        earliest_due = min(datetime.fromisoformat(task['due_date']) for task in tasks)
        
        # Calculate efficiency score
        efficiency_score = self._calculate_batch_efficiency(tasks, shared_resources, total_duration)
        
        return TaskBatch(
            tasks=tasks,
            total_duration=total_duration,
            shared_resources=shared_resources,
            optimal_start_time=earliest_due,
            efficiency_score=efficiency_score
        )
    
    def _calculate_batch_efficiency(self, tasks: List[Dict[str, Any]], 
                                  shared_resources: List[ResourceType], 
                                  total_duration: int) -> float:
        """Calculate efficiency score for a task batch"""
        
        # Base score
        efficiency = 50.0
        
        # Bonus for multiple tasks
        efficiency += len(tasks) * 10.0
        
        # Bonus for shared resources (reduces setup/cleanup time)
        efficiency += len(shared_resources) * 5.0
        
        # Bonus for same garden tasks
        gardens = {task['garden_id'] for task in tasks}
        if len(gardens) == 1:
            efficiency += 15.0
        
        # Penalty for very long batches
        if total_duration > 120:  # Over 2 hours
            efficiency -= (total_duration - 120) * 0.1
        
        return max(0.0, min(100.0, efficiency))
    
    def _optimize_execution_order(self, batches: List[TaskBatch]) -> List[Dict[str, Any]]:
        """Optimize the execution order of task batches"""
        
        # Sort batches by efficiency and urgency
        batch_priorities = []
        
        for i, batch in enumerate(batches):
            urgency_score = 0
            for task in batch.tasks:
                priority_scores = {'Critical': 100, 'High': 75, 'Medium': 50, 'Low': 25}
                urgency_score += priority_scores.get(task['priority'], 25)
            
            urgency_score /= len(batch.tasks)  # Average urgency
            
            combined_score = batch.efficiency_score * 0.6 + urgency_score * 0.4
            batch_priorities.append((combined_score, i, batch))
        
        # Sort by combined score
        batch_priorities.sort(reverse=True)
        
        # Create optimized batch list
        optimized_batches = []
        current_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)  # Start at 8 AM
        
        for score, original_index, batch in batch_priorities:
            batch_info = {
                'id': original_index,
                'tasks': batch.tasks,
                'total_duration_minutes': batch.total_duration,
                'shared_resources': [r.value for r in batch.shared_resources],
                'optimal_start_time': current_time.isoformat(),
                'estimated_end_time': (current_time + timedelta(minutes=batch.total_duration)).isoformat(),
                'efficiency_score': batch.efficiency_score,
                'task_count': len(batch.tasks),
                'gardens_involved': list({task['garden_id'] for task in batch.tasks})
            }
            
            optimized_batches.append(batch_info)
            
            # Add buffer time between batches
            current_time += timedelta(minutes=batch.total_duration + 15)
        
        return optimized_batches
    
    def _identify_sharing_opportunities(self, batches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify opportunities for resource sharing between batches"""
        sharing_opportunities = []
        
        for i, batch1 in enumerate(batches):
            for j, batch2 in enumerate(batches[i+1:], i+1):
                
                # Check for resource overlap
                resources1 = set(batch1['shared_resources'])
                resources2 = set(batch2['shared_resources'])
                shared = resources1 & resources2
                
                if shared:
                    # Calculate potential savings
                    time_gap = (datetime.fromisoformat(batch2['optimal_start_time']) - 
                               datetime.fromisoformat(batch1['estimated_end_time'])).total_seconds() / 60
                    
                    if 0 < time_gap < 60:  # Within 1 hour - good for sharing
                        opportunity = {
                            'batch_1': i,
                            'batch_2': j,
                            'shared_resources': list(shared),
                            'potential_time_savings': min(5 * len(shared), 30),  # Up to 30 minutes
                            'setup_reduction': True
                        }
                        sharing_opportunities.append(opportunity)
        
        return sharing_opportunities
    
    def _calculate_time_savings(self, batches: List[Dict[str, Any]]) -> int:
        """Calculate estimated time savings from task coordination"""
        
        total_individual_time = sum(batch['total_duration_minutes'] for batch in batches)
        
        # Add individual setup/cleanup time that would be needed
        setup_time_per_task = 5  # 5 minutes setup per task
        total_tasks = sum(batch['task_count'] for batch in batches)
        individual_setup_time = total_tasks * setup_time_per_task
        
        # Coordinated setup time (shared resources reduce setup)
        coordinated_setup_time = len(batches) * 10  # 10 minutes per batch
        
        time_savings = individual_setup_time - coordinated_setup_time
        return max(0, time_savings)
    
    def _calculate_resource_efficiency(self, batches: List[Dict[str, Any]]) -> float:
        """Calculate overall resource efficiency percentage"""
        
        if not batches:
            return 0.0
        
        total_efficiency = sum(batch['efficiency_score'] for batch in batches)
        average_efficiency = total_efficiency / len(batches)
        
        return round(average_efficiency, 1)
    
    def get_resource_utilization(self, target_date: datetime = None) -> Dict[str, Any]:
        """Get current resource utilization across all gardens"""
        if target_date is None:
            target_date = datetime.now()
        
        try:
            coordination_result = self.coordinate_daily_tasks(target_date)
            
            resource_usage = defaultdict(float)
            resource_capacity = {
                ResourceType.TIME.value: 480,  # 8 hours
                ResourceType.NUTRIENTS.value: 100,
                ResourceType.WATER.value: 500,
                ResourceType.EQUIPMENT.value: 10
            }
            
            for batch in coordination_result.get('batches', []):
                for resource in batch['shared_resources']:
                    if resource == 'time':
                        resource_usage[resource] += batch['total_duration_minutes']
                    else:
                        resource_usage[resource] += batch['task_count']  # Simplified
            
            utilization = {}
            for resource, capacity in resource_capacity.items():
                usage = resource_usage.get(resource, 0)
                utilization[resource] = {
                    'usage': usage,
                    'capacity': capacity,
                    'percentage': round((usage / capacity) * 100, 1) if capacity > 0 else 0,
                    'available': capacity - usage
                }
            
            return {
                'date': target_date.isoformat(),
                'resource_utilization': utilization,
                'over_capacity': [r for r, data in utilization.items() if data['percentage'] > 100],
                'recommendations': self._get_utilization_recommendations(utilization)
            }
            
        except Exception as e:
            logger.error(f"Error calculating resource utilization: {e}")
            return {'error': str(e)}
