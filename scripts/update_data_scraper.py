import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime

# Base URL for UFC Stats
BASE_URL = "http://ufcstats.com/statistics/events/completed"

def clean_text(text):
    """Clean whitespace from text."""
    if text:
        return text.strip()
    return ""

def get_latest_events():
    """Scrape the list of latest completed events."""
    print(f"Fetching events from {BASE_URL}...")
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    events = []
    rows = soup.find_all('tr', class_='b-statistics__table-row')
    
    for row in rows[2:]: # Skip header rows
        cols = row.find_all('td')
        if len(cols) >= 2:
            link_tag = cols[0].find('a')
            date_span = cols[0].find('span', class_='b-statistics__date')
            
            if link_tag:
                event_name = link_tag.text.strip()
                event_link = link_tag['href']
                
                date_str = ""
                if date_span:
                    date_str = date_span.text.strip()
                else:
                    # Fallback if date is just text
                    date_str = cols[0].get_text().replace(event_name, "").strip()
                
                location = cols[1].text.strip()
                
                events.append({
                    'name': event_name,
                    'link': event_link,
                    'date': date_str,
                    'location': location
                })
    
    return events

def scrape_event_fights(event_url):
    """Scrape the list of fights from an event page."""
    print(f"Fetching fights from {event_url}...")
    response = requests.get(event_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    fights = []
    rows = soup.find_all('tr', class_='b-fight-details__table-row')
    
    for row in rows:
        # Skip rows that are not fights (headers)
        if not row.get('data-link'):
            continue
            
        fight_link = row.get('data-link')
        cols = row.find_all('td')
        
        if len(cols) >= 7:
            # Extract basic info from the event page table
            fighter_names = cols[1].find_all('a')
            if len(fighter_names) == 2:
                r_fighter = fighter_names[0].text.strip()
                b_fighter = fighter_names[1].text.strip()
                
                weight_class = cols[6].text.strip()
                
                fights.append({
                    'link': fight_link,
                    'r_fighter': r_fighter,
                    'b_fighter': b_fighter,
                    'weight_class': weight_class
                })
    
    return fights

def parse_fight_stats(soup):
    """Parse the detailed stats from a fight page."""
    stats = {}
    
    # 1. General Fight Info (Method, Round, Time, etc.)
    # Usually in the top section
    details_div = soup.find('div', class_='b-fight-details__content')
    if details_div:
        # Method
        method_elem = details_div.find('i', style='font-style: normal')
        if method_elem:
            stats['method'] = method_elem.text.strip()
            
        # Round, Time, Format
        # Iterate through all 'i' tags which usually hold the labels
        for i_tag in details_div.find_all('i'):
            label = i_tag.text.strip()
            # The value is usually the next sibling text node
            if i_tag.next_sibling:
                value = i_tag.next_sibling.strip()
                if 'Round:' in label:
                    stats['round'] = value
                elif 'Time:' in label:
                    stats['time'] = value
                elif 'Time format:' in label:
                    stats['format'] = value
                elif 'Referee:' in label:
                    stats['referee'] = value.strip()

    # 2. Totals Table (KD, Sig Str, Total Str, TD, Sub, etc.)
    # There are usually two tables: Totals and Significant Strikes
    # We need the first one for KD, TD, Sub, Rev, Ctrl
    
    tables = soup.find_all('table', class_='b-fight-details__table')
    
    if tables:
        # --- TOTALS TABLE ---
        totals_rows = tables[0].find_all('tr')
        if len(totals_rows) >= 2:
            # The second row usually contains the totals for the whole fight
            cols = totals_rows[1].find_all('td')
            if len(cols) >= 10:
                # Columns: Fighter, KD, Sig.Str., Sig.Str. %, Total Str., TD, TD %, Sub.Att, Rev., Ctrl
                
                # Red Fighter Stats
                stats['r_kd'] = clean_text(cols[1].find_all('p')[0].text)
                stats['r_sig_str'] = clean_text(cols[2].find_all('p')[0].text) # "10 of 20"
                stats['r_sig_str_pct'] = clean_text(cols[3].find_all('p')[0].text)
                stats['r_total_str'] = clean_text(cols[4].find_all('p')[0].text) # "15 of 25"
                stats['r_td'] = clean_text(cols[5].find_all('p')[0].text) # "1 of 3"
                stats['r_td_pct'] = clean_text(cols[6].find_all('p')[0].text)
                stats['r_sub_att'] = clean_text(cols[7].find_all('p')[0].text)
                stats['r_rev'] = clean_text(cols[8].find_all('p')[0].text)
                stats['r_ctrl'] = clean_text(cols[9].find_all('p')[0].text)
                
                # Blue Fighter Stats
                stats['b_kd'] = clean_text(cols[1].find_all('p')[1].text)
                stats['b_sig_str'] = clean_text(cols[2].find_all('p')[1].text)
                stats['b_sig_str_pct'] = clean_text(cols[3].find_all('p')[1].text)
                stats['b_total_str'] = clean_text(cols[4].find_all('p')[1].text)
                stats['b_td'] = clean_text(cols[5].find_all('p')[1].text)
                stats['b_td_pct'] = clean_text(cols[6].find_all('p')[1].text)
                stats['b_sub_att'] = clean_text(cols[7].find_all('p')[1].text)
                stats['b_rev'] = clean_text(cols[8].find_all('p')[1].text)
                stats['b_ctrl'] = clean_text(cols[9].find_all('p')[1].text)

    return stats

def scrape_fight_details(fight_url):
    """Scrape detailed stats for a single fight."""
    print(f"  Scraping fight: {fight_url}")
    try:
        response = requests.get(fight_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return parse_fight_stats(soup)
    except Exception as e:
        print(f"  Error scraping fight: {e}")
        return None

def process_stats(raw_stats):
    """Process raw stats into clean numeric values."""
    processed = {}
    
    for key, value in raw_stats.items():
        if key in ['method', 'round', 'time', 'format', 'referee']:
            processed[key] = value
            continue
            
        # Handle "X of Y" format (e.g. "10 of 20")
        if ' of ' in str(value):
            landed, attempted = value.split(' of ')
            processed[f"{key}_landed"] = int(landed)
            processed[f"{key}_attempted"] = int(attempted)
        # Handle percentages (e.g. "50%")
        elif '%' in str(value):
            processed[key] = int(value.replace('%', '')) / 100.0
        # Handle time (e.g. "3:00")
        elif ':' in str(value):
            mins, secs = value.split(':')
            processed[f"{key}_sec"] = int(mins) * 60 + int(secs)
        # Handle simple integers
        elif str(value).isdigit():
            processed[key] = int(value)
        # Handle "--"
        elif value == '--':
            processed[key] = 0
        else:
            processed[key] = value
            
    return processed

if __name__ == "__main__":
    print("🥊 UFC Data Scraper (ufcstats.com)")
    print("----------------------------------")
    
    # 1. Get Events
    latest_events = get_latest_events()
    print(f"\nFound {len(latest_events)} events.")
    
    # Filter events after March 23, 2024
    cutoff_date = datetime(2024, 3, 23)
    events_to_scrape = []
    
    print(f"Filtering for events after {cutoff_date.strftime('%B %d, %Y')}...")
    
    for event in latest_events:
        try:
            # Parse date string like "November 15, 2025"
            event_date = datetime.strptime(event['date'], "%B %d, %Y")
            if event_date > cutoff_date:
                events_to_scrape.append(event)
        except ValueError as e:
            print(f"⚠️ Could not parse date for {event['name']}: {event['date']}")
            
    print(f"Found {len(events_to_scrape)} new events to scrape.")
    
    all_fight_data = []
    
    for i, event in enumerate(events_to_scrape):
        print(f"\n[{i+1}/{len(events_to_scrape)}] Processing Event: {event['name']} ({event['date']})")
        
        # 2. Get Fights for Event
        fights = scrape_event_fights(event['link'])
        print(f"Found {len(fights)} fights.")
        
        for fight in fights:
            # 3. Get Details for Fight
            raw_stats = scrape_fight_details(fight['link'])
            
            if raw_stats:
                # 4. Process Stats
                clean_stats = process_stats(raw_stats)
                
                # Combine info
                fight_record = {
                    'event_name': event['name'],
                    'event_date': event['date'],
                    'location': event['location'],
                    'r_fighter': fight['r_fighter'],
                    'b_fighter': fight['b_fighter'],
                    'weight_class': fight['weight_class'],
                    **clean_stats
                }
                all_fight_data.append(fight_record)
            
            # Be nice to the server
            time.sleep(1)
            
    # 5. Save to CSV
    if all_fight_data:
        df = pd.DataFrame(all_fight_data)
        output_file = 'data/scraped_raw_data.csv'
        df.to_csv(output_file, index=False)
        print(f"\n✅ Scraped {len(df)} fights. Saved to {output_file}")
        print("Columns:", df.columns.tolist())
    else:
        print("\n❌ No data scraped.")
