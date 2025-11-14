import pandas as pd

def analyze_events():
    # Load the normalized dataset
    df = pd.read_csv('data/normalized_large_dataset.csv')
    
    # Check unique events
    unique_events = df['event_name'].unique()
    print(f"Total unique events: {len(unique_events)}")
    print(f"Total rows: {len(df)}")
    print(f"Average fights per event: {len(df) / len(unique_events):.1f}")
    
    print("\nSample events:")
    for i, event in enumerate(unique_events[:10]):
        count = len(df[df['event_name'] == event])
        print(f"  {i+1}. {event} ({count} fights)")
    
    print(f"\nEvent name statistics:")
    print(f"- Average event name length: {df['event_name'].str.len().mean():.1f} characters")
    print(f"- Max event name length: {df['event_name'].str.len().max()} characters")
    print(f"- Min event name length: {df['event_name'].str.len().min()} characters")
    
    # Calculate storage savings potential
    total_event_chars = df['event_name'].str.len().sum()
    total_rows = len(df)
    print(f"\nStorage analysis:")
    print(f"- Total characters used for event names: {total_event_chars:,}")
    print(f"- Storage with IDs (4 bytes per row): {total_rows * 4:,} bytes")
    print(f"- Storage with strings (assuming 1 byte per char): {total_event_chars:,} bytes")
    print(f"- Potential storage reduction: {((total_event_chars - (total_rows * 4)) / total_event_chars * 100):.1f}%")
    
    return unique_events, df

if __name__ == "__main__":
    events, dataset = analyze_events()