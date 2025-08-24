"""
GrowMaster Pro Configuration Management
Handles application settings, user preferences, and system configuration
"""

import os
import json
import configparser
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Settings:
    """Application settings manager with persistence"""
    
    def __init__(self):
        self.app_dir = Path.home() / "GrowMaster"
        self.config_file = self.app_dir / "config.json"
        self.data_dir = self.app_dir / "data"
        self.backup_dir = self.app_dir / "backups"
        
        # Create application directories
        self._create_directories()
        
        # Default settings
        self.defaults = {
            "app": {
                "version": "1.0.0",
                "first_run": True,
                "theme": "dark",
                "auto_backup": True,
                "backup_interval_days": 7
            },
            "gui": {
                "window_width": 1200,
                "window_height": 800,
                "window_maximized": False,
                "default_tab": "dashboard"
            },
            "notifications": {
                "enabled": True,
                "task_reminders": True,
                "low_stock_alerts": True,
                "desktop_notifications": True,
                "sound_enabled": False
            },
            "database": {
                "auto_backup": True,
                "max_backups": 10,
                "compress_backups": True
            },
            "security": {
                "password_protected": False,
                "encrypt_data": False,
                "session_timeout": 0
            },
            "calendar": {
                "default_view": "monthly",
                "week_start": "monday",
                "show_all_gardens": True,
                "color_scheme": "garden_based"
            }
        }
        
        # Load existing settings or create default
        self.settings = self._load_settings()
    
    def _create_directories(self):
        """Create necessary application directories"""
        directories = [self.app_dir, self.data_dir, self.backup_dir]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory created/verified: {directory}")
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self._merge_settings(self.defaults, loaded_settings)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load settings: {e}. Using defaults.")
                return self.defaults.copy()
        else:
            logger.info("No config file found. Using default settings.")
            return self.defaults.copy()
    
    def _merge_settings(self, defaults: Dict, loaded: Dict) -> Dict:
        """Recursively merge loaded settings with defaults"""
        result = defaults.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_settings(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, section: str, key: str, default=None) -> Any:
        """Get a setting value"""
        try:
            return self.settings[section][key]
        except KeyError:
            return default
    
    def set(self, section: str, key: str, value: Any):
        """Set a setting value"""
        if section not in self.settings:
            self.settings[section] = {}
        self.settings[section][key] = value
    
    def save(self):
        """Save settings to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            logger.info("Settings saved successfully")
        except IOError as e:
            logger.error(f"Failed to save settings: {e}")
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.defaults.copy()
        self.save()
        logger.info("Settings reset to defaults")
    
    def get_data_path(self) -> Path:
        """Get the data directory path"""
        return self.data_dir
    
    def get_backup_path(self) -> Path:
        """Get the backup directory path"""
        return self.backup_dir
    
    def is_first_run(self) -> bool:
        """Check if this is the first application run"""
        return self.get("app", "first_run", True)
    
    def mark_first_run_complete(self):
        """Mark first run as complete"""
        self.set("app", "first_run", False)
        self.save()
