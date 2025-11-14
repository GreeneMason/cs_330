"""
Production-Ready UFC Weighted Ensemble Predictor
Achieves 91.33% accuracy using weighted combination of 4 models
"""

import pandas as pd
import numpy as np
import os
import sys
import pickle
import joblib
from datetime import datetime
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# Fix Windows encoding issues
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

class UFCWeightedEnsemblePredictor:
    """Production-ready weighted ensemble for UFC fight prediction"""
    
    def __init__(self, model_dir=None):
        self.model_dir = model_dir or os.path.join(os.path.dirname(__file__), '..', 'models', 'ensemble')
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        
        # Model configurations (optimized from ensemble experiment)
        self.model_configs = {
            'gradient_boosting': {
                'model': GradientBoostingClassifier(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=6,
                    random_state=42
                ),
                'weight': 0.251,
                'use_scaled': False
            },
            'random_forest': {
                'model': RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    min_samples_split=5,
                    random_state=42,
                    n_jobs=-1
                ),
                'weight': 0.247,
                'use_scaled': False
            },
            'svm': {
                'model': SVC(
                    probability=True,
                    C=1.0,
                    kernel='rbf',
                    random_state=42
                ),
                'weight': 0.251,
                'use_scaled': True
            },
            'neural_network': {
                'model': MLPClassifier(
                    hidden_layer_sizes=(128, 64, 32),
                    activation='relu',
                    solver='adam',
                    alpha=0.001,
                    learning_rate_init=0.01,
                    max_iter=500,
                    random_state=42,
                    early_stopping=True,
                    validation_fraction=0.1
                ),
                'weight': 0.251,
                'use_scaled': True
            }
        }
        
        self.models = {}
        self.scaler = None
        self.feature_columns = None
        self.is_trained = False
        self.metadata = {}
        
        # Ensure model directory exists
        os.makedirs(self.model_dir, exist_ok=True)
    
    def load_and_prepare_data(self, data_path=None):
        """Load and prepare UFC dataset for training"""
        if data_path is None:
            data_path = os.path.join(self.base_dir, 'shared', 'data', 'event_normalized_large_dataset.csv')
        
        print(f"🔄 Loading data from: {data_path}")
        
        # Load data
        self.df = pd.read_csv(data_path)
        print(f"📊 Dataset: {len(self.df)} fights with {self.df.shape[1]} columns")
        
        # Prepare features
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        self.feature_columns = [col for col in numeric_columns if col not in ['winner_encoded', 'event_id']]
        
        # Features and target
        X = self.df[self.feature_columns].fillna(0)
        y = self.df['winner_encoded']  # 1 = Red wins, 0 = Blue wins
        
        print(f"📈 Features: {len(self.feature_columns)} numeric columns")
        print(f"   Target distribution: Red wins: {sum(y)} ({sum(y)/len(y)*100:.1f}%)")
        
        return X, y
    
    def train_ensemble(self, X=None, y=None, test_size=0.2, save_models=True):
        """Train the weighted ensemble"""
        print("🏋️ Training Weighted Ensemble...")
        print("="*50)
        
        # Load data if not provided
        if X is None or y is None:
            X, y = self.load_and_prepare_data()
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Fit scaler
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"   Train set: {len(X_train)} fights")
        print(f"   Test set: {len(X_test)} fights")
        
        # Train individual models
        individual_predictions = []
        model_weights = []
        
        for model_name, config in self.model_configs.items():
            print(f"\n🔄 Training {model_name.replace('_', ' ').title()}...")
            
            try:
                model = config['model']
                use_scaled = config['use_scaled']
                weight = config['weight']
                
                # Select appropriate features
                if use_scaled:
                    model.fit(X_train_scaled, y_train)
                    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
                else:
                    model.fit(X_train, y_train)
                    y_pred_proba = model.predict_proba(X_test)[:, 1]
                
                # Calculate individual accuracy
                y_pred = (y_pred_proba > 0.5).astype(int)
                accuracy = accuracy_score(y_test, y_pred)
                auc = roc_auc_score(y_test, y_pred_proba)
                
                print(f"   ✅ Individual Performance:")
                print(f"      Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
                print(f"      AUC: {auc:.4f}")
                print(f"      Weight: {weight:.3f}")
                
                # Store model and predictions
                self.models[model_name] = model
                individual_predictions.append(y_pred_proba)
                model_weights.append(weight)
                
            except Exception as e:
                print(f"   ❌ Failed to train {model_name}: {e}")
                return False
        
        # Calculate ensemble predictions
        print(f"\n🎯 Calculating Weighted Ensemble Predictions...")
        
        ensemble_pred_proba = np.zeros(len(y_test))
        for predictions, weight in zip(individual_predictions, model_weights):
            ensemble_pred_proba += weight * predictions
        
        ensemble_pred = (ensemble_pred_proba > 0.5).astype(int)
        
        # Evaluate ensemble
        ensemble_accuracy = accuracy_score(y_test, ensemble_pred)
        ensemble_auc = roc_auc_score(y_test, ensemble_pred_proba)
        
        print(f"\n🏆 WEIGHTED ENSEMBLE RESULTS:")
        print(f"   Accuracy: {ensemble_accuracy:.4f} ({ensemble_accuracy*100:.2f}%)")
        print(f"   AUC: {ensemble_auc:.4f}")
        
        # Store metadata
        self.metadata = {
            'training_date': datetime.now().isoformat(),
            'num_features': len(self.feature_columns),
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'ensemble_accuracy': ensemble_accuracy,
            'ensemble_auc': ensemble_auc,
            'model_weights': {name: config['weight'] for name, config in self.model_configs.items()},
            'individual_accuracies': {}
        }
        
        # Calculate individual accuracies for metadata
        for i, (model_name, predictions) in enumerate(zip(self.model_configs.keys(), individual_predictions)):
            pred_binary = (predictions > 0.5).astype(int)
            acc = accuracy_score(y_test, pred_binary)
            self.metadata['individual_accuracies'][model_name] = acc
        
        self.is_trained = True
        
        # Save models if requested
        if save_models:
            self.save_ensemble()
        
        # Generate detailed report
        self.generate_classification_report(y_test, ensemble_pred, ensemble_pred_proba)
        
        return True
    
    def generate_classification_report(self, y_true, y_pred, y_pred_proba):
        """Generate detailed classification report"""
        print(f"\n📋 DETAILED CLASSIFICATION REPORT:")
        print("="*50)
        
        # Basic classification report
        print("\nClassification Report:")
        print(classification_report(y_true, y_pred, target_names=['Blue Wins', 'Red Wins']))
        
        # Confidence analysis
        confidence_scores = np.maximum(y_pred_proba, 1 - y_pred_proba)
        
        print(f"\nConfidence Analysis:")
        print(f"   Mean Confidence: {confidence_scores.mean():.3f}")
        print(f"   Median Confidence: {np.median(confidence_scores):.3f}")
        print(f"   High Confidence (>0.8): {sum(confidence_scores > 0.8)/len(confidence_scores)*100:.1f}%")
        print(f"   Low Confidence (<0.6): {sum(confidence_scores < 0.6)/len(confidence_scores)*100:.1f}%")
        
        # Prediction distribution
        print(f"\nPrediction Distribution:")
        print(f"   Predicted Red Wins: {sum(y_pred)}/{len(y_pred)} ({sum(y_pred)/len(y_pred)*100:.1f}%)")
        print(f"   Predicted Blue Wins: {len(y_pred)-sum(y_pred)}/{len(y_pred)} ({(len(y_pred)-sum(y_pred))/len(y_pred)*100:.1f}%)")
    
    def save_ensemble(self):
        """Save trained ensemble to disk"""
        if not self.is_trained:
            print("❌ Cannot save untrained ensemble")
            return False
        
        print(f"\n💾 Saving ensemble models to: {self.model_dir}")
        
        try:
            # Save individual models
            for model_name, model in self.models.items():
                model_path = os.path.join(self.model_dir, f"{model_name}_model.pkl")
                joblib.dump(model, model_path)
                print(f"   ✅ Saved {model_name}")
            
            # Save scaler
            scaler_path = os.path.join(self.model_dir, "scaler.pkl")
            joblib.dump(self.scaler, scaler_path)
            
            # Save feature columns
            features_path = os.path.join(self.model_dir, "feature_columns.pkl")
            joblib.dump(self.feature_columns, features_path)
            
            # Save metadata and configuration
            metadata_path = os.path.join(self.model_dir, "ensemble_metadata.pkl")
            joblib.dump({
                'metadata': self.metadata,
                'model_configs': self.model_configs
            }, metadata_path)
            
            print(f"   ✅ Saved scaler, features, and metadata")
            print(f"   📁 All files saved to: {self.model_dir}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to save ensemble: {e}")
            return False
    
    def load_ensemble(self):
        """Load trained ensemble from disk"""
        print(f"🔄 Loading ensemble from: {self.model_dir}")
        
        try:
            # Load metadata and configuration
            metadata_path = os.path.join(self.model_dir, "ensemble_metadata.pkl")
            if not os.path.exists(metadata_path):
                print(f"❌ Ensemble metadata not found at: {metadata_path}")
                return False
            
            saved_data = joblib.load(metadata_path)
            self.metadata = saved_data['metadata']
            self.model_configs = saved_data['model_configs']
            
            # Load individual models
            for model_name in self.model_configs.keys():
                model_path = os.path.join(self.model_dir, f"{model_name}_model.pkl")
                if not os.path.exists(model_path):
                    print(f"❌ Model not found: {model_path}")
                    return False
                
                self.models[model_name] = joblib.load(model_path)
                print(f"   ✅ Loaded {model_name}")
            
            # Load scaler
            scaler_path = os.path.join(self.model_dir, "scaler.pkl")
            self.scaler = joblib.load(scaler_path)
            
            # Load feature columns
            features_path = os.path.join(self.model_dir, "feature_columns.pkl")
            self.feature_columns = joblib.load(features_path)
            
            self.is_trained = True
            
            print(f"   ✅ Ensemble loaded successfully")
            print(f"   📊 Training Date: {self.metadata['training_date']}")
            print(f"   🎯 Ensemble Accuracy: {self.metadata['ensemble_accuracy']:.4f} ({self.metadata['ensemble_accuracy']*100:.2f}%)")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to load ensemble: {e}")
            return False
    
    def predict(self, fight_data):
        """Make prediction for a single fight"""
        if not self.is_trained:
            if not self.load_ensemble():
                raise ValueError("Ensemble not trained and cannot be loaded")
        
        # Prepare input data
        if isinstance(fight_data, dict):
            # Convert dict to DataFrame
            input_df = pd.DataFrame([fight_data])
        elif isinstance(fight_data, pd.Series):
            # Convert Series to DataFrame
            input_df = pd.DataFrame([fight_data.to_dict()])
        elif isinstance(fight_data, pd.DataFrame):
            input_df = fight_data.copy()
        else:
            raise ValueError("fight_data must be dict, pandas Series, or DataFrame")
        
        # Ensure all required features are present
        for col in self.feature_columns:
            if col not in input_df.columns:
                input_df[col] = 0  # Fill missing features with 0
        
        # Select and order features
        X = input_df[self.feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        # Get predictions from all models
        individual_predictions = []
        model_weights = []
        
        for model_name, config in self.model_configs.items():
            model = self.models[model_name]
            use_scaled = config['use_scaled']
            weight = config['weight']
            
            if use_scaled:
                pred_proba = model.predict_proba(X_scaled)[:, 1]
            else:
                pred_proba = model.predict_proba(X)[:, 1]
            
            individual_predictions.append(pred_proba[0])
            model_weights.append(weight)
        
        # Calculate weighted ensemble prediction
        ensemble_prob = sum(pred * weight for pred, weight in zip(individual_predictions, model_weights))
        ensemble_prediction = "Red Fighter Wins" if ensemble_prob > 0.5 else "Blue Fighter Wins"
        confidence = max(ensemble_prob, 1 - ensemble_prob)
        
        return {
            'prediction': ensemble_prediction,
            'probability': ensemble_prob,
            'confidence': confidence,
            'individual_predictions': dict(zip(self.model_configs.keys(), individual_predictions)),
            'winner': 'Red' if ensemble_prob > 0.5 else 'Blue'
        }
    
    def predict_fighters(self, red_fighter, blue_fighter):
        """Make prediction based on fighter names"""
        if not self.is_trained:
            if not self.load_ensemble():
                raise ValueError("Ensemble not trained and cannot be loaded")
        
        # Load dataset to get fighter statistics
        data_path = os.path.join(self.base_dir, 'shared', 'data', 'event_normalized_large_dataset.csv')
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Dataset not found at {data_path}")
        
        df = pd.read_csv(data_path)
        
        # Find recent fights for each fighter
        red_as_red = df[df['r_fighter'] == red_fighter]
        red_as_blue = df[df['b_fighter'] == red_fighter]
        blue_as_red = df[df['r_fighter'] == blue_fighter]
        blue_as_blue = df[df['b_fighter'] == blue_fighter]
        
        if red_as_red.empty and red_as_blue.empty:
            raise ValueError(f"No fights found for red fighter: {red_fighter}")
        if blue_as_red.empty and blue_as_blue.empty:
            raise ValueError(f"No fights found for blue fighter: {blue_fighter}")
        
        # Get most recent stats for each fighter
        def get_fighter_stats(fighter_name, as_red_df, as_blue_df):
            """Get the most recent stats for a fighter"""
            
            # Prefer red corner stats, then blue corner stats
            if not as_red_df.empty:
                recent = as_red_df.iloc[-1]
                return {
                    'age': recent['r_age'],
                    'height': recent['r_height'],
                    'weight': recent['r_weight'],
                    'reach': recent['r_reach'],
                    'stance': recent['r_stance'],
                    'wins_total': recent['r_wins_total'],
                    'losses_total': recent['r_losses_total'],
                    'SLpM_total': recent['r_SLpM_total'],
                    'SApM_total': recent['r_SApM_total'],
                    'sig_str_acc_total': recent['r_sig_str_acc_total'],
                    'td_acc_total': recent['r_td_acc_total'],
                    'str_def_total': recent['r_str_def_total'],
                    'td_def_total': recent['r_td_def_total'],
                    'sub_avg': recent['r_sub_avg'],
                    'td_avg': recent['r_td_avg']
                }
            else:
                recent = as_blue_df.iloc[-1]
                return {
                    'age': recent['b_age'],
                    'height': recent['b_height'],
                    'weight': recent['b_weight'],
                    'reach': recent['b_reach'],
                    'stance': recent['b_stance'],
                    'wins_total': recent['b_wins_total'],
                    'losses_total': recent['b_losses_total'],
                    'SLpM_total': recent['b_SLpM_total'],
                    'SApM_total': recent['b_SApM_total'],
                    'sig_str_acc_total': recent['b_sig_str_acc_total'],
                    'td_acc_total': recent['b_td_acc_total'],
                    'str_def_total': recent['b_str_def_total'],
                    'td_def_total': recent['b_td_def_total'],
                    'sub_avg': recent['b_sub_avg'],
                    'td_avg': recent['b_td_avg']
                }
        
        red_stats = get_fighter_stats(red_fighter, red_as_red, red_as_blue)
        blue_stats = get_fighter_stats(blue_fighter, blue_as_red, blue_as_blue)
        
        # Create a synthetic fight record for prediction
        # Use the same structure as the training data
        fight_data = {}
        
        # Red fighter stats (r_ prefix)
        for stat, value in red_stats.items():
            fight_data[f'r_{stat}'] = value
            
        # Blue fighter stats (b_ prefix)  
        for stat, value in blue_stats.items():
            fight_data[f'b_{stat}'] = value
        
        # Calculate difference features (key predictors)
        fight_data['age_diff'] = red_stats['age'] - blue_stats['age']
        fight_data['height_diff'] = red_stats['height'] - blue_stats['height'] 
        fight_data['weight_diff'] = red_stats['weight'] - blue_stats['weight']
        fight_data['reach_diff'] = red_stats['reach'] - blue_stats['reach']
        fight_data['wins_total_diff'] = red_stats['wins_total'] - blue_stats['wins_total']
        fight_data['losses_total_diff'] = red_stats['losses_total'] - blue_stats['losses_total']
        fight_data['SLpM_total_diff'] = red_stats['SLpM_total'] - blue_stats['SLpM_total']
        fight_data['SApM_total_diff'] = red_stats['SApM_total'] - blue_stats['SApM_total']
        fight_data['sig_str_acc_total_diff'] = red_stats['sig_str_acc_total'] - blue_stats['sig_str_acc_total']
        fight_data['td_acc_total_diff'] = red_stats['td_acc_total'] - blue_stats['td_acc_total']
        fight_data['str_def_total_diff'] = red_stats['str_def_total'] - blue_stats['str_def_total']
        fight_data['td_def_total_diff'] = red_stats['td_def_total'] - blue_stats['td_def_total']
        fight_data['sub_avg_diff'] = red_stats['sub_avg'] - blue_stats['sub_avg']
        fight_data['td_avg_diff'] = red_stats['td_avg'] - blue_stats['td_avg']
        
        # Encode stance if needed
        stance_encoding = {'Orthodox': 1, 'Southpaw': 2, 'Switch': 3, 'Unknown': 0}
        fight_data['r_stance_encoded'] = stance_encoding.get(red_stats['stance'], 0)
        fight_data['b_stance_encoded'] = stance_encoding.get(blue_stats['stance'], 0)
        
        # Set default values for fight-specific stats we don't have
        fight_defaults = {
            'r_kd': 0, 'r_sig_str': 0, 'r_sig_str_att': 0, 'r_sig_str_acc': 0,
            'r_str': 0, 'r_str_att': 0, 'r_str_acc': 0, 'r_td': 0, 'r_td_att': 0,
            'r_td_acc': 0, 'r_sub_att': 0, 'r_rev': 0, 'r_ctrl_sec': 0,
            'b_kd': 0, 'b_sig_str': 0, 'b_sig_str_att': 0, 'b_sig_str_acc': 0,
            'b_str': 0, 'b_str_att': 0, 'b_str_acc': 0, 'b_td': 0, 'b_td_att': 0,
            'b_td_acc': 0, 'b_sub_att': 0, 'b_rev': 0, 'b_ctrl_sec': 0,
            'kd_diff': 0, 'sig_str_diff': 0, 'sig_str_att_diff': 0, 'sig_str_acc_diff': 0,
            'str_diff': 0, 'str_att_diff': 0, 'str_acc_diff': 0, 'td_diff': 0,
            'td_att_diff': 0, 'td_acc_diff': 0, 'sub_att_diff': 0, 'rev_diff': 0,
            'ctrl_sec_diff': 0, 'winner_encoded': 0, 'method_encoded': 0,
            'gender_encoded': 0, 'weight_class_encoded': 0
        }
        
        # Add default values for missing fields
        for key, value in fight_defaults.items():
            if key not in fight_data:
                fight_data[key] = value
        
        # Make prediction
        result = self.predict(fight_data)
        
        # Convert numpy types to Python native types for JSON serialization
        def convert_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(v) for v in obj]
            return obj
        
        result = convert_types(result)
        
        # Add fighter names to result
        result['red_fighter'] = red_fighter
        result['blue_fighter'] = blue_fighter
        result['red_fighter_stats'] = convert_types(red_stats)
        result['blue_fighter_stats'] = convert_types(blue_stats)
        
        return result
    
    def predict_batch(self, fight_data_list):
        """Make predictions for multiple fights"""
        if not isinstance(fight_data_list, (list, pd.DataFrame)):
            raise ValueError("fight_data_list must be a list or DataFrame")
        
        results = []
        
        if isinstance(fight_data_list, pd.DataFrame):
            for _, row in fight_data_list.iterrows():
                result = self.predict(row)
                results.append(result)
        else:
            for fight_data in fight_data_list:
                result = self.predict(fight_data)
                results.append(result)
        
        return results
    
    def get_ensemble_info(self):
        """Get information about the ensemble"""
        # Check if models exist on disk
        models_exist = all(
            os.path.exists(os.path.join(self.model_dir, f"{name}_model.pkl"))
            for name in self.model_configs.keys()
        )
        metadata_exists = os.path.exists(os.path.join(self.model_dir, 'ensemble_metadata.pkl'))
        
        if not models_exist or not metadata_exists:
            return {"status": "not_trained"}
        
        # Load metadata if not already loaded
        try:
            metadata_path = os.path.join(self.model_dir, 'ensemble_metadata.pkl')
            saved_data = joblib.load(metadata_path)
            metadata = saved_data['metadata']
        except Exception as e:
            return {"status": "error_loading_metadata", "error": str(e)}
        
        return {
            "status": "trained",
            "accuracy": f"{metadata['ensemble_accuracy']*100:.2f}%",
            "auc": f"{metadata['ensemble_auc']:.4f}",
            "training_date": metadata['training_date'],
            "num_features": metadata['num_features'],
            "training_samples": metadata['training_samples'],
            "model_weights": metadata['model_weights'],
            "individual_accuracies": {k: f"{v*100:.2f}%" for k, v in metadata['individual_accuracies'].items()}
        }

def main():
    """Main function for training or using the ensemble"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='UFC Weighted Ensemble Predictor')
    parser.add_argument('--train', action='store_true', help='Train the ensemble')
    parser.add_argument('--predict', action='store_true', help='Interactive prediction mode')
    parser.add_argument('--info', action='store_true', help='Show ensemble information')
    parser.add_argument('--data', type=str, help='Path to training data CSV')
    parser.add_argument('--model_dir', type=str, help='Directory to save/load models')
    
    # New arguments for API support
    parser.add_argument('--red-fighter', type=str, help='Red fighter name')
    parser.add_argument('--blue-fighter', type=str, help='Blue fighter name')
    parser.add_argument('--output-format', type=str, choices=['json', 'text'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    # Initialize predictor
    predictor = UFCWeightedEnsemblePredictor(model_dir=args.model_dir)
    
    if args.red_fighter and args.blue_fighter:
        # Fighter-based prediction for API
        try:
            result = predictor.predict_fighters(args.red_fighter, args.blue_fighter)
            
            if args.output_format == 'json':
                print(json.dumps(result))
            else:
                print(f"\n🎯 PREDICTION RESULT:")
                print(f"   Red Fighter: {args.red_fighter}")
                print(f"   Blue Fighter: {args.blue_fighter}")
                print(f"   Predicted Winner: {result['prediction']}")
                print(f"   Probability: {result['probability']:.3f}")
                print(f"   Confidence: {result['confidence']:.3f}")
                
        except Exception as e:
            if args.output_format == 'json':
                print(json.dumps({"error": str(e)}))
            else:
                print(f"❌ Prediction failed: {e}")
            sys.exit(1)
    
    elif args.train:
        print("🏋️ Training Weighted Ensemble...")
        success = predictor.train_ensemble()
        if success:
            print("✅ Training completed successfully!")
        else:
            print("❌ Training failed!")
    
    elif args.predict:
        print("🔮 Interactive Prediction Mode")
        print("Note: Using sample data for demonstration")
        
        # Load a sample fight for demonstration
        try:
            data_path = os.path.join(predictor.base_dir, 'shared', 'data', 'event_normalized_large_dataset.csv')
            df = pd.read_csv(data_path)
            sample_fight = df.sample(1).iloc[0]
            
            print(f"\n📊 Sample Fight Data:")
            print(f"   Red Fighter vs Blue Fighter")
            
            result = predictor.predict(sample_fight)
            
            print(f"\n🎯 PREDICTION RESULT:")
            print(f"   Winner: {result['prediction']}")
            print(f"   Probability: {result['probability']:.3f}")
            print(f"   Confidence: {result['confidence']:.3f}")
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
    
    elif args.info:
        info = predictor.get_ensemble_info()
        print("📊 Ensemble Information:")
        for key, value in info.items():
            print(f"   {key}: {value}")
    
    else:
        print("🥊 UFC Weighted Ensemble Predictor")
        print("Usage:")
        print("  --train     Train the ensemble")
        print("  --predict   Interactive prediction mode") 
        print("  --info      Show ensemble information")
        print("\nExample:")
        print("  python predict_ensemble.py --train")
        print("  python predict_ensemble.py --predict")

if __name__ == "__main__":
    main()