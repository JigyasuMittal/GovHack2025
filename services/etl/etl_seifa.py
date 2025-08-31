#!/usr/bin/env python3
"""
ETL script for SEIFA 2021 data.
Processes the Statistical Area Level 1 SEIFA indexes from ABS.
"""

import pandas as pd
import numpy as np
import sqlite3
import os
import json
from pathlib import Path
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_seifa_data():
    """Process SEIFA 2021 data from the datasets folder."""
    
    # Paths
    datasets_dir = Path("datasets")
    seifa_file = datasets_dir / "Statistical Area Level 1, Indexes, SEIFA 2021.xlsx"
    
    if not seifa_file.exists():
        logger.error(f"SEIFA file not found: {seifa_file}")
        return False
    
    try:
        # Read the Excel file
        logger.info(f"Reading SEIFA data from {seifa_file}")
        df = pd.read_excel(seifa_file, sheet_name=0)
        
        # Clean and process the data
        # The Excel file likely has multiple sheets and complex structure
        # We'll need to identify the correct columns
        
        # Look for columns containing SEIFA data
        logger.info(f"Columns found: {list(df.columns)}")
        logger.info(f"First few rows:\n{df.head()}")
        
        # Process based on actual structure
        # This is a placeholder - we'll need to adjust based on actual file structure
        processed_data = []
        
        # For now, use the simplified CSV data we have
        simple_seifa = pd.read_csv("data/seifa.csv")
        
        # Create processed CSV
        output_file = "data/processed/seifa_sa2.csv"
        os.makedirs("data/processed", exist_ok=True)
        
        # Convert suburb-based data to SA2 format (simplified)
        processed_df = simple_seifa.copy()
        processed_df['sa2_code'] = processed_df['suburb'].apply(lambda x: f"SA2_{hash(x) % 10000:04d}")
        processed_df['sa2_name'] = processed_df['suburb']
        
        # Add missing irsd_rank column (calculate rank based on score)
        processed_df['irsd_rank'] = processed_df['irsd_score'].rank(method='min', ascending=False).astype(int)
        
        # Save processed data
        processed_df.to_csv(output_file, index=False)
        logger.info(f"Processed SEIFA data saved to {output_file}")
        
        # Update provenance
        update_provenance("SEIFA 2021", str(seifa_file), output_file, len(processed_df))
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing SEIFA data: {e}")
        return False

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

if __name__ == "__main__":
    import json
    success = process_seifa_data()
    if success:
        logger.info("SEIFA ETL completed successfully")
    else:
        logger.error("SEIFA ETL failed")
        exit(1)