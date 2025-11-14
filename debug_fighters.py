import pandas as pd
import json

# Load dataset
df = pd.read_csv('data/event_normalized_large_dataset.csv')

# Check Jon Jones data
jon_red = df[df['r_fighter'] == 'Jon Jones']
jon_blue = df[df['b_fighter'] == 'Jon Jones']

print("=== JON JONES DATA CHECK ===")
print(f"Jon Jones fights as red fighter: {len(jon_red)}")
print(f"Jon Jones fights as blue fighter: {len(jon_blue)}")

if not jon_red.empty:
    latest_red = jon_red.iloc[-1]
    print("\nJon Jones latest as RED fighter:")
    print(f"  Wins: {latest_red['r_wins_total']}")
    print(f"  Losses: {latest_red['r_losses_total']}")
    print(f"  Age: {latest_red['r_age']}")
    print(f"  Height: {latest_red['r_height']}")
    print(f"  Reach: {latest_red['r_reach']}")
    print(f"  Weight Class: {latest_red['weight_class']}")

if not jon_blue.empty:
    latest_blue = jon_blue.iloc[-1]
    print("\nJon Jones latest as BLUE fighter:")
    print(f"  Wins: {latest_blue['b_wins_total']}")
    print(f"  Losses: {latest_blue['b_losses_total']}")
    print(f"  Age: {latest_blue['b_age']}")
    print(f"  Height: {latest_blue['b_height']}")
    print(f"  Reach: {latest_blue['b_reach']}")
    print(f"  Weight Class: {latest_blue['weight_class']}")

# Now check what our extraction script would generate
with open('ufc-prediction-frontend/public/fighters.json', 'r') as f:
    fighters_data = json.load(f)

jon_data = next((f for f in fighters_data if f['name'] == 'Jon Jones'), None)
if jon_data:
    print("\n=== EXTRACTED FIGHTER DATA ===")
    print(f"Name: {jon_data['name']}")
    print(f"Wins: {jon_data['wins']}")
    print(f"Losses: {jon_data['losses']}")
    print(f"Age: {jon_data['recent_age']}")
    print(f"Height: {jon_data['height']}")
    print(f"Reach: {jon_data['reach']}")
    print(f"Weight Class: {jon_data['recent_weight_class']}")
else:
    print("Jon Jones not found in extracted data!")

# Check Amanda Ribas too
amanda_red = df[df['r_fighter'] == 'Amanda Ribas']
amanda_blue = df[df['b_fighter'] == 'Amanda Ribas']

print("\n=== AMANDA RIBAS DATA CHECK ===")
if not amanda_red.empty:
    latest_red = amanda_red.iloc[-1]
    print(f"Amanda as RED - Wins: {latest_red['r_wins_total']}, Losses: {latest_red['r_losses_total']}, Weight: {latest_red['weight_class']}")

if not amanda_blue.empty:
    latest_blue = amanda_blue.iloc[-1]
    print(f"Amanda as BLUE - Wins: {latest_blue['b_wins_total']}, Losses: {latest_blue['b_losses_total']}, Weight: {latest_blue['weight_class']}")

amanda_data = next((f for f in fighters_data if f['name'] == 'Amanda Ribas'), None)
if amanda_data:
    print(f"Extracted Amanda - Wins: {amanda_data['wins']}, Losses: {amanda_data['losses']}, Weight: {amanda_data['recent_weight_class']}")