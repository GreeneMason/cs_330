#!/usr/bin/env python3
"""
Simple script to test individual fighter creation via Convex CLI.
This creates a few sample fighters to verify the database works.
"""

import subprocess
import json
import os

def create_test_fighters():
    """Create a few test fighters using the Convex CLI."""
    
    # Sample fighters to test with
    test_fighters = [
        {
            "name": "Jon Jones",
            "weightClass": "Heavyweight",
            "wins": 27,
            "losses": 1,
            "draws": 0
        },
        {
            "name": "Islam Makhachev", 
            "weightClass": "Lightweight",
            "wins": 25,
            "losses": 1,
            "draws": 0
        },
        {
            "name": "Alexander Volkanovski",
            "weightClass": "Featherweight", 
            "wins": 26,
            "losses": 3,
            "draws": 0
        }
    ]
    
    os.chdir("frontend")
    
    print("Creating test fighters...")
    
    for i, fighter in enumerate(test_fighters, 1):
        print(f"\n{i}. Creating {fighter['name']}...")
        
        # Create a temporary JSON file
        temp_file = f"temp_fighter_{i}.json"
        with open(temp_file, 'w') as f:
            json.dump(fighter, f)
        
        try:
            # Use PowerShell to run the command with proper JSON formatting
            cmd = f'Get-Content {temp_file} | npx convex run fighters:createFighter'
            
            result = subprocess.run(
                ["powershell", "-Command", cmd],
                capture_output=True,
                text=True,
                cwd="."
            )
            
            if result.returncode == 0:
                print(f"   ✅ {fighter['name']} created successfully")
            else:
                print(f"   ❌ Failed to create {fighter['name']}: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ Error creating {fighter['name']}: {e}")
        
        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    # Test listing fighters
    print("\n📊 Testing fighter list...")
    try:
        result = subprocess.run(
            ["powershell", "-Command", "echo '{}' | npx convex run fighters:listFighters"],
            capture_output=True,
            text=True,
            cwd="."
        )
        
        if result.returncode == 0:
            fighters = json.loads(result.stdout.strip())
            print(f"   ✅ Database now contains {len(fighters)} fighters")
            for fighter in fighters:
                print(f"      - {fighter.get('name', 'Unknown')} ({fighter.get('weightClass', 'Unknown')})")
        else:
            print(f"   ❌ Failed to list fighters: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Error listing fighters: {e}")

if __name__ == "__main__":
    create_test_fighters()