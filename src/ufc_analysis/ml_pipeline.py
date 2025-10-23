"""
Complete ML Pipeline for UFC Fight Prediction

This module implements a full machine learning pipeline from normalized data
to trained models, including feature engineering, model training, evaluation,
and prediction.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import joblib
from pathlib import Path
import warnings
import sys
warnings.filterwarnings('ignore')

# Add scripts directory to path to import normalizer
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))

class UFCMLPipeline:
    """
    Complete ML pipeline for UFC fight outcome prediction.
    """
    
    def __init__(self, data_path='data/normalized_large_dataset.csv'):
        self.data_path = data_path
        self.models = {}
        self.best_model = None
        self.feature_names = None
        self.scaler = StandardScaler()
        self.df = None
        
    def load_and_prepare_data(self):
        """
        Load normalized data for ML training.
        """
        print("="*60)
        print("STEP 1: Loading Normalized Data")
        print("="*60)
        
        # Load the already-normalized dataset
        print(f"Loading data from {self.data_path}...")
        self.df = pd.read_csv(self.data_path)
        
        print(f"✓ Loaded {len(self.df)} fights with {len(self.df.columns)} columns")
        
        # Check for winner column
        if 'winner' not in self.df.columns:
            raise ValueError("Dataset must contain 'winner' column for training")
        
    def create_features(self):
        """
        Create ML-ready features (pre-fight information only).
        """
        print("\n" + "="*60)
        print("STEP 2: Feature Engineering")
        print("="*60)
        
        features = pd.DataFrame()
        
        # Win rate features
        features['r_win_rate'] = self.df['r_win_rate']
        features['b_win_rate'] = self.df['b_win_rate']
        features['win_rate_diff'] = self.df['win_rate_diff']
        
        # Experience features
        features['r_total_fights'] = self.df['r_total_fights']
        features['b_total_fights'] = self.df['b_total_fights']
        features['experience_diff'] = self.df['experience_diff']
        
        # Physical features
        features['height_diff'] = self.df['height_diff']
        features['weight_diff'] = self.df['weight_diff']
        features['reach_diff'] = self.df['reach_diff']
        features['age_diff'] = self.df['age_diff']
        features['bmi_diff'] = self.df['bmi_diff']
        
        # Striking features
        features['r_SLpM_total'] = self.df['r_SLpM_total']
        features['b_SLpM_total'] = self.df['b_SLpM_total']
        features['r_sig_str_acc_total'] = self.df['r_sig_str_acc_total']
        features['b_sig_str_acc_total'] = self.df['b_sig_str_acc_total']
        features['striking_efficiency_diff'] = self.df['striking_efficiency_diff']
        
        # Grappling features
        features['r_td_avg'] = self.df['r_td_avg']
        features['b_td_avg'] = self.df['b_td_avg']
        features['r_td_acc_total'] = self.df['r_td_acc_total']
        features['b_td_acc_total'] = self.df['b_td_acc_total']
        features['grappling_efficiency_diff'] = self.df['grappling_efficiency_diff']
        
        # Defensive features
        features['r_str_def_total'] = self.df['r_str_def_total']
        features['b_str_def_total'] = self.df['b_str_def_total']
        features['r_td_def_total'] = self.df['r_td_def_total']
        features['b_td_def_total'] = self.df['b_td_def_total']
        features['defensive_rating_diff'] = self.df['defensive_rating_diff']
        
        # Submission features
        features['r_sub_avg'] = self.df['r_sub_avg']
        features['b_sub_avg'] = self.df['b_sub_avg']
        
        # Categorical features (one-hot encode)
        features['is_title_bout'] = self.df['is_title_bout']
        
        # Encode stances
        stance_dummies_r = pd.get_dummies(self.df['r_stance'], prefix='r_stance')
        stance_dummies_b = pd.get_dummies(self.df['b_stance'], prefix='b_stance')
        features = pd.concat([features, stance_dummies_r, stance_dummies_b], axis=1)
        
        # Handle any remaining NaN values
        features = features.fillna(features.median())
        
        self.feature_names = features.columns.tolist()
        print(f"Created {len(self.feature_names)} features")
        print(f"Feature categories: Physical, Performance, Style, Experience")
        
        return features
    
    def create_target(self, target_type='winner'):
        """
        Create target variable.
        
        Args:
            target_type: 'winner', 'method', or 'rounds'
        """
        if target_type == 'winner':
            # Binary: Red wins (1) or Blue wins (0)
            target = (self.df['winner'] == 'Red').astype(int)
        elif target_type == 'method':
            # Multi-class: KO/TKO, Submission, Decision
            target = self.df['method']
        elif target_type == 'rounds':
            # Regression: Number of rounds
            target = self.df['finish_round']
        
        return target
    
    def split_data(self, test_size=0.2, random_state=42):
        """
        Split data into train and test sets.
        """
        print("\n" + "="*60)
        print("STEP 3: Splitting Data")
        print("="*60)
        
        X = self.create_features()
        y = self.create_target('winner')
        
        # Stratified split to maintain class balance
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        # Convert back to DataFrame for feature names
        self.X_train_scaled = pd.DataFrame(
            self.X_train_scaled, 
            columns=self.feature_names,
            index=self.X_train.index
        )
        self.X_test_scaled = pd.DataFrame(
            self.X_test_scaled, 
            columns=self.feature_names,
            index=self.X_test.index
        )
        
        print(f"Training set: {len(self.X_train)} samples")
        print(f"Test set: {len(self.X_test)} samples")
        print(f"Red wins in training: {self.y_train.mean():.2%}")
        print(f"Red wins in test: {self.y_test.mean():.2%}")
        
    def train_baseline_models(self):
        """
        Train multiple baseline models.
        """
        print("\n" + "="*60)
        print("STEP 4: Training Baseline Models")
        print("="*60)
        
        # Logistic Regression
        print("\nTraining Logistic Regression...")
        self.models['logistic'] = LogisticRegression(max_iter=1000, random_state=42)
        self.models['logistic'].fit(self.X_train_scaled, self.y_train)
        
        # Random Forest
        print("Training Random Forest...")
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=100, 
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.models['random_forest'].fit(self.X_train_scaled, self.y_train)
        
        # XGBoost
        print("Training XGBoost...")
        self.models['xgboost'] = XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
        self.models['xgboost'].fit(self.X_train_scaled, self.y_train)
        
        print("\nBaseline models trained successfully!")
        
    def evaluate_models(self):
        """
        Evaluate all trained models.
        """
        print("\n" + "="*60)
        print("STEP 5: Model Evaluation")
        print("="*60)
        
        results = {}
        
        for name, model in self.models.items():
            # Predictions
            y_pred = model.predict(self.X_test_scaled)
            y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
            
            # Metrics
            accuracy = accuracy_score(self.y_test, y_pred)
            roc_auc = roc_auc_score(self.y_test, y_pred_proba)
            
            results[name] = {
                'accuracy': accuracy,
                'roc_auc': roc_auc,
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }
            
            print(f"\n{name.upper()}:")
            print(f"  Accuracy: {accuracy:.4f}")
            print(f"  ROC-AUC:  {roc_auc:.4f}")
            print("\nClassification Report:")
            print(classification_report(self.y_test, y_pred, 
                                       target_names=['Blue Wins', 'Red Wins']))
        
        # Find best model
        best_model_name = max(results, key=lambda x: results[x]['accuracy'])
        self.best_model = self.models[best_model_name]
        print(f"\n{'='*60}")
        print(f"BEST MODEL: {best_model_name.upper()}")
        print(f"Accuracy: {results[best_model_name]['accuracy']:.4f}")
        print(f"{'='*60}")
        
        return results
    
    def tune_hyperparameters(self):
        """
        Perform hyperparameter tuning on XGBoost.
        """
        print("\n" + "="*60)
        print("STEP 6: Hyperparameter Tuning (XGBoost)")
        print("="*60)
        
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.05, 0.1],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0]
        }
        
        print("Running Grid Search (this may take a while)...")
        grid_search = GridSearchCV(
            XGBClassifier(random_state=42, eval_metric='logloss'),
            param_grid,
            cv=5,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(self.X_train_scaled, self.y_train)
        
        print(f"\nBest parameters: {grid_search.best_params_}")
        print(f"Best CV score: {grid_search.best_score_:.4f}")
        
        self.models['xgboost_tuned'] = grid_search.best_estimator_
        self.best_model = grid_search.best_estimator_
        
    def analyze_feature_importance(self):
        """
        Analyze feature importance using SHAP.
        """
        print("\n" + "="*60)
        print("STEP 7: Feature Importance Analysis")
        print("="*60)
        
        # Use the best model
        model = self.best_model
        
        # Get feature importance
        if hasattr(model, 'feature_importances_'):
            importances = pd.DataFrame({
                'feature': self.feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\nTop 15 Most Important Features:")
            print(importances.head(15).to_string(index=False))
            
            # Plot
            plt.figure(figsize=(12, 8))
            sns.barplot(data=importances.head(15), x='importance', y='feature')
            plt.title('Top 15 Feature Importances')
            plt.tight_layout()
            plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
            print("\nFeature importance plot saved as 'feature_importance.png'")
        
        # SHAP analysis
        print("\nCalculating SHAP values...")
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(self.X_test_scaled)
        
        # SHAP summary plot
        plt.figure(figsize=(12, 8))
        shap.summary_plot(shap_values, self.X_test_scaled, show=False)
        plt.tight_layout()
        plt.savefig('shap_summary.png', dpi=300, bbox_inches='tight')
        print("SHAP summary plot saved as 'shap_summary.png'")
        plt.close()
        
    def save_models(self, output_dir='models'):
        """
        Save trained models to disk.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        for name, model in self.models.items():
            model_path = output_dir / f'{name}_model.pkl'
            joblib.dump(model, model_path)
            print(f"Saved {name} to {model_path}")
        
        # Save scaler
        scaler_path = output_dir / 'scaler.pkl'
        joblib.dump(self.scaler, scaler_path)
        print(f"Saved scaler to {scaler_path}")
    
    def predict_fight(self, fighter_red, fighter_blue):
        """
        Predict outcome of a specific fight.
        
        Args:
            fighter_red: dict with fighter stats
            fighter_blue: dict with fighter stats
        """
        # Create feature vector
        # This would need the actual fighter stats
        pass
    
    def run_full_pipeline(self):
        """
        Run the complete ML pipeline.
        """
        print("\n" + "🥊" * 30)
        print("UFC FIGHT PREDICTION - FULL ML PIPELINE")
        print("🥊" * 30 + "\n")
        
        # Step 1-3: Load, prepare, split
        self.load_and_prepare_data()
        self.split_data()
        
        # Step 4-5: Train and evaluate
        self.train_baseline_models()
        results = self.evaluate_models()
        
        # Step 6: Tune best model
        self.tune_hyperparameters()
        
        # Step 7: Analyze
        self.analyze_feature_importance()
        
        # Save models
        self.save_models()
        
        print("\n" + "="*60)
        print("PIPELINE COMPLETE!")
        print("="*60)
        print("\nOutputs:")
        print("  - Trained models saved in 'models/' directory")
        print("  - Feature importance plot: feature_importance.png")
        print("  - SHAP analysis: shap_summary.png")
        
        return results

def main():
    # Initialize pipeline
    pipeline = UFCMLPipeline()
    
    # Run complete pipeline
    results = pipeline.run_full_pipeline()

if __name__ == '__main__':
    main()