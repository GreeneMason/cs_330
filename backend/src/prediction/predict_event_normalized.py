"""
UFC Fight Prediction using Event-Normalized Data
Simple script to predict fight outcomes with event lookup
"""

import pandas as pd
import numpy as np
import sqlite3
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class EventNormalizedPredictor:
    """Predictor using event-normalized dataset with event lookup"""
    
    def __init__(self):
        # Use project root directories
        self.model_dir = Path(__file__).parent.parent.parent.parent / 'models' / 'ensemble'
        self.data_dir = Path(__file__).parent.parent.parent.parent / 'data'
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_columns = None
        self.db_path = self.data_dir / 'event_normalized_data.db'
        
    def load_model(self):
        """Load the trained model and preprocessing components"""
        try:
            # Try event-normalized model first
            model_path = self.model_dir / 'event_normalized_best_model.pkl'
            if model_path.exists():
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(self.model_dir / 'event_normalized_scaler.pkl')
                self.label_encoder = joblib.load(self.model_dir / 'event_normalized_label_encoder.pkl')
                self.feature_columns = joblib.load(self.model_dir / 'event_normalized_features.pkl')
                print("✓ Loaded event-normalized model")
                return True
            else:
                # Fallback to original model
                model_path = self.model_dir / 'best_model.pkl'
                if model_path.exists():
                    self.model = joblib.load(model_path)
                    self.scaler = joblib.load(self.model_dir / 'scaler.pkl')
                    self.label_encoder = joblib.load(self.model_dir / 'label_encoder.pkl')
                    self.feature_columns = joblib.load(self.model_dir / 'features.pkl')
                    print("✓ Loaded original model (no event normalization)")
                    return True
                else:
                    print("❌ No trained model found. Please run training first.")
                    return False
                    
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def search_events(self, search_term=""):
        """Search for UFC events by name"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            if search_term:
                query = """
                SELECT event_id, event_name, 
                       (SELECT COUNT(*) FROM fights WHERE event_id = e.event_id) as fight_count
                FROM events e
                WHERE event_name LIKE ?
                ORDER BY event_name
                """
                events = pd.read_sql_query(query, conn, params=[f'%{search_term}%'])
            else:
                query = """
                SELECT event_id, event_name, 
                       (SELECT COUNT(*) FROM fights WHERE event_id = e.event_id) as fight_count
                FROM events e
                ORDER BY event_name
                LIMIT 20
                """
                events = pd.read_sql_query(query, conn)
            
            conn.close()
            return events
            
        except Exception as e:
            print(f"❌ Error searching events: {e}")
            # Fallback to CSV if database not available
            try:
                events_df = pd.read_csv(self.data_dir / 'events_reference.csv')
                if search_term:
                    mask = events_df['event_name'].str.contains(search_term, case=False, na=False)
                    return events_df[mask].head(20)
                else:
                    return events_df.head(20)
            except:
                return pd.DataFrame()
    
    def get_event_fights(self, event_id):
        """Get all fights from a specific event"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = """
            SELECT f.r_fighter, f.b_fighter, f.winner, f.weight_class, 
                   f.method, f.finish_round, e.event_name
            FROM fights f
            JOIN events e ON f.event_id = e.event_id
            WHERE f.event_id = ?
            ORDER BY f.r_fighter
            """
            
            fights = pd.read_sql_query(query, conn, params=[event_id])
            conn.close()
            return fights
            
        except Exception as e:
            print(f"❌ Error getting event fights: {e}")
            return pd.DataFrame()
    
    def predict_fight_interactive(self):
        """Interactive prediction interface"""
        print("\n🥊 UFC FIGHT PREDICTOR (Event-Normalized)")
        print("=" * 50)
        
        if not self.load_model():
            return
        
        while True:
            print("\nChoose prediction method:")
            print("1. Search existing fights by event")
            print("2. Manual fighter stat entry")
            print("3. Quick prediction (simplified)")
            print("4. Browse events")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.predict_from_event()
            elif choice == '2':
                self.predict_manual_entry()
            elif choice == '3':
                self.predict_quick()
            elif choice == '4':
                self.browse_events()
            elif choice == '5':
                print("Thanks for using UFC Fight Predictor!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def browse_events(self):
        """Browse available events"""
        print("\n📅 BROWSE UFC EVENTS")
        print("=" * 30)
        
        search_term = input("Enter event search term (or press Enter for recent events): ").strip()
        
        events = self.search_events(search_term)
        
        if events.empty:
            print("No events found.")
            return
        
        print(f"\nFound {len(events)} events:")
        for i, row in events.iterrows():
            print(f"{row['event_id']:3d}: {row['event_name']} ({row.get('fight_count', '?')} fights)")
        
        while True:
            event_input = input("\nEnter event ID to view fights (or press Enter to return): ").strip()
            if not event_input:
                break
                
            try:
                event_id = int(event_input)
                fights = self.get_event_fights(event_id)
                
                if fights.empty:
                    print("No fights found for this event.")
                    continue
                
                event_name = fights.iloc[0]['event_name'] if not fights.empty else "Unknown Event"
                print(f"\n🏟️  {event_name}")
                print("=" * len(event_name))
                
                for i, fight in fights.iterrows():
                    winner_symbol = "🔴" if fight['winner'] == 'Red' else "🔵"
                    print(f"{fight['r_fighter']:20} vs {fight['b_fighter']:20} | Winner: {winner_symbol} {fight['winner']:4} | {fight['method']}")
                    
            except ValueError:
                print("Please enter a valid event ID.")
    
    def predict_from_event(self):
        """Predict fights from existing event data"""
        print("\n🔍 SEARCH FIGHTS BY EVENT")
        print("=" * 30)
        
        search_term = input("Enter event name to search: ").strip()
        
        events = self.search_events(search_term)
        
        if events.empty:
            print("No events found matching your search.")
            return
        
        print(f"\nFound {len(events)} matching events:")
        for i, row in events.iterrows():
            print(f"{row['event_id']:3d}: {row['event_name']}")
        
        try:
            event_id = int(input("\nEnter event ID: "))
            fights = self.get_event_fights(event_id)
            
            if fights.empty:
                print("No fights found for this event.")
                return
            
            print(f"\nFights from {fights.iloc[0]['event_name']}:")
            for i, fight in fights.iterrows():
                print(f"{i+1:2d}. {fight['r_fighter']} vs {fight['b_fighter']} ({fight['weight_class']})")
            
            fight_num = int(input("\nEnter fight number to analyze: ")) - 1
            
            if 0 <= fight_num < len(fights):
                selected_fight = fights.iloc[fight_num]
                print(f"\n📊 ANALYZING: {selected_fight['r_fighter']} vs {selected_fight['b_fighter']}")
                print(f"Actual winner: {selected_fight['winner']} corner ({selected_fight['method']})")
                
                # Here you would load the actual fight data and make prediction
                # For now, just show the historical result
                print("Note: This would show model prediction vs actual result")
            else:
                print("Invalid fight number.")
                
        except (ValueError, IndexError):
            print("Please enter a valid event ID and fight number.")
    
    def predict_manual_entry(self):
        """Manual prediction with user-entered stats"""
        print("\n✋ MANUAL FIGHTER STATS ENTRY")
        print("=" * 35)
        print("Enter basic stats for both fighters (or press Enter for defaults)")
        
        # Get fighter names
        r_fighter = input("Red fighter name: ").strip() or "Red Fighter"
        b_fighter = input("Blue fighter name: ").strip() or "Blue Fighter"
        
        # Simplified stat collection
        stats = {}
        simple_features = [
            ('r_wins_total', 'Red fighter wins', 15),
            ('r_losses_total', 'Red fighter losses', 5),
            ('r_age', 'Red fighter age', 28),
            ('b_wins_total', 'Blue fighter wins', 12),
            ('b_losses_total', 'Blue fighter losses', 8),
            ('b_age', 'Blue fighter age', 30),
        ]
        
        for feature, prompt, default in simple_features:
            try:
                value = input(f"{prompt} (default {default}): ").strip()
                stats[feature] = float(value) if value else default
            except:
                stats[feature] = default
        
        # Calculate some derived features
        stats['wins_total_diff'] = stats['r_wins_total'] - stats['b_wins_total']
        stats['losses_total_diff'] = stats['r_losses_total'] - stats['b_losses_total']
        stats['age_diff'] = stats['r_age'] - stats['b_age']
        
        # Fill missing features with defaults
        for feature in self.feature_columns:
            if feature not in stats:
                stats[feature] = 0.0
        
        # Make prediction
        try:
            feature_vector = np.array([stats[f] for f in self.feature_columns]).reshape(1, -1)
            
            if hasattr(self, 'scaler') and self.scaler:
                feature_vector = self.scaler.transform(feature_vector)
            
            prediction = self.model.predict(feature_vector)[0]
            probabilities = self.model.predict_proba(feature_vector)[0]
            
            predicted_winner = self.label_encoder.inverse_transform([prediction])[0]
            
            print(f"\n🥊 PREDICTION RESULTS")
            print("=" * 25)
            print(f"Fight: {r_fighter} vs {b_fighter}")
            print(f"Predicted Winner: {predicted_winner} corner")
            
            for i, class_name in enumerate(self.label_encoder.classes_):
                prob = probabilities[i] * 100
                print(f"{class_name}: {prob:.1f}%")
            
        except Exception as e:
            print(f"❌ Error making prediction: {e}")
    
    def predict_quick(self):
        """Quick prediction with minimal input"""
        print("\n⚡ QUICK PREDICTION")
        print("=" * 20)
        
        r_fighter = input("Red fighter name: ").strip()
        b_fighter = input("Blue fighter name: ").strip()
        
        if not r_fighter or not b_fighter:
            print("Both fighter names are required.")
            return
        
        # Use average stats for quick prediction
        default_stats = {f: 0.0 for f in self.feature_columns}
        
        # Set some reasonable defaults for key features
        defaults = {
            'r_wins_total': 15, 'b_wins_total': 12,
            'r_losses_total': 5, 'b_losses_total': 8,
            'r_age': 28, 'b_age': 30,
            'wins_total_diff': 3, 'losses_total_diff': -3,
            'age_diff': -2
        }
        
        for feature, value in defaults.items():
            if feature in default_stats:
                default_stats[feature] = value
        
        try:
            feature_vector = np.array([default_stats[f] for f in self.feature_columns]).reshape(1, -1)
            
            if hasattr(self, 'scaler') and self.scaler:
                feature_vector = self.scaler.transform(feature_vector)
            
            prediction = self.model.predict(feature_vector)[0]
            probabilities = self.model.predict_proba(feature_vector)[0]
            
            predicted_winner = self.label_encoder.inverse_transform([prediction])[0]
            
            print(f"\n🥊 QUICK PREDICTION")
            print("=" * 20)
            print(f"Fight: {r_fighter} vs {b_fighter}")
            print(f"Predicted Winner: {predicted_winner} corner")
            
            for i, class_name in enumerate(self.label_encoder.classes_):
                prob = probabilities[i] * 100
                print(f"{class_name}: {prob:.1f}%")
                
            print("\nNote: This is a quick prediction using average stats.")
            print("For better accuracy, use manual entry with actual fighter stats.")
            
        except Exception as e:
            print(f"❌ Error making prediction: {e}")
    
    def predict_dict(self, fight_data):
        """Predict from a dictionary of features"""
        if self.model is None:
            if not self.load_model():
                return None
        
        try:
            # Convert dict to DataFrame
            df = pd.DataFrame([fight_data])
            
            # Ensure all features are present
            for col in self.feature_columns:
                if col not in df.columns:
                    df[col] = 0
            
            # Select features in correct order
            X = df[self.feature_columns]
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Predict
            prob = self.model.predict_proba(X_scaled)[0][1]
            prediction = "Red" if prob > 0.5 else "Blue"
            confidence = max(prob, 1 - prob)
            
            return {
                'prediction': prediction,
                'probability': float(prob),
                'confidence': float(confidence),
                'winner': prediction
            }
            
        except Exception as e:
            print(f"❌ Error predicting from dict: {e}")
            return None


def main():
    """Main function"""
    predictor = EventNormalizedPredictor()
    predictor.predict_fight_interactive()


if __name__ == "__main__":
    main()