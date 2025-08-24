#!/usr/bin/env python3
"""
GrowMaster Pro - Professional Multi-Garden Management System
Main Application Entry Point

Author: GrowMaster Development Team
Version: 1.0.0
License: Proprietary
"""

import sys
import os
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('growmaster.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    try:
        logger.info("Starting GrowMaster Pro...")
        
        # Import GUI components after path setup
        import tkinter as tk
        from gui.main_window_tk import MainWindow
        from config.settings import Settings
        
        # Initialize application settings
        settings = Settings()
        logger.info("Application settings initialized")
        
        # Create and run main window
        app = MainWindow()
        logger.info("Main window created successfully")
        
        # Start the application
        app.run()
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        print(f"Error: Missing dependencies. Please run 'pip install -r requirements.txt'")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
