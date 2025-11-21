"""
Simple ML Pipeline for Fight Prediction
Works directly with the normalized large_dataset.csv
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class SimpleFightPredictor:
    """Simple but effective fight predictor"""
    
    def __init__(self, data_path='data/UFC dataset/Large set/large_dataset.csv'):
        self.data_path = data_path
        self.models = {}
        self.best_model = None
        self.feature_columns = None
        self.label_encoder = LabelEncoder()
        
        # Create output directory
        self.model_dir = Path('models')
        self.model_dir.mkdir(exist_ok=True)
        
    def load_data(self):
        """Load the dataset"""
        print("\n" + "="*60)
        print("LOADING DATA")
        print("="*60)
        
        print(f"Loading from: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        print(f"✓ Loaded {len(self.df)} fights")
        print(f"✓ Total columns: {len(self.df.columns)}")
        
    def prepare_features(self):
        """Select and prepare features for training"""
        print("\n" + "="*60)
        print("PREPARING FEATURES")
        print("="*60)
        
        # Select numerical features that are available pre-fight
        feature_cols = []
        
        # Red corner fighter stats
        red_features = [
            'r_wins_total', 'r_losses_total',
            'r_height', 'r_weight', 'r_reach', 'r_age',
            'r_SLpM_total', 'r_sig_str_acc_total', 'r_SApM_total', 'r_str_def_total',
            'r_td_avg', 'r_td_acc_total', 'r_td_def_total', 'r_sub_avg'
        ]
        
        # Blue corner fighter stats
        blue_features = [
            'b_wins_total', 'b_losses_total',
            'b_height', 'b_weight', 'b_reach', 'b_age',
            'b_SLpM_total', 'b_sig_str_acc_total', 'b_SApM_total', 'b_str_def_total',
            'b_td_avg', 'b_td_acc_total', 'b_td_def_total', 'b_sub_avg'
        ]
        
        # Only use columns that exist
        for col in red_features + blue_features:
            if col in self.df.columns:
                feature_cols.append(col)
        
        print(f"✓ Selected {len(feature_cols)} features")
        
        # Create feature matrix
        X = self.df[feature_cols].copy()
        
        # Handle missing values
        print("✓ Handling missing values...")
        X = X.fillna(X.median())
        
        # Create engineered features
        print("✓ Engineering additional features...")
        
        # Win rates
        X['r_win_rate'] = X['r_wins_total'] / (X['r_wins_total'] + X['r_losses_total'] + 0.01)
        X['b_win_rate'] = X['b_wins_total'] / (X['b_wins_total'] + X['b_losses_total'] + 0.01)
        X['win_rate_diff'] = X['r_win_rate'] - X['b_win_rate']
        
        # Experience
        X['r_fights'] = X['r_wins_total'] + X['r_losses_total']
        X['b_fights'] = X['b_wins_total'] + X['b_losses_total']
        X['experience_diff'] = X['r_fights'] - X['b_fights']
        
        # Physical differences
        X['height_diff'] = X['r_height'] - X['b_height']
        X['weight_diff'] = X['r_weight'] - X['b_weight']
        X['reach_diff'] = X['r_reach'] - X['b_reach']
        X['age_diff'] = X['r_age'] - X['b_age']
        
        # Striking differences
        X['SLpM_diff'] = X['r_SLpM_total'] - X['b_SLpM_total']
        X['sig_str_acc_diff'] = X['r_sig_str_acc_total'] - X['b_sig_str_acc_total']
        X['SApM_diff'] = X['r_SApM_total'] - X['b_SApM_total']
        X['str_def_diff'] = X['r_str_def_total'] - X['b_str_def_total']
        
        # Grappling differences
        X['td_avg_diff'] = X['r_td_avg'] - X['b_td_avg']
        X['td_acc_diff'] = X['r_td_acc_total'] - X['b_td_acc_total']
        X['td_def_diff'] = X['r_td_def_total'] - X['b_td_def_total']
        X['sub_avg_diff'] = X['r_sub_avg'] - X['b_sub_avg']
        
        # Prepare target
        y = self.label_encoder.fit_transform(self.df['winner'])
        
        print(f"✓ Final feature set: {X.shape[1]} features")
        print(f"✓ Target classes: {list(self.label_encoder.classes_)}")
        
        self.feature_columns = X.columns.tolist()
        
        return X, y
    
    def split_data(self, X, y, test_size=0.2):
        """Split into train and test sets"""
        print("\n" + "="*60)
        print("SPLITTING DATA")
        print("="*60)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"✓ Training set: {len(X_train)} fights")
        print(f"✓ Test set: {len(X_test)} fights")
        
        return X_train, X_test, y_train, y_test
    
    def train_models(self, X_train, y_train):
        """Train multiple models"""
        print("\n" + "="*60)
        print("TRAINING MODELS")
        print("="*60)
        
        # 1. Logistic Regression
        print("\n1. Training Logistic Regression...")
        lr = LogisticRegression(max_iter=1000, random_state=42)
        lr.fit(X_train, y_train)
        self.models['Logistic Regression'] = lr
        print("   ✓ Complete")
        
        # 2. Random Forest
        print("\n2. Training Random Forest...")
        rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        rf.fit(X_train, y_train)
        self.models['Random Forest'] = rf
        print("   ✓ Complete")
        
        # 3. XGBoost
        print("\n3. Training XGBoost...")
        xgb = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1)
        xgb.fit(X_train, y_train)
        self.models['XGBoost'] = xgb
        print("   ✓ Complete")
        
    def evaluate_models(self, X_test, y_test):
        """Evaluate all models"""
        print("\n" + "="*60)
        print("EVALUATING MODELS")
        print("="*60)
        
        results = {}
        best_acc = 0
        
        for name, model in self.models.items():
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            results[name] = acc
            
            print(f"\n{name}:")
            print(f"  Accuracy: {acc:.4f}")
            
            if acc > best_acc:
                best_acc = acc
                self.best_model = model
                self.best_model_name = name
        
        print(f"\n{'='*60}")
        print(f"🏆 Best Model: {self.best_model_name} ({best_acc:.4f})")
        print(f"{'='*60}")
        
        return results
    
    def show_feature_importance(self, top_n=20):
        """Show feature importance for best model"""
        print("\n" + "="*60)
        print("FEATURE IMPORTANCE (Top 20)")
        print("="*60)
        
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            indices = np.argsort(importances)[::-1][:top_n]
            
            plt.figure(figsize=(10, 8))
            plt.barh(range(top_n), importances[indices], color='steelblue', edgecolor='black')
            plt.yticks(range(top_n), [self.feature_columns[i] for i in indices])
            plt.xlabel('Importance')
            plt.title(f'Top {top_n} Feature Importances - {self.best_model_name}')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(self.model_dir / 'feature_importance.png', dpi=300, bbox_inches='tight')
            print(f"✓ Saved feature importance plot")
            plt.close()
            
            # Print top features
            print("\nTop 10 Features:")
            for i, idx in enumerate(indices[:10], 1):
                print(f"  {i}. {self.feature_columns[idx]}: {importances[idx]:.4f}")
    
    def save_model(self):
        """Save the best model"""
        print("\n" + "="*60)
        print("SAVING MODEL")
        print("="*60)
        
        model_path = self.model_dir / 'best_model.pkl'
        
        # Save model and metadata
        joblib.dump({
            'model': self.best_model,
            'model_name': self.best_model_name,
            'feature_columns': self.feature_columns,
            'label_encoder': self.label_encoder
        }, model_path)
        
        print(f"✓ Saved model to: {model_path}")
        
        # Save feature list
        feature_list_path = self.model_dir / 'features.txt'
        with open(feature_list_path, 'w') as f:
            for feature in self.feature_columns:
                f.write(f"{feature}\n")
        print(f"✓ Saved feature list to: {feature_list_path}")
    
    def run_pipeline(self):
        """Run the complete pipeline"""
        print("\n" + "🥊"*30)
        print("FIGHT PREDICTION - ML PIPELINE")
        print("🥊"*30)
        
        # Load data
        self.load_data()
        
        # Prepare features
        X, y = self.prepare_features()
        
        # Split data
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        
        # Train models
        self.train_models(X_train, y_train)
        
        # Evaluate models
        results = self.evaluate_models(X_test, y_test)
        
        # Feature importance
        self.show_feature_importance()
        
        # Save model
        self.save_model()
        
        print("\n" + "="*60)
        print("✅ PIPELINE COMPLETE!")
        print("="*60)
        print(f"\nYou can now use 'predict_fight.py' to predict fights!")
        print(f"The trained model is saved in: {self.model_dir}/best_model.pkl")
        
        return results


if __name__ == '__main__':
    pipeline = SimpleFightPredictor()
    pipeline.run_pipeline()
