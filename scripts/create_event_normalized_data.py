import pandas as pd
import sqlite3
import os

def create_event_normalized_dataset():
    """
    Create a new version of the normalized dataset with event IDs instead of event names,
    plus a separate events reference table.
    """
    
    # Load the current normalized dataset
    print("Loading normalized dataset...")
    df = pd.read_csv('data/normalized_large_dataset.csv')
    
    # Create event reference table
    print("Creating events reference table...")
    unique_events = df['event_name'].unique()
    events_df = pd.DataFrame({
        'event_id': range(1, len(unique_events) + 1),
        'event_name': unique_events
    })
    
    # Create a mapping dictionary
    event_to_id = dict(zip(events_df['event_name'], events_df['event_id']))
    
    # Replace event names with event IDs
    print("Mapping event names to IDs...")
    df_normalized = df.copy()
    df_normalized['event_id'] = df_normalized['event_name'].map(event_to_id)
    
    # Remove the original event_name column and reorder columns
    df_normalized = df_normalized.drop('event_name', axis=1)
    
    # Move event_id to the first column
    cols = ['event_id'] + [col for col in df_normalized.columns if col != 'event_id']
    df_normalized = df_normalized[cols]
    
    # Save the new normalized dataset
    output_file = 'data/event_normalized_large_dataset.csv'
    print(f"Saving event-normalized dataset to {output_file}...")
    df_normalized.to_csv(output_file, index=False)
    
    # Save the events reference table
    events_file = 'data/events_reference.csv'
    print(f"Saving events reference table to {events_file}...")
    events_df.to_csv(events_file, index=False)
    
    # Create SQLite database with both tables
    db_file = 'data/event_normalized_data.db'
    print(f"Creating SQLite database {db_file}...")
    conn = sqlite3.connect(db_file)
    
    # Create events table
    events_df.to_sql('events', conn, if_exists='replace', index=False)
    
    # Create fights table
    df_normalized.to_sql('fights', conn, if_exists='replace', index=False)
    
    # Create index on event_id for faster lookups
    conn.execute('CREATE INDEX IF NOT EXISTS idx_fights_event_id ON fights(event_id)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_events_event_id ON events(event_id)')
    
    conn.close()
    
    # Print statistics
    print("\n" + "="*60)
    print("EVENT NORMALIZATION COMPLETE")
    print("="*60)
    print(f"Original dataset: {len(df):,} fights")
    print(f"Unique events: {len(events_df):,}")
    print(f"Average fights per event: {len(df) / len(events_df):.1f}")
    
    # File size comparison
    original_size = os.path.getsize('data/normalized_large_dataset.csv')
    new_size = os.path.getsize(output_file)
    events_size = os.path.getsize(events_file)
    total_new_size = new_size + events_size
    
    print(f"\nFile size comparison:")
    print(f"- Original dataset: {original_size:,} bytes ({original_size/1024/1024:.2f} MB)")
    print(f"- New dataset: {new_size:,} bytes ({new_size/1024/1024:.2f} MB)")
    print(f"- Events table: {events_size:,} bytes ({events_size/1024:.2f} KB)")
    print(f"- Total new size: {total_new_size:,} bytes ({total_new_size/1024/1024:.2f} MB)")
    print(f"- Size reduction: {((original_size - total_new_size) / original_size * 100):.1f}%")
    
    print(f"\nCreated files:")
    print(f"- {output_file}")
    print(f"- {events_file}")
    print(f"- {db_file}")
    
    # Show sample data
    print(f"\nSample of event-normalized data:")
    print(df_normalized.head(3)[['event_id', 'r_fighter', 'b_fighter', 'winner']].to_string())
    
    print(f"\nSample of events reference table:")
    print(events_df.head(10).to_string())
    
    return df_normalized, events_df

def demonstrate_usage():
    """
    Demonstrate how to use the event-normalized data
    """
    print("\n" + "="*60)
    print("USAGE DEMONSTRATION")
    print("="*60)
    
    # Load the data
    fights_df = pd.read_csv('data/event_normalized_large_dataset.csv')
    events_df = pd.read_csv('data/events_reference.csv')
    
    # Example 1: Find all fights from a specific event
    event_name = "UFC 299: O'Malley vs. Vera 2"
    event_id = events_df[events_df['event_name'] == event_name]['event_id'].iloc[0]
    event_fights = fights_df[fights_df['event_id'] == event_id]
    
    print(f"\nExample 1: Fights from '{event_name}':")
    print(f"Event ID: {event_id}")
    print(f"Number of fights: {len(event_fights)}")
    print(event_fights[['event_id', 'r_fighter', 'b_fighter', 'winner']].head().to_string())
    
    # Example 2: Using SQL with SQLite
    print(f"\nExample 2: SQL query example")
    conn = sqlite3.connect('data/event_normalized_data.db')
    
    query = """
    SELECT e.event_name, COUNT(*) as fight_count
    FROM fights f
    JOIN events e ON f.event_id = e.event_id
    GROUP BY e.event_id, e.event_name
    ORDER BY fight_count DESC
    LIMIT 5
    """
    
    result = pd.read_sql_query(query, conn)
    print("Top 5 events by number of fights:")
    print(result.to_string())
    
    conn.close()

if __name__ == "__main__":
    # Create the event-normalized dataset
    normalized_data, events_reference = create_event_normalized_dataset()
    
    # Demonstrate usage
    demonstrate_usage()