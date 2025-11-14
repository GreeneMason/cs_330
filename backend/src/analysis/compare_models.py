"""
Model Comparison Framework
Compare Neural Network vs Ensemble Models on Identical Test Sets
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'training'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from train_neural_network_hypertuned import HyperparameterTunedNeuralNetwork

class ModelComparison:
    def __init__(self):
        # Use absolute paths relative to the script location
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, 'shared', 'data', 'event_normalized_large_dataset.csv')
        events_path = os.path.join(base_dir, 'data', 'events_reference.csv')
        
        self.neural_net = HyperparameterTunedNeuralNetwork(data_path=data_path, events_path=events_path)
        self.test_results = {}
    
    def compare_models(self):
        """Compare neural network vs baseline models on identical test set"""
        print("🔄 Loading data and preparing test set...")
        
        # Load and prepare data
        self.neural_net.load_data()
        X, y = self.neural_net.prepare_features()
        
        print(f"📊 Dataset: {X.shape[0]} fights with {X.shape[1]} features")
        
        # Create identical train/test split with fixed random state
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"📈 Test set: {len(X_test)} fights")
        print(f"   Red wins: {sum(y_test)} ({sum(y_test)/len(y_test)*100:.1f}%)")
        print(f"   Blue wins: {len(y_test)-sum(y_test)} ({(len(y_test)-sum(y_test))/len(y_test)*100:.1f}%)")
        
        print("\n🧠 Testing Neural Network...")
        nn_predictions = self.test_neural_network(X_test, y_test)
        
        print("\n🌲 Testing Baseline Models...")
        baseline_predictions = self.test_baseline_models(X_train, X_test, y_train, y_test)
        
        print("\n📊 Generating Comparison Report...")
        self.generate_comparison_report(y_test)
        
        return self.test_results
    
    def test_neural_network(self, X_test, y_test):
        """Test neural network model"""
        try:
            # Try to load saved model first
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, 'models', 'neural_network', 'best_tuned_neural_network_model.h5')
            
            if os.path.exists(model_path):
                import tensorflow as tf
                model = tf.keras.models.load_model(model_path)
                print("   ✅ Loaded saved neural network model")
                
                # Make predictions
                predictions = model.predict(X_test, verbose=0)
                pred_binary = (predictions > 0.5).astype(int).flatten()
                
                accuracy = accuracy_score(y_test, pred_binary)
                auc = roc_auc_score(y_test, predictions)
                
                print(f"   📊 Neural Network Results:")
                print(f"      Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
                print(f"      AUC: {auc:.4f}")
                
                self.test_results['neural_network'] = {
                    'accuracy': accuracy,
                    'auc': auc,
                    'predictions': predictions.flatten(),
                    'predictions_binary': pred_binary
                }
                
                return predictions
            else:
                # Try to manually run hyperparameter tuning
                print("   ⚠️  No saved model found, attempting to retrain...")
                print("   🔄 This may take several minutes...")
                
                # Run hyperparameter tuning manually
                tuning_method = getattr(self.neural_net, 'tune_hyperparameters', None)
                if tuning_method:
                    tuning_method()
                    model = self.neural_net.best_model
                else:
                    print("   ❌ Cannot access neural network training methods")
                    return None
                    
                if model is None:
                    print("   ❌ Neural network training failed")
                    return None
                    
                # Make predictions with newly trained model
                predictions = model.predict(X_test, verbose=0)
                pred_binary = (predictions > 0.5).astype(int).flatten()
                
                accuracy = accuracy_score(y_test, pred_binary)
                auc = roc_auc_score(y_test, predictions)
                
                print(f"   📊 Neural Network Results:")
                print(f"      Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
                print(f"      AUC: {auc:.4f}")
                
                self.test_results['neural_network'] = {
                    'accuracy': accuracy,
                    'auc': auc,
                    'predictions': predictions.flatten(),
                    'predictions_binary': pred_binary
                }
                
                return predictions
            
        except Exception as e:
            print(f"   ❌ Neural network test failed: {e}")
            print("   ℹ️  Continuing with baseline model comparison only...")
            return None
    
    def test_baseline_models(self, X_train, X_test, y_train, y_test):
        """Test baseline models for comparison"""
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        
        # Test multiple baseline models
        baseline_models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(random_state=42),
            'logistic_regression': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        # Scale features for logistic regression
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        for model_name, model in baseline_models.items():
            try:
                print(f"   🔄 Training {model_name.replace('_', ' ').title()}...")
                
                # Use scaled features for logistic regression, original for tree-based
                if model_name == 'logistic_regression':
                    model.fit(X_train_scaled, y_train)
                    predictions = model.predict_proba(X_test_scaled)[:, 1]
                else:
                    model.fit(X_train, y_train)
                    predictions = model.predict_proba(X_test)[:, 1]
                
                pred_binary = (predictions > 0.5).astype(int)
                accuracy = accuracy_score(y_test, pred_binary)
                auc = roc_auc_score(y_test, predictions)
                
                print(f"      Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
                print(f"      AUC: {auc:.4f}")
                
                self.test_results[model_name] = {
                    'accuracy': accuracy,
                    'auc': auc,
                    'predictions': predictions,
                    'predictions_binary': pred_binary
                }
                
            except Exception as e:
                print(f"   ❌ {model_name} failed: {e}")
        
        return self.test_results
    
    def generate_comparison_report(self, y_test):
        """Generate comprehensive comparison report"""
        
        print("\n" + "="*80)
        print("🏆 MODEL COMPARISON RESULTS")
        print("="*80)
        
        if 'neural_network' not in self.test_results:
            print("❌ Neural network results not available")
            return
        
        # Get neural network results
        nn_results = self.test_results['neural_network']
        
        print(f"\n🧠 NEURAL NETWORK (Fighter-Aware Architecture):")
        print(f"   Accuracy: {nn_results['accuracy']:.4f} ({nn_results['accuracy']*100:.2f}%)")
        print(f"   AUC: {nn_results['auc']:.4f}")
        
        # Compare with baseline models
        print(f"\n📊 BASELINE MODEL COMPARISON:")
        
        baseline_results = []
        for model_name, results in self.test_results.items():
            if model_name != 'neural_network':
                baseline_results.append((model_name, results))
                print(f"   {model_name.replace('_', ' ').title()}:")
                print(f"      Accuracy: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
                print(f"      AUC: {results['auc']:.4f}")
        
        # Find best baseline
        if baseline_results:
            best_baseline_name, best_baseline = max(baseline_results, key=lambda x: x[1]['accuracy'])
            
            print(f"\n🥇 PERFORMANCE SUMMARY:")
            print(f"   Neural Network:  {nn_results['accuracy']*100:.2f}% accuracy")
            print(f"   Best Baseline:   {best_baseline['accuracy']*100:.2f}% accuracy ({best_baseline_name.replace('_', ' ').title()})")
            
            improvement = (nn_results['accuracy'] - best_baseline['accuracy']) * 100
            if improvement > 0:
                print(f"   🚀 Neural Network Advantage: +{improvement:.2f}% accuracy")
                print(f"   📈 Relative Improvement: {(improvement/best_baseline['accuracy']/100)*100:.1f}%")
            else:
                print(f"   ⚠️  Best Baseline Better: {abs(improvement):.2f}% accuracy")
        
        # Generate Visualizations
        try:
            self.create_comparison_plots(y_test)
        except Exception as e:
            print(f"⚠️  Visualization failed: {e}")
    
    def create_comparison_plots(self, y_test):
        """Create comparison visualizations"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Neural Network vs Baseline Models Comparison', fontsize=16, fontweight='bold')
        
        # ROC Curves
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
        
        for i, (model_name, results) in enumerate(self.test_results.items()):
            fpr, tpr, _ = roc_curve(y_test, results['predictions'])
            axes[0,0].plot(fpr, tpr, 
                          label=f'{model_name.replace("_", " ").title()} (AUC: {results["auc"]:.3f})',
                          color=colors[i % len(colors)], linewidth=2)
        
        axes[0,0].plot([0,1], [0,1], 'k--', alpha=0.5)
        axes[0,0].set_xlabel('False Positive Rate')
        axes[0,0].set_ylabel('True Positive Rate')
        axes[0,0].set_title('ROC Curve Comparison')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # Accuracy Comparison Bar Chart
        model_names = [name.replace('_', ' ').title() for name in self.test_results.keys()]
        accuracies = [results['accuracy'] for results in self.test_results.values()]
        
        bars = axes[0,1].bar(model_names, accuracies, color=colors[:len(model_names)], alpha=0.8)
        axes[0,1].set_ylabel('Accuracy')
        axes[0,1].set_title('Accuracy Comparison')
        axes[0,1].set_ylim(min(accuracies) - 0.02, max(accuracies) + 0.02)
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, acc in zip(bars, accuracies):
            height = bar.get_height()
            axes[0,1].text(bar.get_x() + bar.get_width()/2., height + 0.002,
                          f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Neural Network Prediction Distribution
        if 'neural_network' in self.test_results:
            nn_preds = self.test_results['neural_network']['predictions']
            axes[1,0].hist(nn_preds, alpha=0.7, bins=30, color='#FF6B6B', edgecolor='black')
            axes[1,0].set_xlabel('Neural Network Prediction Probability')
            axes[1,0].set_ylabel('Frequency')
            axes[1,0].set_title('Neural Network Prediction Distribution')
            axes[1,0].axvline(0.5, color='red', linestyle='--', alpha=0.7, label='Decision Threshold')
            axes[1,0].legend()
        
        # Model Performance Summary
        if len(self.test_results) > 1:
            model_names_short = [name.replace('_', '\n') for name in self.test_results.keys()]
            auc_scores = [results['auc'] for results in self.test_results.values()]
            
            bars2 = axes[1,1].bar(model_names_short, auc_scores, color=colors[:len(auc_scores)], alpha=0.8)
            axes[1,1].set_ylabel('AUC Score')
            axes[1,1].set_title('AUC Score Comparison')
            axes[1,1].set_ylim(min(auc_scores) - 0.02, max(auc_scores) + 0.02)
            
            for bar, auc in zip(bars2, auc_scores):
                height = bar.get_height()
                axes[1,1].text(bar.get_x() + bar.get_width()/2., height + 0.002,
                              f'{auc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Ensure visualizations directory exists
        os.makedirs('../visualizations', exist_ok=True)
        plt.savefig('../visualizations/neural_network_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"\n📈 Visualizations saved to visualizations/neural_network_comparison.png")

if __name__ == "__main__":
    comparator = ModelComparison()
    results = comparator.compare_models()