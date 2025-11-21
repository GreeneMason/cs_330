"""
Unified Fight Prediction Interface
Supports Neural Network, Ensemble, and Simple models with model comparison
"""

import pandas as pd
import numpy as np
import sys
import argparse
from pathlib import Path

# Add paths for imports
sys.path.append('../training')
sys.path.append('../prediction')

from train_neural_network_hypertuned import HyperparameterTunedNeuralNetwork

class UnifiedFightPredictor:
    """Unified interface for all prediction models"""
    
    def __init__(self):
        self.models = {}
        self.model_info = {
            'neural_network': {
                'name': 'Neural Network',
                'accuracy': '89.50%',
                'description': 'Fighter-aware deep learning model',
                'speed': 'Medium'
            },
            'ensemble': {
                'name': 'Ensemble Model', 
                'accuracy': '~85%',
                'description': 'XGBoost + Random Forest ensemble',
                'speed': 'Fast'
            },
            'simple': {
                'name': 'Simple Model',
                'accuracy': '~75%', 
                'description': 'Basic decision tree',
                'speed': 'Very Fast'
            }
        }
        
    def load_model(self, model_type):
        """Load specified model type"""
        if model_type in self.models:
            return self.models[model_type]
            
        print(f"🔄 Loading {self.model_info[model_type]['name']}...")
        
        if model_type == 'neural_network':
            model = HyperparameterTunedNeuralNetwork()
            try:
                model.load_best_model()
                self.models[model_type] = model
                print(f"✅ Neural Network loaded successfully")
            except Exception as e:
                print(f"❌ Failed to load neural network: {e}")
                return None
                
        elif model_type == 'ensemble':
            # Import and load ensemble model
            from train_event_normalized_model import EventNormalizedModel
            model = EventNormalizedModel()
            try:
                model.load_model()
                self.models[model_type] = model
                print(f"✅ Ensemble model loaded successfully")
            except Exception as e:
                print(f"❌ Failed to load ensemble model: {e}")
                return None
                
        elif model_type == 'simple':
            # Import and load simple model  
            from train_simple_model import SimpleModel
            model = SimpleModel()
            try:
                model.load_model()
                self.models[model_type] = model
                print(f"✅ Simple model loaded successfully")
            except Exception as e:
                print(f"❌ Failed to load simple model: {e}")
                return None
                
        return self.models.get(model_type)
    
    def predict_fight(self, fighter_data, model_type='neural_network', verbose=True):
        """Predict single fight outcome"""
        
        model = self.load_model(model_type)
        if model is None:
            return None
            
        if verbose:
            print(f"\n🥊 Predicting with {self.model_info[model_type]['name']}")
            print(f"   Accuracy: {self.model_info[model_type]['accuracy']}")
            print(f"   Speed: {self.model_info[model_type]['speed']}")
        
        try:
            if model_type == 'neural_network':
                # Neural network prediction
                prediction_prob = model.predict_fight(fighter_data)
                prediction = "Red Fighter Wins" if prediction_prob > 0.5 else "Blue Fighter Wins"
                confidence = max(prediction_prob, 1 - prediction_prob)
                
            else:
                # Ensemble/Simple model prediction
                prediction_prob = model.predict(fighter_data)
                prediction = "Red Fighter Wins" if prediction_prob > 0.5 else "Blue Fighter Wins"
                confidence = max(prediction_prob, 1 - prediction_prob)
            
            result = {
                'model': self.model_info[model_type]['name'],
                'prediction': prediction,
                'probability': float(prediction_prob),
                'confidence': float(confidence),
                'winner': 'Red' if prediction_prob > 0.5 else 'Blue'
            }
            
            if verbose:
                print(f"   Prediction: {prediction}")
                print(f"   Probability: {prediction_prob:.3f}")
                print(f"   Confidence: {confidence:.3f}")
            
            return result
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            return None
    
    def compare_all_models(self, fighter_data):
        """Get predictions from all available models for comparison"""
        
        print("\n" + "="*60)
        print("🏆 MULTI-MODEL FIGHT PREDICTION")
        print("="*60)
        
        results = {}
        
        for model_type in ['neural_network', 'ensemble', 'simple']:
            result = self.predict_fight(fighter_data, model_type, verbose=True)
            if result:
                results[model_type] = result
                print()
        
        # Summary comparison
        if len(results) > 1:
            print("📊 MODEL CONSENSUS:")
            
            # Check if all models agree
            predictions = [r['winner'] for r in results.values()]
            if len(set(predictions)) == 1:
                print(f"   ✅ All models agree: {predictions[0]} Fighter Wins")
            else:
                print(f"   ⚠️ Models disagree:")
                for model_type, result in results.items():
                    print(f"      {result['model']}: {result['winner']} ({result['probability']:.3f})")
            
            # Average confidence
            avg_confidence = np.mean([r['confidence'] for r in results.values()])
            print(f"   Average Confidence: {avg_confidence:.3f}")
            
            # Recommend best model
            best_model = max(results.items(), key=lambda x: float(self.model_info[x[0]]['accuracy'].rstrip('%')))
            print(f"   🎯 Recommended: {best_model[1]['model']} (Highest Accuracy)")
        
        return results
    
    def interactive_prediction(self):
        """Interactive prediction interface"""
        
        print("🥊 UFC Fight Predictor - Interactive Mode")
        print("="*50)
        
        # Model selection
        print("\nAvailable Models:")
        for i, (model_type, info) in enumerate(self.model_info.items(), 1):
            print(f"  {i}. {info['name']} - {info['accuracy']} accuracy ({info['speed']})")
        
        print("  4. Compare All Models")
        
        while True:
            try:
                choice = input("\nSelect model (1-4, or 'q' to quit): ").strip()
                
                if choice.lower() == 'q':
                    print("👋 Goodbye!")
                    break
                
                choice = int(choice)
                
                if choice == 4:
                    # Compare all models
                    fighter_data = self.get_fighter_input()
                    if fighter_data is not None:
                        self.compare_all_models(fighter_data)
                
                elif 1 <= choice <= 3:
                    model_types = ['neural_network', 'ensemble', 'simple']
                    selected_model = model_types[choice - 1]
                    
                    fighter_data = self.get_fighter_input()
                    if fighter_data is not None:
                        self.predict_fight(fighter_data, selected_model)
                
                else:
                    print("❌ Invalid choice. Please select 1-4.")
                    
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
    
    def get_fighter_input(self):
        """Get fighter data from user input"""
        
        print("\n📝 Enter Fighter Information:")
        print("   (Enter sample data or 'random' for random fight)")
        
        choice = input("Use sample data? (y/n/random): ").strip().lower()
        
        if choice == 'y':
            return self.get_sample_fight_data()
        elif choice == 'random':
            return self.get_random_fight_data()
        else:
            print("📝 Manual data entry not yet implemented.")
            print("   Using sample data instead...")
            return self.get_sample_fight_data()
    
    def get_sample_fight_data(self):
        """Return sample fight data"""
        
        print("📊 Using sample fight: Jon Jones vs Daniel Cormier style matchup")
        
        # This would need to be replaced with actual feature engineering
        # For now, return placeholder that works with loaded models
        sample_data = {
            'red_fighter': 'Jon Jones',
            'blue_fighter': 'Daniel Cormier',
            # Add actual features here based on your model requirements
        }
        
        return sample_data
    
    def get_random_fight_data(self):
        """Generate random fight data from dataset"""
        
        print("🎲 Generating random historical fight...")
        
        try:
            # Load a random fight from the dataset
            df = pd.read_csv('../../shared/data/event_normalized_large_dataset.csv')
            random_fight = df.sample(1).iloc[0]
            
            print(f"📊 Random fight selected from dataset")
            return random_fight.to_dict()
            
        except Exception as e:
            print(f"❌ Failed to load random fight: {e}")
            return self.get_sample_fight_data()
    
    def batch_predict(self, data_file, model_type='neural_network', output_file=None):
        """Predict multiple fights from file"""
        
        print(f"📂 Loading batch data from {data_file}")
        
        try:
            df = pd.read_csv(data_file)
            model = self.load_model(model_type)
            
            if model is None:
                return None
            
            print(f"🔄 Processing {len(df)} fights with {self.model_info[model_type]['name']}")
            
            predictions = []
            for idx, row in df.iterrows():
                result = self.predict_fight(row.to_dict(), model_type, verbose=False)
                if result:
                    predictions.append(result)
                
                if (idx + 1) % 100 == 0:
                    print(f"   Processed {idx + 1}/{len(df)} fights...")
            
            # Save results
            if output_file:
                results_df = pd.DataFrame(predictions)
                results_df.to_csv(output_file, index=False)
                print(f"💾 Results saved to {output_file}")
            
            return predictions
            
        except Exception as e:
            print(f"❌ Batch prediction failed: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='Fight Prediction - Unified Interface')
    parser.add_argument('--model', choices=['neural_network', 'ensemble', 'simple', 'all'], 
                       default='neural_network', help='Model to use for prediction')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    parser.add_argument('--batch', type=str, help='Batch predict from CSV file')
    parser.add_argument('--output', type=str, help='Output file for batch predictions')
    
    args = parser.parse_args()
    
    predictor = UnifiedFightPredictor()
    
    if args.interactive:
        predictor.interactive_prediction()
    elif args.batch:
        predictor.batch_predict(args.batch, args.model, args.output)
    else:
        # Single prediction with sample data
        fighter_data = predictor.get_sample_fight_data()
        
        if args.model == 'all':
            predictor.compare_all_models(fighter_data)
        else:
            predictor.predict_fight(fighter_data, args.model)

if __name__ == "__main__":
    main()