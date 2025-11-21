import json

# Load fighters data
with open('../frontend/public/fighters.json', 'r') as f:
    data = json.load(f)

print('First 5 fighters:')
for i in range(min(5, len(data))):
    fighter = data[i]
    print(f'{i+1}. Name: "{fighter["name"]}"')
    print(f'   Weight: {fighter["recent_weight_class"]}')
    print(f'   Record: {fighter["wins"]}-{fighter["losses"]}')
    print(f'   Age: {fighter["recent_age"]}')
    print()

# Check if any names are empty or None
empty_names = [f for f in data if not f.get("name") or f["name"].strip() == ""]
print(f"Fighters with empty names: {len(empty_names)}")
if empty_names:
    print("First few empty name entries:")
    for i, fighter in enumerate(empty_names[:3]):
        print(f"  {i+1}. {fighter}")