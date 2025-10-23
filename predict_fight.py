"""
Predict the outcome of an upcoming UFC fight using trained models.

Usage:
    python predict_fight.py --interactive
    python predict_fight.py --red-fighter "Fighter Name" --blue-fighter "Fighter Name"
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import argparse
import sqlite3


class FightPredictor:
    """Predict UFC fight outcomes using trained models"""
    
    def __init__(self, model_path='models/best_model.pkl', db_path='data/ufc_database.db'):
        """Initialize the predictor with trained model and database"""
        self.model_path = Path(model_path)
        self.db_path = Path(db_path)
        
        # Load the trained model
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Please train the model first using ml_pipeline.py"
            )
        
        print(f"Loading trained model from {self.model_path}...")
        self.model = joblib.load(self.model_path)
        print("✓ Model loaded successfully!")
        
    def get_fighter_stats(self, fighter_name):
        """Retrieve fighter statistics from database"""
        conn = sqlite3.connect(self.db_path)
        
        query = """
        SELECT * FROM fighter_stats 
        WHERE LOWER(name) LIKE LOWER(?)
        """
        
        df = pd.read_sql_query(query, conn, params=(f'%{fighter_name}%',))
        conn.close()
        
        if len(df) == 0:
            return None
        elif len(df) > 1:
            print(f"\nMultiple fighters found matching '{fighter_name}':")
            for idx, row in df.iterrows():
                print(f"  {idx+1}. {row['name']} (W:{row['wins']} L:{row['losses']})")
            return df
        else:
            return df.iloc[0]
    
    def manual_input_fighter(self, corner="Red"):
        """Manually input fighter statistics"""
        print(f"\n{'='*60}")
        print(f"Enter {corner} Corner Fighter Statistics")
        print(f"{'='*60}")
        
        stats = {}
        
        # Basic info
        stats['name'] = input(f"{corner} Fighter Name: ")
        stats['wins'] = float(input(f"Total Wins: "))
        stats['losses'] = float(input(f"Total Losses: "))
        stats['height'] = float(input(f"Height (cm): "))
        stats['weight'] = float(input(f"Weight (kg): "))
        stats['reach'] = float(input(f"Reach (cm): "))
        stats['age'] = float(input(f"Age: "))
        
        print("\nStance options: Orthodox, Southpaw, Switch, Open Stance")
        stats['stance'] = input(f"Stance: ")
        
        # Striking stats
        print(f"\n--- Striking Statistics ---")
        stats['SLpM'] = float(input(f"Strikes Landed per Minute (SLpM): "))
        stats['sig_str_accuracy'] = float(input(f"Significant Strike Accuracy (%): "))
        stats['SApM'] = float(input(f"Strikes Absorbed per Minute (SApM): "))
        stats['str_def'] = float(input(f"Strike Defense (%): "))
        
        # Grappling stats
        print(f"\n--- Grappling Statistics ---")
        stats['td_avg'] = float(input(f"Takedown Average (per 15 min): "))
        stats['td_accuracy'] = float(input(f"Takedown Accuracy (%): "))
        stats['td_def'] = float(input(f"Takedown Defense (%): "))
        stats['sub_avg'] = float(input(f"Submission Average (per 15 min): "))
        
        return pd.Series(stats)
    
    def create_fight_features(self, red_fighter, blue_fighter):
        """Create features for prediction from fighter statistics"""
        
        # Calculate derived features
        features = {}
        
        # Win rates
        red_total_fights = red_fighter['wins'] + red_fighter['losses']
        blue_total_fights = blue_fighter['wins'] + blue_fighter['losses']
        
        features['r_win_rate'] = red_fighter['wins'] / red_total_fights if red_total_fights > 0 else 0.5
        features['b_win_rate'] = blue_fighter['wins'] / blue_total_fights if blue_total_fights > 0 else 0.5
        features['win_rate_diff'] = features['r_win_rate'] - features['b_win_rate']
        
        # Experience
        features['r_total_fights'] = red_total_fights
        features['b_total_fights'] = blue_total_fights
        features['experience_diff'] = red_total_fights - blue_total_fights
        
        # Physical attributes
        features['r_height'] = red_fighter['height']
        features['b_height'] = blue_fighter['height']
        features['height_diff'] = red_fighter['height'] - blue_fighter['height']
        
        features['r_weight'] = red_fighter['weight']
        features['b_weight'] = blue_fighter['weight']
        features['weight_diff'] = red_fighter['weight'] - blue_fighter['weight']
        
        features['r_reach'] = red_fighter['reach']
        features['b_reach'] = blue_fighter['reach']
        features['reach_diff'] = red_fighter['reach'] - blue_fighter['reach']
        
        features['r_age'] = red_fighter['age']
        features['b_age'] = blue_fighter['age']
        features['age_diff'] = red_fighter['age'] - blue_fighter['age']
        
        # BMI
        features['r_BMI'] = red_fighter['weight'] / ((red_fighter['height']/100) ** 2)
        features['b_BMI'] = blue_fighter['weight'] / ((blue_fighter['height']/100) ** 2)
        features['BMI_diff'] = features['r_BMI'] - features['b_BMI']
        
        # Striking stats
        features['r_SLpM'] = red_fighter['SLpM']
        features['b_SLpM'] = blue_fighter['SLpM']
        features['SLpM_diff'] = red_fighter['SLpM'] - blue_fighter['SLpM']
        
        features['r_sig_str_acc'] = red_fighter['sig_str_accuracy']
        features['b_sig_str_acc'] = blue_fighter['sig_str_accuracy']
        features['sig_str_acc_diff'] = red_fighter['sig_str_accuracy'] - blue_fighter['sig_str_accuracy']
        
        features['r_SApM'] = red_fighter['SApM']
        features['b_SApM'] = blue_fighter['SApM']
        features['SApM_diff'] = red_fighter['SApM'] - blue_fighter['SApM']
        
        features['r_str_def'] = red_fighter['str_def']
        features['b_str_def'] = blue_fighter['str_def']
        features['str_def_diff'] = red_fighter['str_def'] - blue_fighter['str_def']
        
        # Striking efficiency (accuracy - defense of opponent)
        features['r_striking_efficiency'] = red_fighter['sig_str_accuracy'] - blue_fighter['str_def']
        features['b_striking_efficiency'] = blue_fighter['sig_str_accuracy'] - red_fighter['str_def']
        
        # Defensive rating (defense - opponent's accuracy)
        features['r_defensive_rating'] = red_fighter['str_def'] - blue_fighter['sig_str_accuracy']
        features['b_defensive_rating'] = blue_fighter['str_def'] - red_fighter['sig_str_accuracy']
        
        # Grappling stats
        features['r_td_avg'] = red_fighter['td_avg']
        features['b_td_avg'] = blue_fighter['td_avg']
        features['td_avg_diff'] = red_fighter['td_avg'] - blue_fighter['td_avg']
        
        features['r_td_acc'] = red_fighter['td_accuracy']
        features['b_td_acc'] = blue_fighter['td_accuracy']
        features['td_acc_diff'] = red_fighter['td_accuracy'] - blue_fighter['td_accuracy']
        
        features['r_td_def'] = red_fighter['td_def']
        features['b_td_def'] = blue_fighter['td_def']
        features['td_def_diff'] = red_fighter['td_def'] - blue_fighter['td_def']
        
        features['r_sub_avg'] = red_fighter['sub_avg']
        features['b_sub_avg'] = blue_fighter['sub_avg']
        features['sub_avg_diff'] = red_fighter['sub_avg'] - blue_fighter['sub_avg']
        
        # Grappling efficiency
        features['r_grappling_efficiency'] = red_fighter['td_accuracy'] - blue_fighter['td_def']
        features['b_grappling_efficiency'] = blue_fighter['td_accuracy'] - red_fighter['td_def']
        
        # Stance encoding (one-hot encoding)
        stances = ['Orthodox', 'Southpaw', 'Switch', 'Open Stance']
        for stance in stances:
            features[f'r_stance_{stance}'] = 1 if red_fighter['stance'] == stance else 0
            features[f'b_stance_{stance}'] = 1 if blue_fighter['stance'] == stance else 0
        
        # Stance matchup
        features['same_stance'] = 1 if red_fighter['stance'] == blue_fighter['stance'] else 0
        
        return pd.DataFrame([features])
    
    def predict(self, red_fighter, blue_fighter):
        """Make prediction for the fight"""
        
        # Create feature dataframe
        X = self.create_fight_features(red_fighter, blue_fighter)
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        # Display results
        print("\n" + "="*60)
        print("FIGHT PREDICTION")
        print("="*60)
        print(f"\n🔴 Red Corner: {red_fighter['name']}")
        print(f"   Record: {red_fighter['wins']}-{red_fighter['losses']}")
        print(f"   Win Rate: {(red_fighter['wins']/(red_fighter['wins']+red_fighter['losses']))*100:.1f}%")
        
        print(f"\n🔵 Blue Corner: {blue_fighter['name']}")
        print(f"   Record: {blue_fighter['wins']}-{blue_fighter['losses']}")
        print(f"   Win Rate: {(blue_fighter['wins']/(blue_fighter['wins']+blue_fighter['losses']))*100:.1f}%")
        
        print(f"\n{'='*60}")
        print("PREDICTION RESULTS")
        print("="*60)
        
        # Map prediction to winner
        winner_map = {0: 'Blue', 1: 'Red', 2: 'Draw'}
        predicted_winner = winner_map.get(prediction, 'Unknown')
        
        print(f"\n🏆 Predicted Winner: {predicted_winner} Corner")
        print(f"\nWin Probabilities:")
        print(f"   🔴 Red Corner:  {probabilities[1]*100:.2f}%")
        print(f"   🔵 Blue Corner: {probabilities[0]*100:.2f}%")
        if len(probabilities) > 2:
            print(f"   🤝 Draw:        {probabilities[2]*100:.2f}%")
        
        # Confidence level
        max_prob = max(probabilities)
        if max_prob >= 0.7:
            confidence = "HIGH"
        elif max_prob >= 0.55:
            confidence = "MODERATE"
        else:
            confidence = "LOW"
        
        print(f"\n📊 Prediction Confidence: {confidence} ({max_prob*100:.2f}%)")
        
        # Key advantages
        print(f"\n{'='*60}")
        print("KEY ADVANTAGES")
        print("="*60)
        
        # Physical advantages
        if X['height_diff'].values[0] > 5:
            print(f"✓ Red has significant height advantage (+{X['height_diff'].values[0]:.1f} cm)")
        elif X['height_diff'].values[0] < -5:
            print(f"✓ Blue has significant height advantage (+{abs(X['height_diff'].values[0]):.1f} cm)")
        
        if X['reach_diff'].values[0] > 5:
            print(f"✓ Red has significant reach advantage (+{X['reach_diff'].values[0]:.1f} cm)")
        elif X['reach_diff'].values[0] < -5:
            print(f"✓ Blue has significant reach advantage (+{abs(X['reach_diff'].values[0]):.1f} cm)")
        
        # Experience
        if X['experience_diff'].values[0] > 5:
            print(f"✓ Red has more experience (+{X['experience_diff'].values[0]:.0f} fights)")
        elif X['experience_diff'].values[0] < -5:
            print(f"✓ Blue has more experience (+{abs(X['experience_diff'].values[0]):.0f} fights)")
        
        # Striking
        if X['r_striking_efficiency'].values[0] > 10:
            print(f"✓ Red has striking advantage (efficiency: {X['r_striking_efficiency'].values[0]:.1f}%)")
        elif X['b_striking_efficiency'].values[0] > 10:
            print(f"✓ Blue has striking advantage (efficiency: {X['b_striking_efficiency'].values[0]:.1f}%)")
        
        # Grappling
        if X['r_grappling_efficiency'].values[0] > 10:
            print(f"✓ Red has grappling advantage (efficiency: {X['r_grappling_efficiency'].values[0]:.1f}%)")
        elif X['b_grappling_efficiency'].values[0] > 10:
            print(f"✓ Blue has grappling advantage (efficiency: {X['b_grappling_efficiency'].values[0]:.1f}%)")
        
        print(f"\n{'='*60}\n")
        
        return prediction, probabilities


def interactive_mode():
    """Run in interactive mode for manual input"""
    predictor = FightPredictor()
    
    print("\n" + "="*60)
    print("UFC FIGHT PREDICTOR - Interactive Mode")
    print("="*60)
    
    while True:
        print("\nOptions:")
        print("1. Look up fighters from database")
        print("2. Manually enter fighter statistics")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '3':
            print("\nExiting predictor. Good luck with your predictions!")
            break
        
        elif choice == '1':
            # Database lookup
            red_name = input("\nEnter Red Corner fighter name: ").strip()
            red_fighter = predictor.get_fighter_stats(red_name)
            
            if red_fighter is None:
                print(f"Fighter '{red_name}' not found in database.")
                continue
            elif isinstance(red_fighter, pd.DataFrame):
                choice_idx = int(input("Select fighter number: ")) - 1
                red_fighter = red_fighter.iloc[choice_idx]
            
            blue_name = input("\nEnter Blue Corner fighter name: ").strip()
            blue_fighter = predictor.get_fighter_stats(blue_name)
            
            if blue_fighter is None:
                print(f"Fighter '{blue_name}' not found in database.")
                continue
            elif isinstance(blue_fighter, pd.DataFrame):
                choice_idx = int(input("Select fighter number: ")) - 1
                blue_fighter = blue_fighter.iloc[choice_idx]
            
            # Make prediction
            predictor.predict(red_fighter, blue_fighter)
        
        elif choice == '2':
            # Manual input
            red_fighter = predictor.manual_input_fighter("Red")
            blue_fighter = predictor.manual_input_fighter("Blue")
            
            # Make prediction
            predictor.predict(red_fighter, blue_fighter)
        
        else:
            print("Invalid option. Please select 1, 2, or 3.")


def main():
    parser = argparse.ArgumentParser(description='Predict UFC fight outcomes')
    parser.add_argument('--interactive', action='store_true', 
                       help='Run in interactive mode')
    parser.add_argument('--red-fighter', type=str, 
                       help='Red corner fighter name')
    parser.add_argument('--blue-fighter', type=str, 
                       help='Blue corner fighter name')
    parser.add_argument('--model', type=str, default='models/best_model.pkl',
                       help='Path to trained model file')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.red_fighter and args.blue_fighter:
        predictor = FightPredictor(model_path=args.model)
        
        red_fighter = predictor.get_fighter_stats(args.red_fighter)
        if red_fighter is None:
            print(f"Red fighter '{args.red_fighter}' not found.")
            return
        elif isinstance(red_fighter, pd.DataFrame):
            print(f"Multiple matches for '{args.red_fighter}'. Use interactive mode.")
            return
        
        blue_fighter = predictor.get_fighter_stats(args.blue_fighter)
        if blue_fighter is None:
            print(f"Blue fighter '{args.blue_fighter}' not found.")
            return
        elif isinstance(blue_fighter, pd.DataFrame):
            print(f"Multiple matches for '{args.blue_fighter}'. Use interactive mode.")
            return
        
        predictor.predict(red_fighter, blue_fighter)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
