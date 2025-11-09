import sqlite3

def inspect_database(db_path, db_name):
    print(f"\n{'='*60}")
    print(f"Database: {db_name}")
    print(f"{'='*60}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\nTables: {tables}")
    
    # For each table, get schema
    for table in tables:
        print(f"\n--- Table: {table} ---")
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, name, type_, notnull, default, pk = col
            pk_str = " PRIMARY KEY" if pk else ""
            null_str = " NOT NULL" if notnull else ""
            print(f"  {name}: {type_}{pk_str}{null_str}")
    
    conn.close()

# Inspect both databases
inspect_database('data/ufc_database.db', 'ufc_database.db')
inspect_database('data/normalized_ufc.db', 'normalized_ufc.db')
