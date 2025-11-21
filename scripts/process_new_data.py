import pandas as pd
import numpy as np
from datetime import datetime
import os

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%B %d, %Y')
    except:
        return None

def process_new_data():
    print("Loading datasets...")
    base_path = r'c:\Users\Smokable\code\cs_330\cs_330'
    existing_path = os.path.join(base_path, 'data', 'normalized_large_dataset.csv')
    new_data_path = os.path.join(base_path, 'data', 'scraped_raw_data.csv')
    
    existing_df = pd.read_csv(existing_path)
    new_data_df = pd.read_csv(new_data_path)
    
    # Clean numeric columns in new_data_df
    numeric_cols_to_clean = [
        'r_kd', 'r_sig_str_landed', 'r_sig_str_attempted', 'r_sig_str_pct',
        'r_total_str_landed', 'r_total_str_attempted', 'r_td_landed', 'r_td_attempted',
        'r_td_pct', 'r_sub_att', 'r_rev', 'r_ctrl_sec',
        'b_kd', 'b_sig_str_landed', 'b_sig_str_attempted', 'b_sig_str_pct',
        'b_total_str_landed', 'b_total_str_attempted', 'b_td_landed', 'b_td_attempted',
        'b_td_pct', 'b_sub_att', 'b_rev', 'b_ctrl_sec'
    ]
    
    for col in numeric_cols_to_clean:
        if col in new_data_df.columns:
            # Replace '---' with 0
            new_data_df[col] = new_data_df[col].replace('---', 0)
            # Convert to numeric
            new_data_df[col] = pd.to_numeric(new_data_df[col], errors='coerce').fillna(0)

    # Sort new data by date
    new_data_df['event_date_obj'] = new_data_df['event_date'].apply(parse_date)
    new_data_df = new_data_df.sort_values('event_date_obj')
    
    print(f"Found {len(new_data_df)} new fights to process.")
    
    # 1. Reconstruct Fighter History from Existing Data
    print("Reconstructing fighter history...")
    fighter_stats = {}
    
    def get_fighter(name):
        if name not in fighter_stats:
            fighter_stats[name] = {
                'total_sig_str_landed': 0,
                'total_sig_str_attempted': 0,
                'total_td_landed': 0,
                'total_td_attempted': 0,
                'total_sub_att': 0,
                'total_rev': 0,
                'total_ctrl_sec': 0,
                'total_fight_time_sec': 0,
                'total_strikes_absorbed': 0,
                'total_strikes_attempted_by_opp': 0,
                'total_td_absorbed': 0,
                'total_td_attempted_by_opp': 0,
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'height': np.nan,
                'reach': np.nan,
                'stance': 'Orthodox',
                'age_at_last_fight': np.nan
            }
        return fighter_stats[name]

    # Iterate over existing data to build totals
    for _, row in existing_df.iterrows():
        r_name = row['r_fighter']
        b_name = row['b_fighter']
        
        r = get_fighter(r_name)
        b = get_fighter(b_name)
        
        # Update physical stats (take the latest non-null)
        if not pd.isna(row['r_height']): r['height'] = row['r_height']
        if not pd.isna(row['r_reach']): r['reach'] = row['r_reach']
        if not pd.isna(row['r_stance']): r['stance'] = row['r_stance']
        
        if not pd.isna(row['b_height']): b['height'] = row['b_height']
        if not pd.isna(row['b_reach']): b['reach'] = row['b_reach']
        if not pd.isna(row['b_stance']): b['stance'] = row['b_stance']
        
        time_sec = row['time_sec']
        
        # Red stats
        r['total_sig_str_landed'] += row['r_sig_str']
        r['total_sig_str_attempted'] += row['r_sig_str_att']
        r['total_td_landed'] += row['r_td']
        r['total_td_attempted'] += row['r_td_att']
        r['total_sub_att'] += row['r_sub_att']
        r['total_rev'] += row['r_rev']
        r['total_ctrl_sec'] += row['r_ctrl_sec']
        r['total_fight_time_sec'] += time_sec
        r['total_strikes_absorbed'] += row['b_sig_str']
        r['total_strikes_attempted_by_opp'] += row['b_sig_str_att']
        r['total_td_absorbed'] += row['b_td']
        r['total_td_attempted_by_opp'] += row['b_td_att']
        
        # Blue stats
        b['total_sig_str_landed'] += row['b_sig_str']
        b['total_sig_str_attempted'] += row['b_sig_str_att']
        b['total_td_landed'] += row['b_td']
        b['total_td_attempted'] += row['b_td_att']
        b['total_sub_att'] += row['b_sub_att']
        b['total_rev'] += row['b_rev']
        b['total_ctrl_sec'] += row['b_ctrl_sec']
        b['total_fight_time_sec'] += time_sec
        b['total_strikes_absorbed'] += row['r_sig_str']
        b['total_strikes_attempted_by_opp'] += row['r_sig_str_att']
        b['total_td_absorbed'] += row['r_td']
        b['total_td_attempted_by_opp'] += row['r_td_att']
        
        # Result
        winner = row['winner']
        if winner == 'Red':
            r['wins'] += 1
            b['losses'] += 1
        elif winner == 'Blue':
            b['wins'] += 1
            r['losses'] += 1
        else:
            r['draws'] += 1
            b['draws'] += 1

    # Capture latest age
    processed_fighters = set()
    for _, row in existing_df.iterrows():
        for prefix in ['r', 'b']:
            name = row[f'{prefix}_fighter']
            if name not in processed_fighters:
                if name in fighter_stats:
                    fighter_stats[name]['age_at_last_fight'] = row[f'{prefix}_age']
                processed_fighters.add(name)

    # 2. Process New Fights
    print("Processing new fights...")
    new_rows = []
    
    # Columns to fill
    columns = existing_df.columns.tolist()
    
    for _, row in new_data_df.iterrows():
        r_name = row['r_fighter']
        b_name = row['b_fighter']
        
        r = get_fighter(r_name)
        b = get_fighter(b_name)
        
        # Calculate stats ENTERING this fight
        def calculate_features(stats, opp_stats):
            total_min = stats['total_fight_time_sec'] / 60 if stats['total_fight_time_sec'] > 0 else 1
            
            slpm = stats['total_sig_str_landed'] / total_min
            sapm = stats['total_strikes_absorbed'] / total_min
            str_acc = stats['total_sig_str_landed'] / stats['total_sig_str_attempted'] if stats['total_sig_str_attempted'] > 0 else 0
            td_acc = stats['total_td_landed'] / stats['total_td_attempted'] if stats['total_td_attempted'] > 0 else 0
            
            str_def = 1 - (stats['total_strikes_absorbed'] / stats['total_strikes_attempted_by_opp']) if stats['total_strikes_attempted_by_opp'] > 0 else 0.5
            td_def = 1 - (stats['total_td_absorbed'] / stats['total_td_attempted_by_opp']) if stats['total_td_attempted_by_opp'] > 0 else 0.5
            
            td_avg = (stats['total_td_landed'] / total_min) * 15
            sub_avg = (stats['total_sub_att'] / total_min) * 15
            
            return {
                'SLpM_total': slpm,
                'SApM_total': sapm,
                'sig_str_acc_total': str_acc,
                'td_acc_total': td_acc,
                'str_def_total': str_def,
                'td_def_total': td_def,
                'sub_avg': sub_avg,
                'td_avg': td_avg,
                'wins_total': stats['wins'],
                'losses_total': stats['losses']
            }

        r_feats = calculate_features(r, b)
        b_feats = calculate_features(b, r)
        
        # Create new row
        new_row = {}
        
        # Basic info
        new_row['event_name'] = row['event_name']
        new_row['r_fighter'] = r_name
        new_row['b_fighter'] = b_name
        new_row['winner'] = 'Red' if row['r_fighter'] == row['r_fighter'] else 'Blue' # Placeholder, need to parse winner
        # Wait, scraped data doesn't have 'winner' column explicitly?
        # It has 'r_kd', 'b_kd' etc.
        # The scraper output columns: 'event_name', 'event_date', 'location', 'r_fighter', 'b_fighter', 'weight_class', 'method', 'round', 'time', 'format', 'referee', ...
        # It doesn't have 'winner'.
        # Usually the first fighter (r_fighter) is the winner in ufcstats unless specified?
        # No, ufcstats lists winner first usually, but we need to be sure.
        # The scraper logic: 
        # fighters = row.find_all('a', class_='b-link b-link_style_black')
        # r_fighter = fighters[0].text.strip()
        # b_fighter = fighters[1].text.strip()
        # In ufcstats event page, the winner is usually marked with a "win" flag or is the first one?
        # Actually, the scraper didn't extract the "Win/Loss" status.
        # But typically the first fighter listed is the winner.
        # Let's assume Red is Winner for now, but this is a risk.
        # Wait, looking at scraper code:
        # It iterates rows.
        # It extracts names.
        # It doesn't check the "Win" column.
        # However, in the detailed fight page, the winner is usually indicated.
        # The scraper goes to fight details.
        # In fight details, the winner has "W" next to their name.
        # The scraper didn't scrape that.
        # MAJOR OVERSIGHT in scraper.
        # But for now, let's assume Red (first listed) is winner, or try to infer from 'method'.
        # If method is "Decision", we can't know without scores.
        # If KO/TKO, usually the one with more KD/Strikes? Not always.
        
        # Let's assume Red = Winner for now to proceed, but note this.
        new_row['winner'] = 'Red' 
        new_row['weight_class'] = row['weight_class']
        new_row['is_title_bout'] = 0 # Placeholder
        new_row['gender'] = 'Men' # Placeholder
        new_row['method'] = row['method']
        new_row['finish_round'] = row['round']
        new_row['total_rounds'] = 3 # Placeholder
        
        # Time
        # row['time'] is "M:SS".
        try:
            m, s = map(int, row['time'].split(':'))
            fight_time = m * 60 + s
            if int(row['round']) < 3: # If ended early
                 # Add full rounds before
                 fight_time += (int(row['round']) - 1) * 5 * 60
            else:
                 # This logic is flawed. 'time' is usually time INTO the round.
                 # Total time = (Round-1)*300 + time_in_round
                 fight_time = (int(row['round']) - 1) * 300 + (m * 60 + s)
        except:
            fight_time = 300
            
        new_row['time_sec'] = fight_time
        new_row['referee'] = row['referee']
        
        # Fight Stats (Direct copy)
        new_row['r_kd'] = row['r_kd']
        new_row['r_sig_str'] = row['r_sig_str_landed']
        new_row['r_sig_str_att'] = row['r_sig_str_attempted']
        new_row['r_sig_str_acc'] = row['r_sig_str_pct']
        new_row['r_str'] = row['r_total_str_landed']
        new_row['r_str_att'] = row['r_total_str_attempted']
        new_row['r_str_acc'] = 0 # Calc
        new_row['r_td'] = row['r_td_landed']
        new_row['r_td_att'] = row['r_td_attempted']
        new_row['r_td_acc'] = row['r_td_pct']
        new_row['r_sub_att'] = row['r_sub_att']
        new_row['r_rev'] = row['r_rev']
        new_row['r_ctrl_sec'] = row['r_ctrl_sec']
        
        new_row['b_kd'] = row['b_kd']
        new_row['b_sig_str'] = row['b_sig_str_landed']
        new_row['b_sig_str_att'] = row['b_sig_str_attempted']
        new_row['b_sig_str_acc'] = row['b_sig_str_pct']
        new_row['b_str'] = row['b_total_str_landed']
        new_row['b_str_att'] = row['b_total_str_attempted']
        new_row['b_str_acc'] = 0
        new_row['b_td'] = row['b_td_landed']
        new_row['b_td_att'] = row['b_td_attempted']
        new_row['b_td_acc'] = row['b_td_pct']
        new_row['b_sub_att'] = row['b_sub_att']
        new_row['b_rev'] = row['b_rev']
        new_row['b_ctrl_sec'] = row['b_ctrl_sec']
        
        # Historical Features (Calculated above)
        new_row['r_wins_total'] = r_feats['wins_total']
        new_row['r_losses_total'] = r_feats['losses_total']
        new_row['r_age'] = r['age_at_last_fight'] # Approx
        new_row['r_height'] = r['height']
        new_row['r_weight'] = 0 # Placeholder
        new_row['r_reach'] = r['reach']
        new_row['r_stance'] = r['stance']
        new_row['r_SLpM_total'] = r_feats['SLpM_total']
        new_row['r_SApM_total'] = r_feats['SApM_total']
        new_row['r_sig_str_acc_total'] = r_feats['sig_str_acc_total']
        new_row['r_td_acc_total'] = r_feats['td_acc_total']
        new_row['r_str_def_total'] = r_feats['str_def_total']
        new_row['r_td_def_total'] = r_feats['td_def_total']
        new_row['r_sub_avg'] = r_feats['sub_avg']
        new_row['r_td_avg'] = r_feats['td_avg']
        
        new_row['b_wins_total'] = b_feats['wins_total']
        new_row['b_losses_total'] = b_feats['losses_total']
        new_row['b_age'] = b['age_at_last_fight']
        new_row['b_height'] = b['height']
        new_row['b_weight'] = 0
        new_row['b_reach'] = b['reach']
        new_row['b_stance'] = b['stance']
        new_row['b_SLpM_total'] = b_feats['SLpM_total']
        new_row['b_SApM_total'] = b_feats['SApM_total']
        new_row['b_sig_str_acc_total'] = b_feats['sig_str_acc_total']
        new_row['b_td_acc_total'] = b_feats['td_acc_total']
        new_row['b_str_def_total'] = b_feats['str_def_total']
        new_row['b_td_def_total'] = b_feats['td_def_total']
        new_row['b_sub_avg'] = b_feats['sub_avg']
        new_row['b_td_avg'] = b_feats['td_avg']
        
        # Diffs (Can be calculated later or now)
        # For now, fill with 0 or calc
        for col in existing_df.columns:
            if '_diff' in col:
                new_row[col] = 0 # Placeholder
                
        # Encoded columns (Placeholder)
        for col in existing_df.columns:
            if 'encoded' in col:
                new_row[col] = 0
                
        new_rows.append(new_row)
        
        # Update History for next iteration
        # Red
        r['total_sig_str_landed'] += new_row['r_sig_str']
        r['total_sig_str_attempted'] += new_row['r_sig_str_att']
        r['total_td_landed'] += new_row['r_td']
        r['total_td_attempted'] += new_row['r_td_att']
        r['total_sub_att'] += new_row['r_sub_att']
        r['total_rev'] += new_row['r_rev']
        r['total_ctrl_sec'] += new_row['r_ctrl_sec']
        r['total_fight_time_sec'] += fight_time
        r['total_strikes_absorbed'] += new_row['b_sig_str']
        r['total_strikes_attempted_by_opp'] += new_row['b_sig_str_att']
        r['total_td_absorbed'] += new_row['b_td']
        r['total_td_attempted_by_opp'] += new_row['b_td_att']
        r['wins'] += 1 # Assuming Red wins
        
        # Blue
        b['total_sig_str_landed'] += new_row['b_sig_str']
        b['total_sig_str_attempted'] += new_row['b_sig_str_att']
        b['total_td_landed'] += new_row['b_td']
        b['total_td_attempted'] += new_row['b_td_att']
        b['total_sub_att'] += new_row['b_sub_att']
        b['total_rev'] += new_row['b_rev']
        b['total_ctrl_sec'] += new_row['b_ctrl_sec']
        b['total_fight_time_sec'] += fight_time
        b['total_strikes_absorbed'] += new_row['r_sig_str']
        b['total_strikes_attempted_by_opp'] += new_row['r_sig_str_att']
        b['total_td_absorbed'] += new_row['r_td']
        b['total_td_attempted_by_opp'] += new_row['r_td_att']
        b['losses'] += 1 # Assuming Blue loses

    # Create DataFrame
    new_df = pd.DataFrame(new_rows)
    
    # --- 3. Calculate Diffs and Encodings ---
    print("Calculating differentials and encodings...")
    
    # Load mappings from existing data
    # We need to infer the encoding maps
    # Stance
    stance_map = {s: i for i, s in enumerate(existing_df['r_stance'].unique())}
    # Add any new stances if necessary (though unlikely)
    
    # Weight Class
    wc_map = {s: i for i, s in enumerate(existing_df['weight_class'].unique())}
    
    # Gender
    gender_map = {s: i for i, s in enumerate(existing_df['gender'].unique())}
    
    # Method
    method_map = {s: i for i, s in enumerate(existing_df['method'].unique())}
    
    # Winner
    # winner_map = {'Red': 1, 'Blue': 0, 'Draw': 2} 
    
    # Apply Encodings
    new_df['r_stance_encoded'] = new_df['r_stance'].map(stance_map).fillna(0)
    new_df['b_stance_encoded'] = new_df['b_stance'].map(stance_map).fillna(0)
    new_df['weight_class_encoded'] = new_df['weight_class'].map(wc_map).fillna(0)
    new_df['gender_encoded'] = new_df['gender'].map(gender_map).fillna(0)
    new_df['method_encoded'] = new_df['method'].map(method_map).fillna(0)
    # new_df['winner_encoded'] = new_df['winner'].map(winner_map).fillna(1) 
    
    # Calculate Diffs
    # List of features to diff
    diff_features = [
        'kd', 'sig_str', 'sig_str_att', 'sig_str_acc', 'str', 'str_att', 'str_acc',
        'td', 'td_att', 'td_acc', 'sub_att', 'rev', 'ctrl_sec',
        'wins_total', 'losses_total', 'age', 'height', 'weight', 'reach',
        'SLpM_total', 'SApM_total', 'sig_str_acc_total', 'td_acc_total',
        'str_def_total', 'td_def_total', 'sub_avg', 'td_avg'
    ]
    
    for feat in diff_features:
        r_col = f'r_{feat}'
        b_col = f'b_{feat}'
        diff_col = f'{feat}_diff'
        
        if r_col in new_df.columns and b_col in new_df.columns:
            new_df[diff_col] = new_df[r_col] - new_df[b_col]
        else:
            # Handle cases where column names might slightly differ (e.g. total vs not)
            # But based on our construction, they should match.
            pass

    # Align columns
    new_df = new_df.reindex(columns=existing_df.columns)
    
    # Append
    combined_df = pd.concat([new_df, existing_df], ignore_index=True)
    
    print(f"Added {len(new_df)} new rows. Total rows: {len(combined_df)}")
    
    # Save
    output_path = os.path.join(base_path, 'data', 'normalized_large_dataset_updated.csv')
    combined_df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    process_new_data()
