"""
GrowMaster Pro Database Management System
SQLite database initialization, schema creation, and data management
Handles all application data persistence and backup operations
"""

import sqlite3
import json
import logging
import os
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import shutil

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Complete database management system for GrowMaster Pro"""
    
    def __init__(self, db_path: str = None):
        """Initialize database manager with optional custom path"""
        if db_path is None:
            # Use application data directory
            app_dir = Path.home() / "Documents" / "GrowMaster Pro"
            app_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = str(app_dir / "growmaster.db")
        else:
            self.db_path = db_path
        
        self.backup_dir = Path(self.db_path).parent / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        self.initialize_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper settings"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn
    
    def initialize_database(self):
        """Initialize database with complete schema"""
        logger.info(f"Initializing database at: {self.db_path}")
        
        with self.get_connection() as conn:
            # Gardens table - Master garden information
            conn.execute("""
                CREATE TABLE IF NOT EXISTS gardens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    garden_type TEXT NOT NULL,
                    growing_method TEXT NOT NULL,
                    location TEXT,
                    dimensions_length REAL,
                    dimensions_width REAL,
                    dimensions_height REAL,
                    environmental_settings TEXT,  -- JSON
                    created_date TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    notes TEXT,
                    color_code TEXT DEFAULT '#4CAF50'
                )
            """)
            
            # Plants table - Individual plant tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS plants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    garden_id INTEGER NOT NULL,
                    plant_name TEXT NOT NULL,
                    strain_cultivar TEXT,
                    plant_type TEXT NOT NULL,
                    growth_stage TEXT NOT NULL,
                    planting_date TEXT NOT NULL,
                    expected_harvest_date TEXT,
                    current_week INTEGER DEFAULT 1,
                    health_status TEXT DEFAULT 'healthy',
                    location_in_garden TEXT,
                    notes TEXT,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY (garden_id) REFERENCES gardens (id) ON DELETE CASCADE
                )
            """)
            
            # Tasks table - All scheduled and completed tasks
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    garden_id INTEGER,
                    plant_id INTEGER,
                    title TEXT NOT NULL,
                    description TEXT,
                    task_type TEXT NOT NULL,
                    priority TEXT NOT NULL DEFAULT 'medium',
                    due_date TEXT NOT NULL,
                    due_time TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    completed_date TEXT,
                    recurring_pattern TEXT,  -- JSON for recurring tasks
                    weather_dependent BOOLEAN DEFAULT FALSE,
                    estimated_duration INTEGER,  -- minutes
                    cost REAL DEFAULT 0,
                    supplies_needed TEXT,  -- JSON array
                    notes TEXT,
                    created_date TEXT NOT NULL,
                    FOREIGN KEY (garden_id) REFERENCES gardens (id) ON DELETE SET NULL,
                    FOREIGN KEY (plant_id) REFERENCES plants (id) ON DELETE SET NULL
                )
            """)
            
            # Environmental readings table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS environmental_readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    garden_id INTEGER NOT NULL,
                    temperature REAL,
                    humidity REAL,
                    ph_level REAL,
                    ec_ppm REAL,
                    light_ppfd REAL,
                    co2_ppm REAL,
                    reading_time TEXT NOT NULL,
                    notes TEXT,
                    FOREIGN KEY (garden_id) REFERENCES gardens (id) ON DELETE CASCADE
                )
            """)
            
            # Inventory management
            conn.execute("""
                CREATE TABLE IF NOT EXISTS inventory_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    brand TEXT,
                    item_type TEXT,
                    current_quantity REAL NOT NULL DEFAULT 0,
                    unit_of_measure TEXT NOT NULL,
                    minimum_threshold REAL DEFAULT 0,
                    cost_per_unit REAL DEFAULT 0,
                    supplier TEXT,
                    storage_location TEXT,
                    expiration_date TEXT,
                    notes TEXT,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL
                )
            """)
            
            # Inventory transactions
            conn.execute("""
                CREATE TABLE IF NOT EXISTS inventory_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL,  -- 'purchase', 'use', 'waste', 'adjustment'
                    quantity REAL NOT NULL,
                    cost REAL DEFAULT 0,
                    transaction_date TEXT NOT NULL,
                    garden_id INTEGER,
                    task_id INTEGER,
                    notes TEXT,
                    FOREIGN KEY (item_id) REFERENCES inventory_items (id) ON DELETE CASCADE,
                    FOREIGN KEY (garden_id) REFERENCES gardens (id) ON DELETE SET NULL,
                    FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE SET NULL
                )
            """)
            
            # Cost tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cost_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    garden_id INTEGER,
                    category TEXT NOT NULL,  -- 'setup', 'utilities', 'supplies', 'maintenance'
                    subcategory TEXT,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    entry_date TEXT NOT NULL,
                    vendor TEXT,
                    receipt_path TEXT,
                    is_recurring BOOLEAN DEFAULT FALSE,
                    recurring_frequency TEXT,  -- 'monthly', 'weekly', etc.
                    notes TEXT,
                    FOREIGN KEY (garden_id) REFERENCES gardens (id) ON DELETE SET NULL
                )
            """)
            
            # Photos and documentation
            conn.execute("""
                CREATE TABLE IF NOT EXISTS photos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    garden_id INTEGER,
                    plant_id INTEGER,
                    file_path TEXT NOT NULL,
                    thumbnail_path TEXT,
                    caption TEXT,
                    photo_date TEXT NOT NULL,
                    growth_stage TEXT,
                    file_size INTEGER,
                    image_width INTEGER,
                    image_height INTEGER,
                    FOREIGN KEY (garden_id) REFERENCES gardens (id) ON DELETE CASCADE,
                    FOREIGN KEY (plant_id) REFERENCES plants (id) ON DELETE CASCADE
                )
            """)
            
            # Harvest tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS harvests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plant_id INTEGER NOT NULL,
                    garden_id INTEGER NOT NULL,
                    harvest_date TEXT NOT NULL,
                    fresh_weight REAL,
                    dry_weight REAL,
                    quality_rating INTEGER,  -- 1-10 scale
                    trichome_stage TEXT,
                    harvest_notes TEXT,
                    curing_start_date TEXT,
                    curing_notes TEXT,
                    final_yield REAL,
                    storage_location TEXT,
                    FOREIGN KEY (plant_id) REFERENCES plants (id) ON DELETE CASCADE,
                    FOREIGN KEY (garden_id) REFERENCES gardens (id) ON DELETE CASCADE
                )
            """)
            
            # User preferences and settings
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_name TEXT NOT NULL UNIQUE,
                    setting_value TEXT NOT NULL,
                    setting_type TEXT NOT NULL DEFAULT 'string',
                    last_updated TEXT NOT NULL
                )
            """)
            
            # Create indexes for better performance
            self.create_indexes(conn)
            
            # Insert default settings if database is new
            self.initialize_default_settings(conn)
            
            conn.commit()
        
        logger.info("Database initialization completed successfully")
    
    def create_indexes(self, conn: sqlite3.Connection):
        """Create database indexes for performance optimization"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks (due_date)",
            "CREATE INDEX IF NOT EXISTS idx_tasks_garden_id ON tasks (garden_id)",
            "CREATE INDEX IF NOT EXISTS idx_plants_garden_id ON plants (garden_id)",
            "CREATE INDEX IF NOT EXISTS idx_environmental_garden_time ON environmental_readings (garden_id, reading_time)",
            "CREATE INDEX IF NOT EXISTS idx_inventory_category ON inventory_items (category)",
            "CREATE INDEX IF NOT EXISTS idx_transactions_item_date ON inventory_transactions (item_id, transaction_date)",
            "CREATE INDEX IF NOT EXISTS idx_costs_garden_date ON cost_entries (garden_id, entry_date)",
            "CREATE INDEX IF NOT EXISTS idx_photos_garden_date ON photos (garden_id, photo_date)"
        ]
        
        for index_sql in indexes:
            conn.execute(index_sql)
    
    def initialize_default_settings(self, conn: sqlite3.Connection):
        """Initialize default application settings"""
        default_settings = [
            ("theme", "dark", "string"),
            ("temperature_unit", "fahrenheit", "string"),
            ("backup_frequency", "weekly", "string"),
            ("notification_enabled", "true", "boolean"),
            ("auto_save_interval", "300", "integer"),  # 5 minutes
            ("default_garden_type", "indoor", "string"),
            ("currency", "USD", "string")
        ]
        
        for setting_name, setting_value, setting_type in default_settings:
            conn.execute("""
                INSERT OR IGNORE INTO user_settings (setting_name, setting_value, setting_type, last_updated)
                VALUES (?, ?, ?, ?)
            """, (setting_name, setting_value, setting_type, datetime.now().isoformat()))
    
    # Garden Management Methods
    def create_garden(self, garden_data: Dict) -> int:
        """Create new garden and return garden ID"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO gardens (name, garden_type, growing_method, location, 
                                   dimensions_length, dimensions_width, dimensions_height,
                                   environmental_settings, created_date, status, notes, color_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                garden_data['name'],
                garden_data['garden_type'],
                garden_data['growing_method'],
                garden_data.get('location', ''),
                garden_data.get('dimensions_length', 0),
                garden_data.get('dimensions_width', 0),
                garden_data.get('dimensions_height', 0),
                json.dumps(garden_data.get('environmental_settings', {})),
                datetime.now().isoformat(),
                'active',
                garden_data.get('notes', ''),
                garden_data.get('color_code', '#4CAF50')
            ))
            
            garden_id = cursor.lastrowid
            conn.commit()
            logger.info(f"Created garden '{garden_data['name']}' with ID {garden_id}")
            return garden_id
    
    def get_all_gardens(self) -> List[Dict]:
        """Get all gardens with basic information"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT g.*, 
                       COUNT(p.id) as plant_count,
                       COUNT(CASE WHEN t.completed = 0 AND DATE(t.due_date) = DATE('now') THEN 1 END) as tasks_due_today
                FROM gardens g
                LEFT JOIN plants p ON g.id = p.garden_id
                LEFT JOIN tasks t ON g.id = t.garden_id
                WHERE g.status = 'active'
                GROUP BY g.id
                ORDER BY g.name
            """)
            
            gardens = []
            for row in cursor.fetchall():
                garden = dict(row)
                garden['environmental_settings'] = json.loads(garden['environmental_settings'] or '{}')
                gardens.append(garden)
            
            return gardens
    
    def get_garden_details(self, garden_id: int) -> Optional[Dict]:
        """Get detailed garden information including plants and recent activity"""
        with self.get_connection() as conn:
            # Get garden info
            cursor = conn.execute("SELECT * FROM gardens WHERE id = ?", (garden_id,))
            garden = cursor.fetchone()
            if not garden:
                return None
            
            garden_dict = dict(garden)
            garden_dict['environmental_settings'] = json.loads(garden_dict['environmental_settings'] or '{}')
            
            # Get plants in garden
            cursor = conn.execute("""
                SELECT * FROM plants WHERE garden_id = ? ORDER BY planting_date DESC
            """, (garden_id,))
            garden_dict['plants'] = [dict(row) for row in cursor.fetchall()]
            
            # Get pending tasks
            cursor = conn.execute("""
                SELECT * FROM tasks 
                WHERE garden_id = ? AND completed = 0 
                ORDER BY due_date, priority DESC
                LIMIT 10
            """, (garden_id,))
            garden_dict['pending_tasks'] = [dict(row) for row in cursor.fetchall()]
            
            # Get recent environmental readings
            cursor = conn.execute("""
                SELECT * FROM environmental_readings 
                WHERE garden_id = ? 
                ORDER BY reading_time DESC 
                LIMIT 50
            """, (garden_id,))
            garden_dict['environmental_readings'] = [dict(row) for row in cursor.fetchall()]
            
            return garden_dict
    
    # Plant Management Methods
    def add_plant(self, plant_data: Dict) -> int:
        """Add new plant to garden"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO plants (garden_id, plant_name, strain_cultivar, plant_type, 
                                  growth_stage, planting_date, expected_harvest_date,
                                  location_in_garden, notes, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plant_data['garden_id'],
                plant_data['plant_name'],
                plant_data.get('strain_cultivar', ''),
                plant_data['plant_type'],
                plant_data.get('growth_stage', 'seedling'),
                plant_data['planting_date'],
                plant_data.get('expected_harvest_date'),
                plant_data.get('location_in_garden', ''),
                plant_data.get('notes', ''),
                datetime.now().isoformat()
            ))
            
            plant_id = cursor.lastrowid
            conn.commit()
            logger.info(f"Added plant '{plant_data['plant_name']}' with ID {plant_id}")
            return plant_id
    
    # Task Management Methods
    def create_task(self, task_data: Dict) -> int:
        """Create new task"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO tasks (garden_id, plant_id, title, description, task_type, 
                                 priority, due_date, due_time, recurring_pattern,
                                 weather_dependent, estimated_duration, cost, 
                                 supplies_needed, notes, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task_data.get('garden_id'),
                task_data.get('plant_id'),
                task_data['title'],
                task_data.get('description', ''),
                task_data['task_type'],
                task_data.get('priority', 'medium'),
                task_data['due_date'],
                task_data.get('due_time'),
                json.dumps(task_data.get('recurring_pattern', {})),
                task_data.get('weather_dependent', False),
                task_data.get('estimated_duration', 0),
                task_data.get('cost', 0),
                json.dumps(task_data.get('supplies_needed', [])),
                task_data.get('notes', ''),
                datetime.now().isoformat()
            ))
            
            task_id = cursor.lastrowid
            conn.commit()
            return task_id
    
    def get_tasks_for_date_range(self, start_date: str, end_date: str, 
                                garden_id: int = None) -> List[Dict]:
        """Get tasks within date range, optionally filtered by garden"""
        with self.get_connection() as conn:
            if garden_id:
                cursor = conn.execute("""
                    SELECT t.*, g.name as garden_name, p.plant_name 
                    FROM tasks t
                    LEFT JOIN gardens g ON t.garden_id = g.id
                    LEFT JOIN plants p ON t.plant_id = p.id
                    WHERE t.due_date BETWEEN ? AND ? AND t.garden_id = ?
                    ORDER BY t.due_date, t.priority DESC
                """, (start_date, end_date, garden_id))
            else:
                cursor = conn.execute("""
                    SELECT t.*, g.name as garden_name, p.plant_name 
                    FROM tasks t
                    LEFT JOIN gardens g ON t.garden_id = g.id
                    LEFT JOIN plants p ON t.plant_id = p.id
                    WHERE t.due_date BETWEEN ? AND ?
                    ORDER BY t.due_date, t.priority DESC
                """, (start_date, end_date))
            
            tasks = []
            for row in cursor.fetchall():
                task = dict(row)
                task['recurring_pattern'] = json.loads(task['recurring_pattern'] or '{}')
                task['supplies_needed'] = json.loads(task['supplies_needed'] or '[]')
                tasks.append(task)
            
            return tasks
    
    def complete_task(self, task_id: int, completion_notes: str = '') -> bool:
        """Mark task as completed"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                UPDATE tasks 
                SET completed = TRUE, completed_date = ?, notes = COALESCE(notes, '') || ?
                WHERE id = ?
            """, (datetime.now().isoformat(), f"\nCompleted: {completion_notes}", task_id))
            
            success = cursor.rowcount > 0
            conn.commit()
            return success
    
    # Backup and Maintenance
    def create_backup(self) -> str:
        """Create database backup and return backup file path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"growmaster_backup_{timestamp}.db"
        backup_path = self.backup_dir / backup_filename
        
        try:
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backup created: {backup_path}")
            return str(backup_path)
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise
    
    def get_database_stats(self) -> Dict:
        """Get database statistics for monitoring"""
        with self.get_connection() as conn:
            stats = {}
            
            # Count records in main tables
            tables = ['gardens', 'plants', 'tasks', 'environmental_readings', 
                     'inventory_items', 'cost_entries', 'photos']
            
            for table in tables:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                stats[f"{table}_count"] = cursor.fetchone()[0]
            
            # Database file size
            stats['db_file_size_mb'] = os.path.getsize(self.db_path) / (1024 * 1024)
            
            # Last backup info
            if self.backup_dir.exists():
                backup_files = list(self.backup_dir.glob("growmaster_backup_*.db"))
                if backup_files:
                    latest_backup = max(backup_files, key=os.path.getctime)
                    stats['last_backup'] = latest_backup.name
                    stats['last_backup_date'] = datetime.fromtimestamp(
                        os.path.getctime(latest_backup)
                    ).isoformat()
            
            return stats

# Global database manager instance  
db_manager = DatabaseManager()
