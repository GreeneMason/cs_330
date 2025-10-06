import pandas as pd
from pathlib import Path

# Read the CSV file
csv_path = Path('data/UFC dataset/Fighter stats/fighter_stats.csv')
df = pd.read_csv(csv_path)

# Print original column names
print("Original column names:")
print(df.columns.tolist())