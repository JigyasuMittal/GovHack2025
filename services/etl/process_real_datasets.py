#!/usr/bin/env python3
"""
Process real datasets for GovMate AI Agent.
This script processes actual government datasets and creates service data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import json
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

def process_seifa_data():
    """Process SEIFA (Socioeconomic Index) data."""
    print("Processing SEIFA data...")
    
    seifa_path = project_root / "datasets" / "Statistical Area Level 1, Indexes, SEIFA 2021.xlsx"
    
    if seifa_path.exists():
        try:
            # Read the SEIFA data
            seifa_df = pd.read_excel(seifa_path, sheet_name="Table 1")
            
            # Extract relevant columns
            seifa_clean = seifa_df[['SA2_NAME_2021', 'STATE_NAME_2021', 'IRSAD_2021_Score', 'IRSAD_2021_Decile']].copy()
            seifa_clean.columns = ['sa2_name', 'state', 'irsad_score', 'irsad_decile']
            
            # Calculate rank
            seifa_clean['irsad_rank'] = seifa_clean['irsad_score'].rank(method='min', ascending=False).astype(int)
            
            # Filter for Queensland data (focus on Brisbane area)
            qld_data = seifa_clean[seifa_clean['state'] == 'Queensland'].copy()
            
            # Get top areas for service placement
            top_areas = qld_data.nlargest(10, 'irsad_score')
            
            print(f"✅ Processed SEIFA data: {len(seifa_clean)} records")
            return seifa_clean, top_areas
            
        except Exception as e:
            print(f"❌ Error processing SEIFA data: {e}")
            return None, None
    else:
        print("❌ SEIFA dataset not found")
        return None, None

def process_labour_data():
    """Process labour force data."""
    print("Processing labour force data...")
    
    labour_path = project_root / "datasets" / "Unemployment rate.csv"
    
    if labour_path.exists():
        try:
            labour_df = pd.read_csv(labour_path)
            
            # Extract state-level data
            state_data = labour_df[labour_df['State'] == 'Queensland'].copy()
            
            # Get latest data
            latest_data = state_data.iloc[-1] if not state_data.empty else None
            
            print(f"✅ Processed labour data: {len(labour_df)} records")
            return labour_df, latest_data
            
        except Exception as e:
            print(f"❌ Error processing labour data: {e}")
            return None, None
    else:
        print("❌ Labour dataset not found")
        return None, None

def create_service_locations(seifa_data):
    """Create service locations based on SEIFA data and real government services."""
    print("Creating service locations...")
    
    # Real government service locations in Brisbane area
    services = [
        {
            "id": 1,
            "name": "Job Seeker Centrelink - Brisbane City",
            "description": "Services Australia Centrelink office for unemployment benefits and job seeker support",
            "category": "employment support",
            "agency": "Services Australia",
            "address": "56 Edward Street",
            "suburb": "Brisbane City",
            "state": "QLD",
            "latitude": -27.4679,
            "longitude": 153.0281,
            "phone": "1328502300",
            "website": "https://www.servicesaustralia.gov.au"
        },
        {
            "id": 2,
            "name": "Food Bank South Brisbane",
            "description": "Community food bank providing free groceries to individuals and families in need",
            "category": "food assistance",
            "agency": "Foodbank Queensland",
            "address": "5 Merivale Street",
            "suburb": "South Brisbane",
            "state": "QLD",
            "latitude": -27.4850,
            "longitude": 153.0230,
            "phone": "0739000455",
            "website": "https://www.foodbank.org.au"
        },
        {
            "id": 3,
            "name": "Queensland Transport and Main Roads - Driver Licensing",
            "description": "Service centre for driver licence tests, renewals and vehicle registrations",
            "category": "driving licence",
            "agency": "Queensland Transport and Main Roads",
            "address": "77 George Street",
            "suburb": "Brisbane City",
            "state": "QLD",
            "latitude": -27.4670,
            "longitude": 153.0170,
            "phone": "132380",
            "website": "https://www.qld.gov.au/transport"
        },
        {
            "id": 4,
            "name": "Public Housing Service Office - Brisbane",
            "description": "Provides assistance with public housing applications and tenancy support",
            "category": "housing support",
            "agency": "Queensland Housing Department",
            "address": "50 Tank Street",
            "suburb": "Brisbane City",
            "state": "QLD",
            "latitude": -27.4620,
            "longitude": 153.0300,
            "phone": "131287",
            "website": "https://www.qld.gov.au/housing"
        },
        {
            "id": 5,
            "name": "Medicare Service Centre - Brisbane",
            "description": "Medicare service centre for health insurance and Medicare enquiries",
            "category": "health insurance",
            "agency": "Services Australia",
            "address": "141 Queen Street",
            "suburb": "Brisbane City",
            "state": "QLD",
            "latitude": -27.4679,
            "longitude": 153.0260,
            "phone": "132011",
            "website": "https://www.servicesaustralia.gov.au/medicare"
        },
        {
            "id": 6,
            "name": "Multicultural Service Centre - South Brisbane",
            "description": "Supports migrants with settlement, language and translation services",
            "category": "community support",
            "agency": "Multicultural Australia",
            "address": "20 Russell Street",
            "suburb": "South Brisbane",
            "state": "QLD",
            "latitude": -27.4600,
            "longitude": 153.0300,
            "phone": "0733508700",
            "website": "https://www.multiculturalaustralia.org.au"
        },
        {
            "id": 7,
            "name": "Centrelink - Fortitude Valley",
            "description": "Services Australia office for social security and welfare payments",
            "category": "employment support",
            "agency": "Services Australia",
            "address": "690 Ann Street",
            "suburb": "Fortitude Valley",
            "state": "QLD",
            "latitude": -27.4560,
            "longitude": 153.0350,
            "phone": "1328502300",
            "website": "https://www.servicesaustralia.gov.au"
        },
        {
            "id": 8,
            "name": "Queensland Transport - Vehicle Registration",
            "description": "Vehicle registration and licensing services",
            "category": "driving licence",
            "agency": "Queensland Transport and Main Roads",
            "address": "150 George Street",
            "suburb": "Brisbane City",
            "state": "QLD",
            "latitude": -27.4680,
            "longitude": 153.0250,
            "phone": "132380",
            "website": "https://www.qld.gov.au/transport"
        }
    ]
    
    # Add SEIFA context to services
    if seifa_data is not None:
        for service in services:
            # Find matching SEIFA data for the suburb
            suburb_data = seifa_data[seifa_data['sa2_name'].str.contains(service['suburb'], case=False, na=False)]
            if not suburb_data.empty:
                service['seifa_score'] = float(suburb_data.iloc[0]['irsad_score'])
                service['seifa_decile'] = int(suburb_data.iloc[0]['irsad_decile'])
            else:
                service['seifa_score'] = 1000.0  # Default
                service['seifa_decile'] = 7  # Default
    
    print(f"✅ Created {len(services)} service locations")
    return services

def process_employment_data():
    """Process employment and unemployment data."""
    print("Processing employment data...")
    
    employment_path = project_root / "datasets" / "Employed people.csv"
    unemployment_path = project_root / "datasets" / "Unemployment rate.csv"
    
    employment_data = {}
    
    if employment_path.exists():
        try:
            emp_df = pd.read_csv(employment_path)
            qld_emp = emp_df[emp_df['State'] == 'Queensland']
            if not qld_emp.empty:
                employment_data['employed'] = int(qld_emp.iloc[-1]['Employed people'])
        except Exception as e:
            print(f"❌ Error processing employment data: {e}")
    
    if unemployment_path.exists():
        try:
            unemp_df = pd.read_csv(unemployment_path)
            qld_unemp = unemp_df[unemp_df['State'] == 'Queensland']
            if not qld_unemp.empty:
                employment_data['unemployment_rate'] = float(qld_unemp.iloc[-1]['Unemployment rate'])
        except Exception as e:
            print(f"❌ Error processing unemployment data: {e}")
    
    print(f"✅ Processed employment data: {employment_data}")
    return employment_data

def main():
    """Main ETL process."""
    print("🚀 Starting real dataset processing for GovMate AI Agent")
    print("=" * 60)
    
    # Process SEIFA data
    seifa_data, top_areas = process_seifa_data()
    
    # Process labour data
    labour_data, latest_labour = process_labour_data()
    
    # Process employment data
    employment_data = process_employment_data()
    
    # Create service locations
    services = create_service_locations(seifa_data)
    
    # Create processed data structure
    processed_data = {
        'services': services,
        'seifa_data': seifa_data.to_dict('records') if seifa_data is not None else [],
        'labour_data': labour_data.to_dict('records') if labour_data is not None else [],
        'employment_data': employment_data,
        'top_areas': top_areas.to_dict('records') if top_areas is not None else []
    }
    
    # Save processed data
    output_path = project_root / "services" / "api" / "processed_data.json"
    with open(output_path, 'w') as f:
        json.dump(processed_data, f, indent=2, default=str)
    
    print(f"✅ Saved processed data to {output_path}")
    
    # Print summary
    print("\n📊 Data Processing Summary:")
    print(f"- Services: {len(services)} locations")
    print(f"- SEIFA records: {len(processed_data['seifa_data'])}")
    print(f"- Labour records: {len(processed_data['labour_data'])}")
    print(f"- Employment data: {employment_data}")
    
    print("\n🎉 Real dataset processing complete!")
    return processed_data

if __name__ == "__main__":
    main()
