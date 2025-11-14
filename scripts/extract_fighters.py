#!/usr/bin/env python3
"""
Extract unique fighter names from the dataset for the frontend fighter selection.
"""

import pandas as pd
import json
import sys
import os

def extract_fighters():
    """Extract unique fighter names from the dataset."""
    
    # Load the dataset
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'event_normalized_large_dataset.csv')
    
    try:
        df = pd.read_csv(data_path)
        print(f"Loaded dataset with {len(df)} rows")
        
        # Get unique fighters from both red and blue fighter columns
        red_fighters = set(df['r_fighter'].unique())
        blue_fighters = set(df['b_fighter'].unique())
        
        # Combine and sort all unique fighters
        all_fighters = sorted(list(red_fighters.union(blue_fighters)))
        
        print(f"Found {len(all_fighters)} unique fighters")
        
        # Create fighter data with additional info
        fighter_data = []
        for fighter in all_fighters:
            # Get fighter stats from most recent fight
            red_fights = df[df['r_fighter'] == fighter]
            blue_fights = df[df['b_fighter'] == fighter]
            
            # Get most recent fight data
            if not red_fights.empty:
                recent_red = red_fights.iloc[-1]
                fighter_info = {
                    'name': fighter,
                    'recent_weight_class': str(recent_red['weight_class']),
                    'recent_age': float(recent_red['r_age']) if pd.notna(recent_red['r_age']) else None,
                    'height': float(recent_red['r_height']) if pd.notna(recent_red['r_height']) else None,
                    'reach': float(recent_red['r_reach']) if pd.notna(recent_red['r_reach']) else None,
                    'stance': str(recent_red['r_stance']),
                    'wins': int(recent_red['r_wins_total']) if pd.notna(recent_red['r_wins_total']) else 0,
                    'losses': int(recent_red['r_losses_total']) if pd.notna(recent_red['r_losses_total']) else 0
                }
            elif not blue_fights.empty:
                recent_blue = blue_fights.iloc[-1]
                fighter_info = {
                    'name': fighter,
                    'recent_weight_class': str(recent_blue['weight_class']),
                    'recent_age': float(recent_blue['b_age']) if pd.notna(recent_blue['b_age']) else None,
                    'height': float(recent_blue['b_height']) if pd.notna(recent_blue['b_height']) else None,
                    'reach': float(recent_blue['b_reach']) if pd.notna(recent_blue['b_reach']) else None,
                    'stance': str(recent_blue['b_stance']),
                    'wins': int(recent_blue['b_wins_total']) if pd.notna(recent_blue['b_wins_total']) else 0,
                    'losses': int(recent_blue['b_losses_total']) if pd.notna(recent_blue['b_losses_total']) else 0
                }
            else:
                continue
                
            fighter_data.append(fighter_info)
        
        # Save to JSON file for frontend
        output_path = os.path.join(os.path.dirname(__file__), '..', 'ufc-prediction-frontend', 'public', 'fighters.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(fighter_data, f, indent=2)
        
        print(f"Saved fighter data to {output_path}")
        
        # Also create a simple names list
        names_only = [f['name'] for f in fighter_data]
        names_path = os.path.join(os.path.dirname(__file__), '..', 'ufc-prediction-frontend', 'public', 'fighter_names.json')
        
        with open(names_path, 'w') as f:
            json.dump(names_only, f, indent=2)
            
        print(f"Saved fighter names to {names_path}")
        
        # Show some sample fighters
        print("\nSample fighters:")
        for fighter in fighter_data[:10]:
            print(f"  {fighter['name']} - {fighter['recent_weight_class']} ({fighter['wins']}-{fighter['losses']})")
        
        return fighter_data
        
    except Exception as e:
        print(f"Error extracting fighters: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extract_fighters()