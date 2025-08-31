#!/usr/bin/env python3
"""
Main ETL runner script for GovMate.
Processes all real datasets and loads them into the database.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_etl_pipeline():
    """Run the complete ETL pipeline."""
    
    logger.info("Starting GovMate ETL pipeline...")
    
    # Create processed directory
    processed_dir = Path("data/processed")
    processed_dir.mkdir(exist_ok=True)
    
    # Import ETL modules
    try:
        from services.etl.etl_seifa import process_seifa_data
        from services.etl.etl_labour import process_labour_data
        from services.etl.etl_directories import main as process_directories
    except ImportError as e:
        logger.error(f"Failed to import ETL modules: {e}")
        return False
    
    # Run ETL processes
    success = True
    
    # 1. Process SEIFA data
    logger.info("Processing SEIFA data...")
    if not process_seifa_data():
        logger.error("SEIFA ETL failed")
        success = False
    
    # 2. Process Labour Force data
    logger.info("Processing Labour Force data...")
    if not process_labour_data():
        logger.error("Labour Force ETL failed")
        success = False
    
    # 3. Process Government Directories data
    logger.info("Processing Government Directories data...")
    if not process_directories():
        logger.error("Directories ETL failed")
        success = False
    
    # 4. Load data into database
    logger.info("Loading data into database...")
    if not load_to_database():
        logger.error("Database loading failed")
        success = False
    
    if success:
        logger.info("ETL pipeline completed successfully!")
    else:
        logger.error("ETL pipeline failed!")
    
    return success

def load_to_database():
    """Load processed data into the database."""
    
    try:
        # Import database modules
        from services.api.database import engine
        from services.api.models import SeifaSA2, LabourStateMonthly, Agency, ServiceLocation
        
        # Load SEIFA data
        seifa_file = "data/processed/seifa_sa2.csv"
        if os.path.exists(seifa_file):
            import pandas as pd
            df = pd.read_csv(seifa_file)
            
            with engine.begin() as conn:
                # Clear existing data
                conn.execute(SeifaSA2.__table__.delete())
                # Insert new data
                conn.execute(SeifaSA2.__table__.insert(), df.to_dict(orient="records"))
            
            logger.info(f"Loaded {len(df)} SEIFA records")
        
        # Load Labour data
        labour_file = "data/processed/labour_state_monthly.csv"
        if os.path.exists(labour_file):
            df = pd.read_csv(labour_file)
            
            with engine.begin() as conn:
                # Clear existing data
                conn.execute(LabourStateMonthly.__table__.delete())
                # Insert new data
                conn.execute(LabourStateMonthly.__table__.insert(), df.to_dict(orient="records"))
            
            logger.info(f"Loaded {len(df)} Labour records")
        
        # Load Agencies data
        agencies_file = "data/processed/agencies.csv"
        if os.path.exists(agencies_file):
            df = pd.read_csv(agencies_file)
            
            with engine.begin() as conn:
                # Clear existing data
                conn.execute(Agency.__table__.delete())
                # Insert new data
                conn.execute(Agency.__table__.insert(), df.to_dict(orient="records"))
            
            logger.info(f"Loaded {len(df)} Agency records")
        
        # Load Service Locations data
        services_file = "data/processed/service_locations.csv"
        if os.path.exists(services_file):
            df = pd.read_csv(services_file)
            
            with engine.begin() as conn:
                # Clear existing data
                conn.execute(ServiceLocation.__table__.delete())
                # Insert new data
                conn.execute(ServiceLocation.__table__.insert(), df.to_dict(orient="records"))
            
            logger.info(f"Loaded {len(df)} Service Location records")
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading data to database: {e}")
        return False

if __name__ == "__main__":
    success = run_etl_pipeline()
    if not success:
        sys.exit(1)