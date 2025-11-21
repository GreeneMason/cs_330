"""
UFC Fight Prediction using Neural Network with Event-Normalized Data
Fighter-aware neural network with same interface as existing models
"""

import pandas as pd
import numpy as np
import tensorflow as tf
import sqlite3
import joblib
from pathlib import Path
import warnings
import json
warnings.filterwarnings('ignore')

class EventNormalizedNeuralNetworkPredictor:
    """Neural network predictor using event-normalized dataset with event lookup"""
    
    def __init__(self):
        # Use project root directories
        self.model_dir = Path(__file__).parent.parent.parent.parent / 'models' / 'neural_network'
        self.data_dir = Path(__file__).parent.parent.parent.parent / 'data'
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_columns = None
        self.feature_categories = None
        self.metadata = None
        self.db_path = self.data_dir / 'event_normalized_data.db'
        
    def load_model(self):
        """Load the trained neural network model and preprocessing components"""
        try:
            # Load neural network model
            model_path = self.model_dir / 'best_tuned_neural_network_model.h5'
            if model_path.exists():
                print(f"Attempting to load model from {model_path}")
                try:
                    # Try with safe_mode=False for Lambda layers
                    self.model = tf.keras.models.load_model(model_path, safe_mode=False)
                    print("✓ Loaded neural network model (safe_mode=False)")
                except TypeError:
                    # Fallback for older versions
                    print("Falling back to standard load_model")
                    self.model = tf.keras.models.load_model(model_path)
                    print("✓ Loaded neural network model")
            else:
                print(f"❌ Neural network model not found at {model_path}. Please run training first.")
                return False
            
            # Load preprocessing components
            scaler_path = self.model_dir / 'tuned_neural_network_scaler.pkl'
            if scaler_path.exists():
                self.scaler = joblib.load(scaler_path)
                print("✓ Loaded feature scaler")
            else:
                print("❌ Scaler not found")
                return False
            
            encoder_path = self.model_dir / 'tuned_neural_network_label_encoder.pkl'
            if encoder_path.exists():
                self.label_encoder = joblib.load(encoder_path)
                print("✓ Loaded label encoder")
            else:
                print("❌ Label encoder not found")
                return False
            
            features_path = self.model_dir / 'tuned_neural_network_features.pkl'
            if features_path.exists():
                self.feature_columns = joblib.load(features_path)
                print(f"✓ Loaded feature list ({len(self.feature_columns)} features)")
            else:
                print("❌ Feature list not found")
                return False
            
            # Load metadata
            metadata_path = self.model_dir / 'tuned_neural_network_metadata.json'
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                print(f"✓ Model trained on {self.metadata.get('training_date', 'unknown date')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading neural network model: {e}")
            return False
    
    def predict_single_fight(self, fighter_stats):
        """Predict outcome for a single fight"""
        if self.model is None:
            print("❌ Model not loaded. Please load model first.")
            return None
        
        try:
            # Convert dict to DataFrame if needed
            if isinstance(fighter_stats, dict):
                fighter_stats = pd.DataFrame([fighter_stats])

            # Ensure all required features are present
            missing_features = [f for f in self.feature_columns if f not in fighter_stats.columns]
            if missing_features:
                # print(f"⚠️  Missing features: {missing_features[:5]}...")
                # Fill missing features with zeros (or medians from training)
                for feature in missing_features:
                    fighter_stats[feature] = 0
            
            # Select and order features
            X = fighter_stats[self.feature_columns]
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Make prediction
            prediction_proba = self.model.predict(X_scaled, verbose=0)[0][0]
            predicted_winner = self.label_encoder.classes_[1 if prediction_proba > 0.5 else 0]
            
            # Calculate confidence
            confidence = max(prediction_proba, 1 - prediction_proba)
            
            return {
                'predicted_winner': predicted_winner,
                'confidence': confidence,
                'red_win_probability': 1 - prediction_proba,
                'blue_win_probability': prediction_proba,
                'model_type': 'Neural Network (Fighter-Aware)'
            }
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None
    
    def get_events(self, limit=20):
        """Get list of available events"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
            SELECT DISTINCT event_id, event_name, event_date, location
            FROM events
            ORDER BY event_date DESC
            LIMIT ?
            """
            events = pd.read_sql_query(query, conn, params=[limit])
            conn.close()
            return events
        except Exception as e:
            print(f"❌ Error getting events: {e}")
            return pd.DataFrame()
    
    def search_events(self, search_term):
        """Search for events by name or location"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
            SELECT DISTINCT event_id, event_name, event_date, location
            FROM events
            WHERE event_name LIKE ? OR location LIKE ?
            ORDER BY event_date DESC
            LIMIT 10
            """
            search_pattern = f"%{search_term}%"
            events = pd.read_sql_query(query, conn, params=[search_pattern, search_pattern])
            conn.close()
            return events
        except Exception as e:
            print(f"❌ Error searching events: {e}")
            return pd.DataFrame()
    
    def get_event_fights(self, event_id):
        """Get fights from a specific event"""
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
    
    def predict_from_csv_row(self, csv_data, row_index=0):
        """Predict from a row in the CSV dataset"""
        try:
            # Load the dataset
            df = pd.read_csv(self.base_dir / 'shared' / 'data' / 'event_normalized_large_dataset.csv')
            
            if row_index >= len(df):
                print(f"❌ Row index {row_index} out of range (max: {len(df)-1})")
                return None
            
            row = df.iloc[row_index:row_index+1]
            
            # Get fight info
            fight_info = {
                'red_fighter': row['r_fighter'].iloc[0],
                'blue_fighter': row['b_fighter'].iloc[0],
                'actual_winner': row['winner'].iloc[0],
                'weight_class': row['weight_class'].iloc[0],
                'method': row.get('method', 'Unknown').iloc[0] if 'method' in row.columns else 'Unknown'
            }
            
            # Make prediction
            prediction = self.predict_single_fight(row)
            
            if prediction:
                prediction.update(fight_info)
                prediction['correct_prediction'] = prediction['predicted_winner'] == fight_info['actual_winner']
            
            return prediction
            
        except Exception as e:
            print(f"❌ Error predicting from CSV: {e}")
            return None
    
    def display_model_info(self):
        """Display information about the loaded model"""
        if self.model is None:
            print("❌ No model loaded")
            return
        
        print("\n" + "="*60)
        print("NEURAL NETWORK MODEL INFORMATION")
        print("="*60)
        
        print(f"Model Type: Fighter-Aware Neural Network")
        print(f"Total Features: {len(self.feature_columns)}")
        
        if self.feature_categories:
            print(f"Red Fighter Features: {len(self.feature_categories['red_features'])}")
            print(f"Blue Fighter Features: {len(self.feature_categories['blue_features'])}")
            print(f"Differential Features: {len(self.feature_categories['diff_features'])}")
            print(f"Other Features: {len(self.feature_categories['encoded_features']) + len(self.feature_categories['other_features'])}")
        
        if self.metadata:
            print(f"Model Parameters: {self.metadata.get('model_parameters', 'Unknown'):,}")
            print(f"Training Date: {self.metadata.get('training_date', 'Unknown')}")
            print(f"Cross-Validation Accuracy: {self.metadata.get('cv_mean_accuracy', 0):.4f} ± {self.metadata.get('cv_std_accuracy', 0):.4f}")
        
        print(f"Target Classes: {list(self.label_encoder.classes_)}")
    
    def predict_quick(self):
        """Quick prediction with random fight from dataset"""
        print("\n🎲 QUICK NEURAL NETWORK PREDICTION")
        print("=" * 50)
        
        # Get random row from dataset
        import random
        df = pd.read_csv(self.base_dir / 'shared' / 'data' / 'event_normalized_large_dataset.csv')
        random_row = random.randint(0, len(df) - 1)
        
        prediction = self.predict_from_csv_row(df, random_row)
        
        if prediction:
            print(f"\n🥊 {prediction['red_fighter']} vs {prediction['blue_fighter']}")
            print(f"Weight Class: {prediction['weight_class']}")
            print(f"Actual Winner: {prediction['actual_winner']}")
            print(f"\n🤖 Neural Network Prediction:")
            print(f"Predicted Winner: {prediction['predicted_winner']}")
            print(f"Confidence: {prediction['confidence']:.1%}")
            print(f"Red Fighter Win Probability: {prediction['red_win_probability']:.1%}")
            print(f"Blue Fighter Win Probability: {prediction['blue_win_probability']:.1%}")
            
            if prediction['correct_prediction']:
                print("✅ Correct prediction!")
            else:
                print("❌ Incorrect prediction")
        else:
            print("❌ Failed to make prediction")
    
    def predict_manual_entry(self):
        """Manual fighter stat entry for prediction"""
        print("\n📝 MANUAL FIGHTER STATS ENTRY")
        print("=" * 50)
        print("This feature requires implementing a manual stat entry interface.")
        print("For now, use the quick prediction or CSV row prediction.")
        print("You can extend this method to create a full manual entry form.")
    
    def browse_events(self):
        """Browse available events"""
        print("\n📅 BROWSE EVENTS")
        print("=" * 50)
        
        events = self.get_events(20)
        if events.empty:
            print("❌ No events found in database")
            return
        
        for idx, event in events.iterrows():
            print(f"{idx+1}. {event['event_name']} ({event.get('event_date', 'Unknown date')})")
        
        try:
            choice = int(input("\\nSelect event number (or 0 to return): "))
            if choice > 0 and choice <= len(events):
                selected_event = events.iloc[choice-1]
                self.show_event_fights(selected_event['event_id'], selected_event['event_name'])
        except ValueError:
            print("Invalid selection")
    
    def show_event_fights(self, event_id, event_name):
        """Show fights from an event"""
        print(f"\\n🥊 FIGHTS FROM {event_name}")
        print("=" * 60)
        
        fights = self.get_event_fights(event_id)
        if fights.empty:
            print("❌ No fights found for this event")
            return
        
        for idx, fight in fights.iterrows():
            print(f"{idx+1}. {fight['r_fighter']} vs {fight['b_fighter']} ({fight['weight_class']})")
            print(f"   Winner: {fight['winner']} by {fight.get('method', 'Unknown')}")
    
    def predict_fight_interactive(self):
        """Interactive prediction interface - same as existing models"""
        print("\\n🤖 NEURAL NETWORK UFC FIGHT PREDICTOR")
        print("Fighter-Aware Architecture")
        print("=" * 60)
        
        if not self.load_model():
            return
        
        # Display model information
        self.display_model_info()
        
        while True:
            print("\\nChoose prediction method:")
            print("1. Quick prediction (random fight)")
            print("2. Predict specific CSV row")
            print("3. Manual fighter stat entry")
            print("4. Browse events")
            print("5. Model information")
            print("6. Exit")
            
            choice = input("\\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.predict_quick()
            elif choice == '2':
                try:
                    row_num = int(input("Enter row number (0-7439): "))
                    prediction = self.predict_from_csv_row(None, row_num)
                    if prediction:
                        print(f"\\n🥊 {prediction['red_fighter']} vs {prediction['blue_fighter']}")
                        print(f"Predicted Winner: {prediction['predicted_winner']} ({prediction['confidence']:.1%} confidence)")
                        print(f"Actual Winner: {prediction['actual_winner']}")
                        print(f"Correct: {'✅' if prediction['correct_prediction'] else '❌'}")
                except ValueError:
                    print("Please enter a valid number")
            elif choice == '3':
                self.predict_manual_entry()
            elif choice == '4':
                self.browse_events()
            elif choice == '5':
                self.display_model_info()
            elif choice == '6':
                print("Thanks for using Neural Network UFC Fight Predictor!")
                break
            else:
                print("Invalid choice. Please try again.")


def main():
    """Main prediction function"""
    predictor = EventNormalizedNeuralNetworkPredictor()
    predictor.predict_fight_interactive()


if __name__ == "__main__":
    main()