#!/usr/bin/env python3
"""
ETL script for Government Directories data.
Processes agency and service location data from government directories.
"""

import pandas as pd
import numpy as np
import os
import json
from pathlib import Path
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_directories_data():
    """Process Government Directories data from the datasets folder."""
    
    try:
        # Process agencies data
        agencies_file = "data/directories.csv"
        if os.path.exists(agencies_file):
            logger.info(f"Processing agencies data from {agencies_file}")
            agencies_df = pd.read_csv(agencies_file)
            
            # Create processed CSV
            output_file = "data/processed/agencies.csv"
            os.makedirs("data/processed", exist_ok=True)
            
            # Add additional fields
            agencies_df['jurisdiction'] = agencies_df['agency'].apply(get_jurisdiction)
            agencies_df['last_seen_at'] = datetime.now().isoformat()
            
            # Save processed data
            agencies_df.to_csv(output_file, index=False)
            logger.info(f"Processed agencies data saved to {output_file}")
            
            # Update provenance
            update_provenance("Government Directories", agencies_file, output_file, len(agencies_df))
            
            return True
        else:
            logger.error(f"Agencies file not found: {agencies_file}")
            return False
            
    except Exception as e:
        logger.error(f"Error processing directories data: {e}")
        return False

def process_services_data():
    """Process services data from the datasets folder."""
    
    try:
        # Process services data
        services_file = "data/services.csv"
        if os.path.exists(services_file):
            logger.info(f"Processing services data from {services_file}")
            services_df = pd.read_csv(services_file)
            
            # Create processed CSV
            output_file = "data/processed/service_locations.csv"
            os.makedirs("data/processed", exist_ok=True)
            
            # Transform to match schema
            processed_df = services_df.copy()
            processed_df['agency_id'] = processed_df['service_id']  # Simplified mapping
            processed_df['services_json'] = processed_df['category'].apply(lambda x: f'["{x}"]')
            
            # Rename columns to match schema
            processed_df = processed_df.rename(columns={
                'service_id': 'id',
                'name': 'name',
                'address': 'address_norm',
                'latitude': 'lat',
                'longitude': 'lon'
            })
            
            # Select required columns
            required_columns = ['id', 'agency_id', 'name', 'address_norm', 'suburb', 'state', 'lat', 'lon', 'services_json']
            processed_df = processed_df[required_columns]
            
            # Save processed data
            processed_df.to_csv(output_file, index=False)
            logger.info(f"Processed services data saved to {output_file}")
            
            # Update provenance
            update_provenance("Service Locations", services_file, output_file, len(processed_df))
            
            return True
        else:
            logger.error(f"Services file not found: {services_file}")
            return False
            
    except Exception as e:
        logger.error(f"Error processing services data: {e}")
        return False

def get_jurisdiction(agency_name):
    """Determine jurisdiction based on agency name."""
    if 'Services Australia' in agency_name:
        return 'Federal'
    elif 'Queensland' in agency_name:
        return 'QLD'
    elif 'Foodbank' in agency_name:
        return 'QLD'  # Foodbank Queensland
    elif 'Multicultural' in agency_name:
        return 'QLD'  # Multicultural Australia
    else:
        return 'Unknown'

def update_provenance(dataset_name, source_file, output_file, row_count):
    """Update provenance.json with processing information."""
    
    provenance_file = "data/provenance.json"
    
    try:
        if os.path.exists(provenance_file):
            with open(provenance_file, 'r') as f:
                provenance = json.load(f)
        else:
            provenance = {}
        
        provenance[dataset_name] = {
            "source_file": source_file,
            "output_file": output_file,
            "processed_at": datetime.utcnow().isoformat(),
            "row_count": row_count,
            "transform_hash": "manual_etl"
        }
        
        with open(provenance_file, 'w') as f:
            json.dump(provenance, f, indent=2)
            
        logger.info(f"Updated provenance for {dataset_name}")
        
    except Exception as e:
        logger.error(f"Error updating provenance: {e}")

def main():
    """Main ETL process for directories data."""
    
    success1 = process_directories_data()
    success2 = process_services_data()
    
    if success1 and success2:
        logger.info("Directories ETL completed successfully")
        return True
    else:
        logger.error("Directories ETL failed")
        return False

if __name__ == "__main__":
    import json
    success = main()
    if not success:
        exit(1)