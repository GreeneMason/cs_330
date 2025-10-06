import pandas as pd
import sqlite3
from pathlib import Path

# Read the CSV file
csv_path = Path('data/UFC dataset/Fighter stats/fighter_stats.csv')
df = pd.read_csv(csv_path)

# Create a SQLite database
db_path = Path('data/ufc_database.db')
conn = sqlite3.connect(db_path)

# Clean column names (remove spaces and special characters)
df.columns = [col.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('%', 'pct') for col in df.columns]

# Create table and import data
df.to_sql('fighter_stats', conn, index=False, if_exists='replace')

# Create indexes for commonly queried columns
cursor = conn.cursor()
cursor.execute('CREATE INDEX IF NOT EXISTS idx_fighter_name ON fighter_stats(name)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_fighter_wins ON fighter_stats(wins)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_fighter_losses ON fighter_stats(losses)')

# Verify the data
result = pd.read_sql('SELECT COUNT(*) as count FROM fighter_stats', conn)
print(f"Number of records imported: {result['count'][0]}")

# Show table structure
cursor.execute("PRAGMA table_info(fighter_stats)")
print("\nTable structure:")
for column in cursor.fetchall():
    print(f"{column[1]} ({column[2]})")

# Show sample data
print("\nSample data (first 5 rows):")
sample = pd.read_sql('SELECT * FROM fighter_stats LIMIT 5', conn)
print(sample)

conn.close()
print("\nDatabase created successfully at:", db_path.absolute())