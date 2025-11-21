#!/usr/bin/env python3
"""
Migrate fighter data from CSV to Convex database.
This script reads the event_normalized_large_dataset.csv file and extracts
unique fighter information, then sends it to Convex via the bulk insert API.
"""

import pandas as pd
import json
import sys
import os
import requests
from typing import Dict, List, Optional, Any

def clean_numeric_value(value) -> Optional[float]:
    """Clean and convert numeric values, handling NaN and invalid values."""
    if pd.isna(value):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def clean_string_value(value) -> Optional[str]:
    """Clean string values, handling NaN and empty strings."""
    if pd.isna(value) or str(value).strip() == '':
        return None
    return str(value).strip()

def extract_fighter_data(csv_path: str) -> List[Dict[str, Any]]:
    """Extract unique fighter data from the CSV file."""
    
    print(f"Loading dataset from {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded dataset with {len(df)} rows")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []
    
    fighter_data = {}
    
    print("Processing red fighters...")
    # Process red fighters
    for _, row in df.iterrows():
        name = clean_string_value(row['r_fighter'])
        if not name:
            continue
            
        weight_class = clean_string_value(row['weight_class'])
        if not weight_class:
            continue
            
        # Get most recent data for this fighter (assuming CSV is chronologically ordered)
        if name not in fighter_data:
            fighter_data[name] = {
                'name': name,
                'weightClass': weight_class,
                'wins': int(clean_numeric_value(row['r_wins_total']) or 0),
                'losses': int(clean_numeric_value(row['r_losses_total']) or 0),
                'draws': 0,  # Not in the dataset
                'height': clean_numeric_value(row['r_height']),  # cm
                'weight': clean_numeric_value(row['r_weight']),  # kg  
                'reach': clean_numeric_value(row['r_reach']),    # cm
                'stance': clean_string_value(row['r_stance']),
                'age': clean_numeric_value(row['r_age']),
                'performance': {
                    'strikeLandedPerMinute': clean_numeric_value(row['r_SLpM_total']),
                    'strikeAbsorbedPerMinute': clean_numeric_value(row['r_SApM_total']),
                    'strikeAccuracy': clean_numeric_value(row['r_sig_str_acc_total']),
                    'strikeDefense': clean_numeric_value(row['r_str_def_total']),
                    'takedownAccuracy': clean_numeric_value(row['r_td_acc_total']),
                    'takedownDefense': clean_numeric_value(row['r_td_def_total']),
                    'submissionAverage': clean_numeric_value(row['r_sub_avg']),
                    'takedownAverage': clean_numeric_value(row['r_td_avg']),
                }
            }
        else:
            # Update with more recent data (later rows in CSV)
            fighter_data[name]['wins'] = int(clean_numeric_value(row['r_wins_total']) or fighter_data[name]['wins'])
            fighter_data[name]['losses'] = int(clean_numeric_value(row['r_losses_total']) or fighter_data[name]['losses'])
            if clean_numeric_value(row['r_age']):
                fighter_data[name]['age'] = clean_numeric_value(row['r_age'])
    
    print("Processing blue fighters...")
    # Process blue fighters
    for _, row in df.iterrows():
        name = clean_string_value(row['b_fighter'])
        if not name:
            continue
            
        weight_class = clean_string_value(row['weight_class'])
        if not weight_class:
            continue
            
        # Get most recent data for this fighter
        if name not in fighter_data:
            fighter_data[name] = {
                'name': name,
                'weightClass': weight_class,
                'wins': int(clean_numeric_value(row['b_wins_total']) or 0),
                'losses': int(clean_numeric_value(row['b_losses_total']) or 0),
                'draws': 0,  # Not in the dataset
                'height': clean_numeric_value(row['b_height']),  # cm
                'weight': clean_numeric_value(row['b_weight']),  # kg  
                'reach': clean_numeric_value(row['b_reach']),    # cm
                'stance': clean_string_value(row['b_stance']),
                'age': clean_numeric_value(row['b_age']),
                'performance': {
                    'strikeLandedPerMinute': clean_numeric_value(row['b_SLpM_total']),
                    'strikeAbsorbedPerMinute': clean_numeric_value(row['b_SApM_total']),
                    'strikeAccuracy': clean_numeric_value(row['b_sig_str_acc_total']),
                    'strikeDefense': clean_numeric_value(row['b_str_def_total']),
                    'takedownAccuracy': clean_numeric_value(row['b_td_acc_total']),
                    'takedownDefense': clean_numeric_value(row['b_td_def_total']),
                    'submissionAverage': clean_numeric_value(row['b_sub_avg']),
                    'takedownAverage': clean_numeric_value(row['b_td_avg']),
                }
            }
        else:
            # Update with more recent data (later rows in CSV)
            fighter_data[name]['wins'] = int(clean_numeric_value(row['b_wins_total']) or fighter_data[name]['wins'])
            fighter_data[name]['losses'] = int(clean_numeric_value(row['b_losses_total']) or fighter_data[name]['losses'])
            if clean_numeric_value(row['b_age']):
                fighter_data[name]['age'] = clean_numeric_value(row['b_age'])
    
    # Convert to list and clean up None values in performance
    fighters_list = []
    for fighter in fighter_data.values():
        # Filter out None values from performance dict
        if fighter['performance']:
            fighter['performance'] = {k: v for k, v in fighter['performance'].items() if v is not None}
            if not fighter['performance']:
                fighter['performance'] = None
        
        fighters_list.append(fighter)
    
    print(f"Extracted data for {len(fighters_list)} unique fighters")
    
    # Show some sample fighters
    print("\nSample fighters:")
    for fighter in fighters_list[:5]:
        print(f"  {fighter['name']} - {fighter['weightClass']} ({fighter['wins']}-{fighter['losses']})")
    
    return fighters_list

def save_fighter_data(fighters: List[Dict[str, Any]], output_path: str):
    """Save fighter data to JSON file."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(fighters, f, indent=2)
        print(f"Saved fighter data to {output_path}")
        return True
    except Exception as e:
        print(f"Error saving fighter data: {e}")
        return False

def batch_upload_to_convex(fighters: List[Dict[str, Any]], batch_size: int = 50):
    """Upload fighter data to Convex in batches using the bulkInsertFighters function."""
    
    # Note: This would normally require Convex client setup
    # For now, we'll save the data and provide instructions
    
    total_fighters = len(fighters)
    print(f"\nPreparing to upload {total_fighters} fighters to Convex...")
    
    # Save the data for manual import
    migration_data_path = os.path.join(os.path.dirname(__file__), 'fighter_migration_data.json')
    save_fighter_data(fighters, migration_data_path)
    
    print(f"""
Fighter migration data prepared!

To complete the migration:
1. The fighter data has been saved to: {migration_data_path}
2. You can use the Convex dashboard or a frontend script to call the bulkInsertFighters mutation
3. Or use the provided Node.js script to upload the data programmatically

Sample batches of {batch_size} fighters each would be uploaded.
Total batches needed: {(total_fighters + batch_size - 1) // batch_size}
""")
    
    return migration_data_path

def main():
    """Main migration function."""
    
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'data', 'event_normalized_large_dataset.csv')
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        print("Please ensure the dataset file exists.")
        sys.exit(1)
    
    print("=== UFC Fighter Data Migration ===")
    print("This script will extract fighter data from the CSV and prepare it for Convex import.")
    
    # Extract fighter data
    fighters = extract_fighter_data(csv_path)
    
    if not fighters:
        print("No fighter data extracted. Exiting.")
        sys.exit(1)
    
    # Upload to Convex (prepare for upload)
    migration_file = batch_upload_to_convex(fighters)
    
    print(f"\nMigration preparation complete!")
    print(f"Fighter data ready for import: {migration_file}")
    print(f"Total fighters prepared: {len(fighters)}")

if __name__ == "__main__":
    main()