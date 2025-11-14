"""
Simple ML Pipeline for UFC Fight Prediction (Headless Version)
Works with the event-normalized dataset - no plotting
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class EventNormalizedUFCPredictorHeadless:
    """UFC fight predictor using event-normalized data - no GUI plots"""
    
    def __init__(self, data_path='../../shared/data/event_normalized_large_dataset.csv', 
                 events_path='data/events_reference.csv'):
        self.data_path = data_path
        self.events_path = events_path
        self.models = {}
        self.best_model = None
        self.feature_columns = None
        self.label_encoder = LabelEncoder()
        
        # Create output directory
        self.model_dir = Path('models')
        self.model_dir.mkdir(exist_ok=True)
        
    def load_data(self):
        """Load the event-normalized dataset"""
        print("\n" + "="*60)
        print("LOADING EVENT-NORMALIZED DATA")
        print("="*60)
        
        print(f"Loading fights from: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        print(f"✓ Loaded {len(self.df)} fights")
        
        print(f"Loading events from: {self.events_path}")
        self.events_df = pd.read_csv(self.events_path)
        print(f"✓ Loaded {len(self.events_df)} unique events")
        print(f"✓ Total fight columns: {len(self.df.columns)}")
        
        # Show sample of event mapping
        print(f"\nSample event mappings:")
        for i in range(min(5, len(self.events_df))):
            event_id = self.events_df.iloc[i]['event_id']
            event_name = self.events_df.iloc[i]['event_name']
            fight_count = len(self.df[self.df['event_id'] == event_id])
            print(f"  ID {event_id}: {event_name} ({fight_count} fights)")
        
    def prepare_features(self):
        """Select and prepare features for training"""
        print("\n" + "="*60)
        print("PREPARING FEATURES")
        print("="*60)
        
        # Check for missing values
        missing_values = self.df.isnull().sum()
        if missing_values.any():
            print(f"⚠️  Found {missing_values.sum()} missing values")
            print("Missing values by column:")
            for col, count in missing_values[missing_values > 0].items():
                print(f"  - {col}: {count}")
        else:
            print("✓ No missing values found")
        
        # Select feature columns (exclude non-predictive columns and data leakage)
        excluded_cols = [
            'event_id',  # Event ID not used for prediction  
            'r_fighter', 'b_fighter',  # Fighter names
            'winner',  # Target variable - PRIMARY LEAKAGE
            'winner_encoded',  # Encoded target - DATA LEAKAGE!
            'method', 'method_encoded',  # Fight outcome method - DATA LEAKAGE!
            'finish_round', 'total_rounds', 'time_sec',  # Fight outcome details - DATA LEAKAGE!
            'referee',  # Not predictive
            'weight_class', 'gender',  # Categorical (use encoded versions)
            'r_stance', 'b_stance',  # Categorical (use encoded versions)
            'is_title_bout',  # Boolean that might need encoding
            # Fight stats that happen during the fight (potential leakage)
            'r_kd', 'b_kd', 'kd_diff',  # Knockdowns during fight
            'r_sig_str', 'b_sig_str', 'sig_str_diff',  # Significant strikes landed
            'r_sig_str_att', 'b_sig_str_att', 'sig_str_att_diff',  # Strike attempts
            'r_sig_str_acc', 'b_sig_str_acc', 'sig_str_acc_diff',  # Strike accuracy
            'r_str', 'b_str', 'str_diff',  # Total strikes
            'r_str_att', 'b_str_att', 'str_att_diff',  # Strike attempts
            'r_str_acc', 'b_str_acc', 'str_acc_diff',  # Strike accuracy
            'r_td', 'b_td', 'td_diff',  # Takedowns
            'r_td_att', 'b_td_att', 'td_att_diff',  # Takedown attempts
            'r_td_acc', 'b_td_acc', 'td_acc_diff',  # Takedown accuracy
            'r_sub_att', 'b_sub_att', 'sub_att_diff',  # Submission attempts
            'r_rev', 'b_rev', 'rev_diff',  # Reversals
            'r_ctrl_sec', 'b_ctrl_sec', 'ctrl_sec_diff',  # Control time
        ]
        
        self.feature_columns = [col for col in self.df.columns if col not in excluded_cols]
        
        print(f"✓ Selected {len(self.feature_columns)} features")
        print("Feature categories:")
        categories = {
            'Fight Stats': [c for c in self.feature_columns if any(stat in c for stat in ['kd', 'sig_str', 'str', 'td', 'sub', 'rev', 'ctrl'])],
            'Fighter Info': [c for c in self.feature_columns if any(info in c for info in ['age', 'height', 'weight', 'reach', 'wins', 'losses'])],
            'Performance': [c for c in self.feature_columns if any(perf in c for perf in ['SLpM', 'SApM', 'acc', 'def', 'avg'])],
            'Encoded': [c for c in self.feature_columns if 'encoded' in c],
            'Differences': [c for c in self.feature_columns if 'diff' in c]
        }
        
        for category, cols in categories.items():
            if cols:
                print(f"  - {category}: {len(cols)} features")
        
        # Prepare feature matrix and target
        X = self.df[self.feature_columns].copy()
        y = self.df['winner'].copy()
        
        # Handle any remaining missing values
        if X.isnull().any().any():
            print("⚠️  Filling remaining missing values with column medians")
            X = X.fillna(X.median())
        
        # Encode target variable
        y_encoded = self.label_encoder.fit_transform(y)
        
        print(f"✓ Target classes: {list(self.label_encoder.classes_)}")
        print(f"✓ Feature matrix shape: {X.shape}")
        print(f"✓ Target distribution:")
        target_counts = pd.Series(y).value_counts()
        for class_name, count in target_counts.items():
            print(f"   - {class_name}: {count} ({count/len(y)*100:.1f}%)")
        
        return X, y_encoded
    
    def train_models(self, X, y):
        """Train multiple models and find the best one"""
        print("\n" + "="*60)
        print("TRAINING MODELS")
        print("="*60)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"✓ Training set: {len(X_train)} samples")
        print(f"✓ Test set: {len(X_test)} samples")
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Store the scaler
        self.scaler = scaler
        
        # Model configurations
        model_configs = {
            'XGBoost': {
                'model': XGBClassifier(random_state=42, eval_metric='logloss'),
                'params': {
                    'max_depth': [3, 4],
                    'learning_rate': [0.1],
                    'n_estimators': [100]
                }
            },
            'Random Forest': {
                'model': RandomForestClassifier(random_state=42),
                'params': {
                    'n_estimators': [100],
                    'max_depth': [10],
                    'min_samples_split': [5]
                }
            }
        }
        
        best_score = 0
        results = []
        
        for name, config in model_configs.items():
            print(f"\nTraining {name}...")
            
            # Grid search for best parameters
            grid_search = GridSearchCV(
                config['model'], 
                config['params'],
                cv=3,
                scoring='accuracy',
                n_jobs=1,  # Use single job to avoid issues
                verbose=0
            )
            
            # Use original data for tree-based models
            grid_search.fit(X_train, y_train)
            y_pred = grid_search.best_estimator_.predict(X_test)
            
            # Calculate accuracy
            accuracy = accuracy_score(y_test, y_pred)
            results.append({
                'Model': name,
                'Accuracy': accuracy,
                'Best_Params': grid_search.best_params_
            })
            
            # Store the model
            self.models[name] = grid_search.best_estimator_
            
            print(f"✓ {name}: {accuracy:.4f} accuracy")
            print(f"  Best params: {grid_search.best_params_}")
            
            # Track best model
            if accuracy > best_score:
                best_score = accuracy
                self.best_model = grid_search.best_estimator_
                self.best_model_name = name
                
        # Store test data for evaluation
        self.X_test = X_test
        self.y_test = y_test
        
        print(f"\n🏆 Best model: {self.best_model_name} ({best_score:.4f} accuracy)")
        
        return results
    
    def evaluate_model(self):
        """Evaluate the best model in detail"""
        print("\n" + "="*60)
        print(f"EVALUATING BEST MODEL ({self.best_model_name})")
        print("="*60)
        
        y_pred = self.best_model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        
        print(f"Test Accuracy: {accuracy:.4f}")
        print(f"Test Accuracy: {accuracy*100:.2f}%")
        
        # Classification report
        print("\nClassification Report:")
        class_names = self.label_encoder.classes_
        print(classification_report(self.y_test, y_pred, 
                                  target_names=class_names))
        
        # Confusion matrix (text only)
        cm = confusion_matrix(self.y_test, y_pred)
        print(f"\nConfusion Matrix:")
        print(f"                Predicted")
        print(f"Actual    {'Blue':>6}  {'Red':>6}")
        print(f"Blue      {cm[0][0]:>6}  {cm[0][1]:>6}")
        print(f"Red       {cm[1][0]:>6}  {cm[1][1]:>6}")
        
        # Feature importance (for tree-based models)
        if hasattr(self.best_model, 'feature_importances_'):
            self.show_feature_importance()
            
        return accuracy
    
    def show_feature_importance(self, top_n=10):
        """Show feature importance for the best model (text only)"""
        if not hasattr(self.best_model, 'feature_importances_'):
            print("Model doesn't support feature importance")
            return
            
        # Get feature importances
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\nTop {min(top_n, len(importance_df))} most important features:")
        for i, row in importance_df.head(top_n).iterrows():
            print(f"  {row['feature']:30}: {row['importance']:.4f}")
    
    def save_model(self):
        """Save the best model and necessary components"""
        print("\n" + "="*60)
        print("SAVING MODEL")
        print("="*60)
        
        # Save the best model
        model_path = self.model_dir / 'event_normalized_best_model.pkl'
        joblib.dump(self.best_model, model_path)
        print(f"✓ Model saved to: {model_path}")
        
        # Save the scaler
        scaler_path = self.model_dir / 'event_normalized_scaler.pkl'
        joblib.dump(self.scaler, scaler_path)
        print(f"✓ Scaler saved to: {scaler_path}")
        
        # Save label encoder
        encoder_path = self.model_dir / 'event_normalized_label_encoder.pkl'
        joblib.dump(self.label_encoder, encoder_path)
        print(f"✓ Label encoder saved to: {encoder_path}")
        
        # Save feature columns
        features_path = self.model_dir / 'event_normalized_features.pkl'
        joblib.dump(self.feature_columns, features_path)
        print(f"✓ Feature list saved to: {features_path}")
        
        return model_path
    
    def run_full_pipeline(self):
        """Run the complete training pipeline"""
        print("🥊 EVENT-NORMALIZED UFC FIGHT PREDICTOR (HEADLESS)")
        print("=" * 60)
        
        # Load data
        self.load_data()
        
        # Prepare features
        X, y = self.prepare_features()
        
        # Train models
        results = self.train_models(X, y)
        
        # Evaluate best model
        accuracy = self.evaluate_model()
        
        # Save model
        model_path = self.save_model()
        
        print("\n" + "="*60)
        print("TRAINING COMPLETE!")
        print("="*60)
        print(f"🏆 Best Model: {self.best_model_name}")
        print(f"🎯 Final Accuracy: {accuracy*100:.2f}%")
        print(f"💾 Model saved to: {model_path}")
        print(f"📊 Trained on {len(self.df)} fights from {len(self.events_df)} events")
        print("="*60)
        
        return self.best_model, accuracy


def main():
    """Main training script"""
    # Initialize predictor with event-normalized data
    predictor = EventNormalizedUFCPredictorHeadless()
    
    # Run the full pipeline
    model, accuracy = predictor.run_full_pipeline()
    
    print(f"\nTraining completed successfully!")
    print(f"Final model accuracy: {accuracy*100:.2f}%")


if __name__ == "__main__":
    main()