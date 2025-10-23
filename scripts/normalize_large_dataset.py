import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
import sqlite3
from pathlib import Path

class UFCDataNormalizer:
    """
    Comprehensive data normalization for UFC large dataset.
    Handles both relational database normalization and feature scaling.
    """
    
    def __init__(self, csv_path='data/UFC dataset/Large set/large_dataset.csv'):
        self.csv_path = Path(csv_path)
        self.df = None
        self.scalers = {}
        self.encoders = {}
        
    def load_data(self):
        """Load the large dataset"""
        print("Loading large dataset...")
        self.df = pd.read_csv(self.csv_path)
        print(f"Loaded {len(self.df)} fights with {len(self.df.columns)} columns")
        print(f"Null values: {self.df.isnull().sum().sum()}")
        return self.df
    
    def handle_missing_values(self):
        """Handle missing values intelligently"""
        print("\nHandling missing values...")
        
        # For numeric columns, fill with median or 0 based on context
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if 'acc' in col.lower() or 'pct' in col.lower():
                # Accuracy/percentage: fill with median
                self.df[col].fillna(self.df[col].median(), inplace=True)
            elif '_diff' in col:
                # Differences: fill with 0 (no difference)
                self.df[col].fillna(0, inplace=True)
            elif 'ctrl_sec' in col or 'time_sec' in col:
                # Time: fill with median
                self.df[col].fillna(self.df[col].median(), inplace=True)
            else:
                # Other numeric: fill with median
                self.df[col].fillna(self.df[col].median(), inplace=True)
        
        # For categorical columns, fill with 'Unknown'
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            self.df[col].fillna('Unknown', inplace=True)
        
        print(f"Remaining null values: {self.df.isnull().sum().sum()}")
        
    def create_normalized_database(self, db_path='data/normalized_ufc.db'):
        """
        Create a properly normalized relational database.
        Follows 3NF (Third Normal Form).
        """
        print("\nCreating normalized database...")
        db_path = Path(db_path)
        conn = sqlite3.connect(db_path)
        
        # 1. Events table
        events_df = self.df[[
            'event_name', 'weight_class', 'is_title_bout', 
            'gender', 'referee', 'total_rounds'
        ]].drop_duplicates()
        events_df['event_id'] = range(1, len(events_df) + 1)
        events_df.to_sql('events', conn, if_exists='replace', index=False)
        
        # 2. Fighters table
        # Extract red corner fighters
        r_fighters = self.df[[
            'r_fighter', 'r_height', 'r_reach', 'r_stance'
        ]].rename(columns={
            'r_fighter': 'name',
            'r_height': 'height',
            'r_reach': 'reach',
            'r_stance': 'stance'
        })
        
        # Extract blue corner fighters
        b_fighters = self.df[[
            'b_fighter', 'b_height', 'b_reach', 'b_stance'
        ]].rename(columns={
            'b_fighter': 'name',
            'b_height': 'height',
            'b_reach': 'reach',
            'b_stance': 'stance'
        })
        
        # Combine and deduplicate
        fighters_df = pd.concat([r_fighters, b_fighters]).drop_duplicates(subset=['name'])
        fighters_df['fighter_id'] = range(1, len(fighters_df) + 1)
        fighters_df.to_sql('fighters', conn, if_exists='replace', index=False)
        
        # 3. Fights table
        fights_df = self.df.copy()
        fights_df['fight_id'] = range(1, len(fights_df) + 1)
        
        # Map to event_id
        event_map = events_df.set_index('event_name')['event_id'].to_dict()
        fights_df['event_id'] = fights_df['event_name'].map(event_map)
        
        # Map to fighter_ids
        fighter_map = fighters_df.set_index('name')['fighter_id'].to_dict()
        fights_df['r_fighter_id'] = fights_df['r_fighter'].map(fighter_map)
        fights_df['b_fighter_id'] = fights_df['b_fighter'].map(fighter_map)
        
        # Select relevant columns for fights table
        fights_columns = [
            'fight_id', 'event_id', 'r_fighter_id', 'b_fighter_id',
            'winner', 'method', 'finish_round', 'time_sec'
        ]
        fights_df[fights_columns].to_sql('fights', conn, if_exists='replace', index=False)
        
        # 4. Fight statistics table
        stats_columns = [col for col in self.df.columns if col not in fights_columns + 
                        ['event_name', 'r_fighter', 'b_fighter', 'weight_class', 
                         'is_title_bout', 'gender', 'referee', 'total_rounds',
                         'r_height', 'r_reach', 'r_stance', 'b_height', 'b_reach', 'b_stance']]
        
        fight_stats_df = self.df[['event_name', 'r_fighter', 'b_fighter'] + stats_columns].copy()
        fight_stats_df['fight_id'] = fights_df['fight_id']
        fight_stats_df = fight_stats_df[['fight_id'] + stats_columns]
        fight_stats_df.to_sql('fight_statistics', conn, if_exists='replace', index=False)
        
        conn.close()
        print(f"Normalized database created at: {db_path.absolute()}")
        print(f"Tables created: events, fighters, fights, fight_statistics")
        
    def scale_features(self):
        """
        Apply appropriate scaling to numerical features.
        Returns a new dataframe with scaled features.
        """
        print("\nScaling features...")
        scaled_df = self.df.copy()
        
        # Identify feature types
        percentage_cols = [col for col in scaled_df.columns if 
                          'acc' in col.lower() or 'def' in col.lower()]
        
        rate_cols = [col for col in scaled_df.columns if 
                    'slpm' in col.lower() or 'sapm' in col.lower() or 
                    'avg' in col.lower()]
        
        count_cols = [col for col in scaled_df.columns if 
                     any(x in col.lower() for x in ['_kd', '_str', '_td', '_sub', '_rev']) and
                     'acc' not in col.lower() and 'diff' not in col]
        
        physical_cols = ['r_height', 'r_weight', 'r_reach', 'r_age',
                        'b_height', 'b_weight', 'b_reach', 'b_age']
        
        diff_cols = [col for col in scaled_df.columns if '_diff' in col]
        
        # Apply Min-Max scaling to percentages (already 0-1 range)
        for col in percentage_cols:
            if col in scaled_df.columns:
                scaler = MinMaxScaler()
                scaled_df[f'{col}_scaled'] = scaler.fit_transform(scaled_df[[col]])
                self.scalers[col] = scaler
        
        # Apply Standard scaling to rates and counts
        for col in rate_cols + count_cols:
            if col in scaled_df.columns:
                scaler = StandardScaler()
                scaled_df[f'{col}_scaled'] = scaler.fit_transform(scaled_df[[col]])
                self.scalers[col] = scaler
        
        # Apply Standard scaling to physical attributes
        for col in physical_cols:
            if col in scaled_df.columns:
                scaler = StandardScaler()
                scaled_df[f'{col}_scaled'] = scaler.fit_transform(scaled_df[[col]])
                self.scalers[col] = scaler
        
        # Apply Standard scaling to difference columns
        for col in diff_cols:
            if col in scaled_df.columns:
                scaler = StandardScaler()
                scaled_df[f'{col}_scaled'] = scaler.fit_transform(scaled_df[[col]])
                self.scalers[col] = scaler
        
        print(f"Scaled {len(self.scalers)} features")
        return scaled_df
    
    def encode_categorical(self):
        """Encode categorical variables"""
        print("\nEncoding categorical variables...")
        encoded_df = self.df.copy()
        
        categorical_cols = ['stance', 'winner', 'method', 'gender', 'weight_class']
        
        for col in categorical_cols:
            # Check both r_ and b_ versions
            for prefix in ['r_', 'b_', '']:
                full_col = f'{prefix}{col}' if prefix else col
                if full_col in encoded_df.columns:
                    encoder = LabelEncoder()
                    encoded_df[f'{full_col}_encoded'] = encoder.fit_transform(
                        encoded_df[full_col].astype(str)
                    )
                    self.encoders[full_col] = encoder
        
        print(f"Encoded {len(self.encoders)} categorical features")
        return encoded_df
    
    def create_feature_engineered_dataset(self):
        """
        Create additional engineered features for ML.
        """
        print("\nEngineering new features...")
        feat_df = self.df.copy()
        
        # Win rates (if we have historical data)
        feat_df['r_win_rate'] = feat_df['r_wins_total'] / (
            feat_df['r_wins_total'] + feat_df['r_losses_total']
        )
        feat_df['b_win_rate'] = feat_df['b_wins_total'] / (
            feat_df['b_wins_total'] + feat_df['b_losses_total']
        )
        feat_df['win_rate_diff'] = feat_df['r_win_rate'] - feat_df['b_win_rate']
        
        # Experience differential
        feat_df['r_total_fights'] = feat_df['r_wins_total'] + feat_df['r_losses_total']
        feat_df['b_total_fights'] = feat_df['b_wins_total'] + feat_df['b_losses_total']
        feat_df['experience_diff'] = feat_df['r_total_fights'] - feat_df['b_total_fights']
        
        # Physical advantages
        feat_df['r_bmi'] = feat_df['r_weight'] / ((feat_df['r_height']/100) ** 2)
        feat_df['b_bmi'] = feat_df['b_weight'] / ((feat_df['b_height']/100) ** 2)
        feat_df['bmi_diff'] = feat_df['r_bmi'] - feat_df['b_bmi']
        
        # Striking efficiency
        feat_df['r_striking_efficiency'] = feat_df['r_SLpM_total'] * feat_df['r_sig_str_acc_total']
        feat_df['b_striking_efficiency'] = feat_df['b_SLpM_total'] * feat_df['b_sig_str_acc_total']
        feat_df['striking_efficiency_diff'] = feat_df['r_striking_efficiency'] - feat_df['b_striking_efficiency']
        
        # Grappling efficiency
        feat_df['r_grappling_efficiency'] = feat_df['r_td_avg'] * feat_df['r_td_acc_total']
        feat_df['b_grappling_efficiency'] = feat_df['b_td_avg'] * feat_df['b_td_acc_total']
        feat_df['grappling_efficiency_diff'] = feat_df['r_grappling_efficiency'] - feat_df['b_grappling_efficiency']
        
        # Defensive rating
        feat_df['r_defensive_rating'] = (feat_df['r_str_def_total'] + feat_df['r_td_def_total']) / 2
        feat_df['b_defensive_rating'] = (feat_df['b_str_def_total'] + feat_df['b_td_def_total']) / 2
        feat_df['defensive_rating_diff'] = feat_df['r_defensive_rating'] - feat_df['b_defensive_rating']
        
        print(f"Created {len(feat_df.columns) - len(self.df.columns)} new features")
        return feat_df
    
    def save_normalized_csv(self, output_path='data/normalized_large_dataset.csv'):
        """Save fully normalized and processed dataset"""
        print(f"\nSaving normalized dataset to {output_path}...")
        
        # Combine all transformations
        processed_df = self.create_feature_engineered_dataset()
        processed_df = self.encode_categorical()
        
        processed_df.to_csv(output_path, index=False)
        print(f"Saved {len(processed_df)} rows with {len(processed_df.columns)} columns")
    
    def generate_normalization_report(self):
        """Generate a report of normalization steps"""
        report = {
            'original_shape': self.df.shape,
            'null_values_handled': self.df.isnull().sum().sum(),
            'scalers_applied': len(self.scalers),
            'encoders_applied': len(self.encoders),
            'data_types': self.df.dtypes.value_counts().to_dict()
        }
        return report

def main():
    # Initialize normalizer
    normalizer = UFCDataNormalizer()
    
    # Step 1: Load data
    normalizer.load_data()
    
    # Step 2: Handle missing values
    normalizer.handle_missing_values()
    
    # Step 3: Create normalized database
    normalizer.create_normalized_database()
    
    # Step 4: Create feature-engineered dataset
    normalized_df = normalizer.create_feature_engineered_dataset()
    
    # Step 5: Encode categorical variables
    encoded_df = normalizer.encode_categorical()
    
    # Step 6: Scale features
    scaled_df = normalizer.scale_features()
    
    # Step 7: Save processed data
    normalizer.save_normalized_csv()
    
    # Step 8: Generate report
    report = normalizer.generate_normalization_report()
    print("\n" + "="*50)
    print("NORMALIZATION COMPLETE")
    print("="*50)
    print(f"Original shape: {report['original_shape']}")
    print(f"Null values handled: {report['null_values_handled']}")
    print(f"Scalers applied: {report['scalers_applied']}")
    print(f"Encoders applied: {report['encoders_applied']}")
    print("\nOutputs created:")
    print("  - data/normalized_ufc.db (relational database)")
    print("  - data/normalized_large_dataset.csv (processed CSV)")

if __name__ == '__main__':
    main()