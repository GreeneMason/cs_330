"""
Simple UFC Fight Predictor - Works with trained model
"""

import pandas as pd
import numpy as np
import joblib
import sqlite3
from pathlib import Path
import argparse


class SimpleFightPredictor:
    """Simple fight predictor that works with the trained model"""
    
    def __init__(self, model_path='models/best_model.pkl'):
        """Load the trained model"""
        print(f"\nLoading trained model from {model_path}...")
        
        model_data = joblib.load(model_path)
        self.model = model_data['model']
        self.feature_columns = model_data['feature_columns']
        self.label_encoder = model_data['label_encoder']
        
        print(f"✓ Model loaded: {model_data['model_name']}")
        print(f"✓ Features required: {len(self.feature_columns)}")
        
    def get_fighter_from_db(self, fighter_name, db_path='data/ufc_database.db'):
        """Get fighter stats from database"""
        conn = sqlite3.connect(db_path)
        
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
                print(f"  {idx+1}. {row['name']} (Record: {row['wins']}-{row['losses']})")
            choice = int(input("Select fighter number: ")) - 1
            return df.iloc[choice]
        else:
            return df.iloc[0]
    
    def manual_input_fighter(self, corner="Red"):
        """Manually input fighter statistics"""
        print(f"\n{'='*60}")
        print(f"Enter {corner} Corner Fighter Statistics")
        print(f"{'='*60}")
        
        fighter = {}
        fighter['name'] = input(f"{corner} Fighter Name: ")
        fighter['wins'] = float(input("Total Wins: "))
        fighter['losses'] = float(input("Total Losses: "))
        fighter['height'] = float(input("Height (cm): "))
        fighter['weight'] = float(input("Weight (kg): "))
        fighter['reach'] = float(input("Reach (cm): "))
        fighter['age'] = float(input("Age: "))
        
        print("\n--- Striking Stats ---")
        fighter['slpm'] = float(input("Strikes Landed per Minute: "))
        fighter['sig_str_acc'] = float(input("Striking Accuracy (%): "))
        fighter['sapm'] = float(input("Strikes Absorbed per Minute: "))
        fighter['str_def'] = float(input("Strike Defense (%): "))
        
        print("\n--- Grappling Stats ---")
        fighter['td_avg'] = float(input("Takedown Average (per 15 min): "))
        fighter['td_acc'] = float(input("Takedown Accuracy (%): "))
        fighter['td_def'] = float(input("Takedown Defense (%): "))
        fighter['sub_avg'] = float(input("Submission Average (per 15 min): "))
        
        return pd.Series(fighter)
    
    def create_features_from_fighters(self, red_fighter, blue_fighter):
        """Create features matching the trained model"""
        
        # Map database columns to feature names expected by model
        # Database has: slpm, sig_str_acc, sapm, str_def, td_acc, td_def, td_avg, sub_avg
        # Model expects: r_wins_total, r_SLpM_total, etc.
        
        features = {}
        
        # Red corner - use _total suffix to match training data
        features['r_wins_total'] = red_fighter['wins']
        features['r_losses_total'] = red_fighter['losses']
        features['r_height'] = red_fighter['height']
        features['r_weight'] = red_fighter['weight']
        features['r_reach'] = red_fighter['reach']
        features['r_age'] = red_fighter['age']
        features['r_SLpM_total'] = red_fighter['slpm']
        features['r_sig_str_acc_total'] = red_fighter['sig_str_acc']
        features['r_SApM_total'] = red_fighter['sapm']
        features['r_str_def_total'] = red_fighter['str_def']
        features['r_td_avg'] = red_fighter['td_avg']
        features['r_td_acc_total'] = red_fighter['td_acc']
        features['r_td_def_total'] = red_fighter['td_def']
        features['r_sub_avg'] = red_fighter['sub_avg']
        
        # Blue corner
        features['b_wins_total'] = blue_fighter['wins']
        features['b_losses_total'] = blue_fighter['losses']
        features['b_height'] = blue_fighter['height']
        features['b_weight'] = blue_fighter['weight']
        features['b_reach'] = blue_fighter['reach']
        features['b_age'] = blue_fighter['age']
        features['b_SLpM_total'] = blue_fighter['slpm']
        features['b_sig_str_acc_total'] = blue_fighter['sig_str_acc']
        features['b_SApM_total'] = blue_fighter['sapm']
        features['b_str_def_total'] = blue_fighter['str_def']
        features['b_td_avg'] = blue_fighter['td_avg']
        features['b_td_acc_total'] = blue_fighter['td_acc']
        features['b_td_def_total'] = blue_fighter['td_def']
        features['b_sub_avg'] = blue_fighter['sub_avg']
        
        # Engineered features (same as training)
        red_total_fights = features['r_wins_total'] + features['r_losses_total']
        blue_total_fights = features['b_wins_total'] + features['b_losses_total']
        
        features['r_win_rate'] = features['r_wins_total'] / (red_total_fights + 0.01)
        features['b_win_rate'] = features['b_wins_total'] / (blue_total_fights + 0.01)
        features['win_rate_diff'] = features['r_win_rate'] - features['b_win_rate']
        
        features['r_fights'] = red_total_fights
        features['b_fights'] = blue_total_fights
        features['experience_diff'] = features['r_fights'] - features['b_fights']
        
        features['height_diff'] = features['r_height'] - features['b_height']
        features['weight_diff'] = features['r_weight'] - features['b_weight']
        features['reach_diff'] = features['r_reach'] - features['b_reach']
        features['age_diff'] = features['r_age'] - features['b_age']
        
        features['SLpM_diff'] = features['r_SLpM_total'] - features['b_SLpM_total']
        features['sig_str_acc_diff'] = features['r_sig_str_acc_total'] - features['b_sig_str_acc_total']
        features['SApM_diff'] = features['r_SApM_total'] - features['b_SApM_total']
        features['str_def_diff'] = features['r_str_def_total'] - features['b_str_def_total']
        
        features['td_avg_diff'] = features['r_td_avg'] - features['b_td_avg']
        features['td_acc_diff'] = features['r_td_acc_total'] - features['b_td_acc_total']
        features['td_def_diff'] = features['r_td_def_total'] - features['b_td_def_total']
        features['sub_avg_diff'] = features['r_sub_avg'] - features['b_sub_avg']
        
        # Create DataFrame with exact columns the model expects
        X = pd.DataFrame([features])
        
        # Ensure all required features are present
        for col in self.feature_columns:
            if col not in X.columns:
                X[col] = 0  # Fill missing features with 0
        
        # Return only the columns the model was trained on, in the same order
        return X[self.feature_columns]
    
    def predict(self, red_fighter, blue_fighter):
        """Make prediction"""
        
        # Create features
        X = self.create_features_from_fighters(red_fighter, blue_fighter)
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        # Display results
        print("\n" + "="*60)
        print("FIGHT PREDICTION")
        print("="*60)
        
        print(f"\n🔴 Red Corner: {red_fighter['name']}")
        print(f"   Record: {int(red_fighter['wins'])}-{int(red_fighter['losses'])}")
        red_total = red_fighter['wins'] + red_fighter['losses']
        if red_total > 0:
            print(f"   Win Rate: {(red_fighter['wins']/red_total)*100:.1f}%")
        
        print(f"\n🔵 Blue Corner: {blue_fighter['name']}")
        print(f"   Record: {int(blue_fighter['wins'])}-{int(blue_fighter['losses'])}")
        blue_total = blue_fighter['wins'] + blue_fighter['losses']
        if blue_total > 0:
            print(f"   Win Rate: {(blue_fighter['wins']/blue_total)*100:.1f}%")
        
        print(f"\n{'='*60}")
        print("PREDICTION")
        print("="*60)
        
        # Get predicted winner
        winner = self.label_encoder.inverse_transform([prediction])[0]
        
        print(f"\n🏆 Predicted Winner: {winner} Corner")
        
        print(f"\nWin Probabilities:")
        class_names = self.label_encoder.classes_
        for i, class_name in enumerate(class_names):
            print(f"   {class_name} Corner: {probabilities[i]*100:.2f}%")
        
        # Confidence
        max_prob = max(probabilities)
        if max_prob >= 0.7:
            confidence = "HIGH"
        elif max_prob >= 0.6:
            confidence = "MODERATE"
        else:
            confidence = "LOW"
        
        print(f"\n📊 Prediction Confidence: {confidence} ({max_prob*100:.2f}%)")
        
        # Show key differences
        print(f"\n{'='*60}")
        print("KEY FACTORS")
        print("="*60)
        
        win_rate_r = red_fighter['wins'] / (red_total + 0.01)
        win_rate_b = blue_fighter['wins'] / (blue_total + 0.01)
        
        if abs(win_rate_r - win_rate_b) > 0.1:
            if win_rate_r > win_rate_b:
                print(f"✓ Red has better win rate ({win_rate_r*100:.1f}% vs {win_rate_b*100:.1f}%)")
            else:
                print(f"✓ Blue has better win rate ({win_rate_b*100:.1f}% vs {win_rate_r*100:.1f}%)")
        
        if abs(red_fighter['height'] - blue_fighter['height']) > 5:
            if red_fighter['height'] > blue_fighter['height']:
                print(f"✓ Red has height advantage (+{red_fighter['height'] - blue_fighter['height']:.1f} cm)")
            else:
                print(f"✓ Blue has height advantage (+{blue_fighter['height'] - red_fighter['height']:.1f} cm)")
        
        if abs(red_fighter['reach'] - blue_fighter['reach']) > 5:
            if red_fighter['reach'] > blue_fighter['reach']:
                print(f"✓ Red has reach advantage (+{red_fighter['reach'] - blue_fighter['reach']:.1f} cm)")
            else:
                print(f"✓ Blue has reach advantage (+{blue_fighter['reach'] - red_fighter['reach']:.1f} cm)")
        
        if abs(red_total - blue_total) > 5:
            if red_total > blue_total:
                print(f"✓ Red has more experience (+{red_total - blue_total:.0f} fights)")
            else:
                print(f"✓ Blue has more experience (+{blue_total - red_total:.0f} fights)")
        
        print("\n" + "="*60 + "\n")
        
        return prediction, probabilities


def interactive_mode(predictor):
    """Run in interactive mode"""
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
            print("\nExiting. Thanks for using UFC Fight Predictor!")
            break
        
        elif choice == '1':
            # Database lookup
            red_name = input("\nEnter Red Corner fighter name: ").strip()
            red_fighter = predictor.get_fighter_from_db(red_name)
            
            if red_fighter is None:
                print(f"❌ Fighter '{red_name}' not found in database.")
                continue
            
            blue_name = input("Enter Blue Corner fighter name: ").strip()
            blue_fighter = predictor.get_fighter_from_db(blue_name)
            
            if blue_fighter is None:
                print(f"❌ Fighter '{blue_name}' not found in database.")
                continue
            
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
                       help='Red corner fighter name (from database)')
    parser.add_argument('--blue-fighter', type=str, 
                       help='Blue corner fighter name (from database)')
    
    args = parser.parse_args()
    
    # Load model
    try:
        predictor = SimpleFightPredictor()
    except FileNotFoundError:
        print("\n❌ Error: Model not found!")
        print("Please train the model first:")
        print("  python train_simple_model.py")
        return
    
    if args.interactive:
        interactive_mode(predictor)
    
    elif args.red_fighter and args.blue_fighter:
        # Command line mode
        red_fighter = predictor.get_fighter_from_db(args.red_fighter)
        if red_fighter is None:
            print(f"\n❌ Fighter '{args.red_fighter}' not found in database.")
            return
        
        blue_fighter = predictor.get_fighter_from_db(args.blue_fighter)
        if blue_fighter is None:
            print(f"\n❌ Fighter '{args.blue_fighter}' not found in database.")
            return
        
        predictor.predict(red_fighter, blue_fighter)
    
    else:
        print("\nUsage:")
        print("  Interactive mode:  python predict_simple.py --interactive")
        print("  Command line:      python predict_simple.py --red-fighter \"Name\" --blue-fighter \"Name\"")
        print("\nExample:")
        print('  python predict_simple.py --red-fighter "Jon Jones" --blue-fighter "Daniel Cormier"')


if __name__ == '__main__':
    main()
