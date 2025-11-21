import requests
import pandas as pd
import os
import json
from datetime import datetime

# Configuration
API_KEY = os.getenv("RAPIDAPI_KEY", "YOUR_API_KEY_HERE")
API_HOST = "mma-api1.p.rapidapi.com"
BASE_URL = "https://mma-api1.p.rapidapi.com"

def fetch_upcoming_events():
    """Fetch upcoming UFC events."""
    url = f"{BASE_URL}/upcoming"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching events: {e}")
        return None

def fetch_fighter_profile(fighter_name):
    """Fetch fighter profile by name."""
    url = f"{BASE_URL}/search"
    querystring = {"name": fighter_name}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching fighter {fighter_name}: {e}")
        return None

if __name__ == "__main__":
    print("🥊 UFC Data Updater (RapidAPI)")
    print("------------------------------")
    print("This script uses the 'MMA API' from RapidAPI.")
    print("You need to subscribe at: https://rapidapi.com/api-sports/api/mma-api1")
    print(f"Current API Key: {API_KEY}")
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("\n⚠️  Please set your RAPIDAPI_KEY environment variable or edit this script.")
    else:
        print("\nFetching upcoming events...")
        events = fetch_upcoming_events()
        if events:
            print(json.dumps(events, indent=2))
