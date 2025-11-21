"""
Fight Prediction Ensemble
Combines Neural Network + Traditional ML models for superior performance
"""

import pandas as pd
import numpy as np
import os
import sys
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Add training directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'training'))

class FightEnsembleExperiment:
    """Experiment with different ensemble combinations"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.results = {}
        self.base_models = {}
        
        # Initialize base models
        self.initialize_base_models()
        
    def initialize_base_models(self):
        """Initialize all base models"""
        print("🏗️ Initializing base models...")
        
        self.base_models = {
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            ),
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            ),
            'svm': SVC(
                probability=True,
                C=1.0,
                kernel='rbf',
                random_state=42
            ),
            'neural_network_sklearn': MLPClassifier(
                hidden_layer_sizes=(128, 64, 32),
                activation='relu',
                solver='adam',
                alpha=0.001,
                learning_rate_init=0.01,
                max_iter=500,
                random_state=42,
                early_stopping=True,
                validation_fraction=0.1
            )
        }
        
        print(f"   ✅ Initialized {len(self.base_models)} base models")
    
    def load_and_prepare_data(self):
        """Load and prepare the fight dataset"""
        print("🔄 Loading fight data...")
        
        # Load data
        data_path = os.path.join(self.base_dir, 'shared', 'data', 'event_normalized_large_dataset.csv')
        self.df = pd.read_csv(data_path)
        print(f"📊 Dataset: {len(self.df)} fights with {self.df.shape[1]} columns")
        
        # Remove non-numeric columns
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        feature_columns = [col for col in numeric_columns if col not in ['winner_encoded', 'event_id']]
        
        # Prepare features and target
        self.X = self.df[feature_columns].fillna(0)
        self.y = self.df['winner_encoded']  # 1 = Red wins, 0 = Blue wins
        
        print(f"📈 Features: {len(feature_columns)} numeric columns")
        print(f"   Target distribution: Red wins: {sum(self.y)} ({sum(self.y)/len(self.y)*100:.1f}%)")
        
        # Train/test split with SAME random state for fair comparison
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        # Scale features for models that need it
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"   Train set: {len(self.X_train)} fights")
        print(f"   Test set: {len(self.X_test)} fights")
    
    def train_individual_models(self):
        """Train all individual models"""
        print("\n🏋️ Training individual models...")
        print("="*60)
        
        individual_results = {}
        
        for model_name, model in self.base_models.items():
            print(f"\n🔄 Training {model_name.replace('_', ' ').title()}...")
            
            try:
                # Use scaled features for SVM and neural networks
                if model_name in ['svm', 'neural_network_sklearn']:
                    model.fit(self.X_train_scaled, self.y_train)
                    y_pred = model.predict(self.X_test_scaled)
                    y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
                    
                    # Cross-validation with scaled features
                    cv_scores = cross_val_score(model, self.X_train_scaled, self.y_train, cv=5)
                else:
                    model.fit(self.X_train, self.y_train)
                    y_pred = model.predict(self.X_test)
                    y_pred_proba = model.predict_proba(self.X_test)[:, 1]
                    
                    # Cross-validation
                    cv_scores = cross_val_score(model, self.X_train, self.y_train, cv=5)
                
                # Calculate metrics
                accuracy = accuracy_score(self.y_test, y_pred)
                auc = roc_auc_score(self.y_test, y_pred_proba)
                cv_mean = cv_scores.mean()
                cv_std = cv_scores.std()
                
                individual_results[model_name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'auc': auc,
                    'cv_mean': cv_mean,
                    'cv_std': cv_std,
                    'predictions': y_pred_proba,
                    'cv_scores': cv_scores
                }
                
                print(f"   ✅ Results:")
                print(f"      Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
                print(f"      AUC: {auc:.4f}")
                print(f"      CV Score: {cv_mean:.4f} ± {cv_std:.4f}")
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
        
        self.individual_results = individual_results
        return individual_results
    
    def create_ensemble_combinations(self):
        """Create different ensemble combinations"""
        print("\n🎯 Creating ensemble combinations...")
        print("="*60)
        
        ensemble_results = {}
        
        # Get trained models
        trained_models = [(name, results['model']) for name, results in self.individual_results.items()]
        
        # 1. Simple Voting Ensemble (All models)
        print("\n🗳️  Testing Simple Voting Ensemble...")
        voting_models = []
        for name, model in trained_models:
            # Create new instances to avoid fitting issues
            if name == 'gradient_boosting':
                voting_models.append(('gb', GradientBoostingClassifier(random_state=42)))
            elif name == 'random_forest':
                voting_models.append(('rf', RandomForestClassifier(random_state=42, n_jobs=-1)))
            elif name == 'svm':
                voting_models.append(('svm', SVC(probability=True, random_state=42)))
            elif name == 'neural_network_sklearn':
                voting_models.append(('nn', MLPClassifier(hidden_layer_sizes=(128, 64, 32), random_state=42, max_iter=500)))
        
        # Create voting classifier
        voting_ensemble = VotingClassifier(estimators=voting_models, voting='soft', n_jobs=-1)
        
        try:
            voting_ensemble.fit(self.X_train_scaled, self.y_train)  # Use scaled for SVM/NN compatibility
            voting_pred_proba = voting_ensemble.predict_proba(self.X_test_scaled)[:, 1]
            voting_pred = (voting_pred_proba > 0.5).astype(int)
            
            voting_accuracy = accuracy_score(self.y_test, voting_pred)
            voting_auc = roc_auc_score(self.y_test, voting_pred_proba)
            
            ensemble_results['voting_all'] = {
                'name': 'Voting Ensemble (All Models)',
                'accuracy': voting_accuracy,
                'auc': voting_auc,
                'predictions': voting_pred_proba,
                'models': list(dict(voting_models).keys())
            }
            
            print(f"   ✅ Voting Ensemble: {voting_accuracy:.4f} ({voting_accuracy*100:.2f}%)")
            
        except Exception as e:
            print(f"   ❌ Voting Ensemble failed: {e}")
        
        # 2. Top 3 Models Ensemble
        print("\n🏆 Testing Top 3 Models Ensemble...")
        top_3_models = sorted(self.individual_results.items(), 
                             key=lambda x: x[1]['accuracy'], reverse=True)[:3]
        
        top_3_voting = []
        for name, _ in top_3_models:
            if name == 'gradient_boosting':
                top_3_voting.append(('gb', GradientBoostingClassifier(random_state=42)))
            elif name == 'random_forest':
                top_3_voting.append(('rf', RandomForestClassifier(random_state=42, n_jobs=-1)))
            elif name == 'svm':
                top_3_voting.append(('svm', SVC(probability=True, random_state=42)))
            elif name == 'neural_network_sklearn':
                top_3_voting.append(('nn', MLPClassifier(hidden_layer_sizes=(128, 64, 32), random_state=42, max_iter=500)))
        
        try:
            top_3_ensemble = VotingClassifier(estimators=top_3_voting, voting='soft', n_jobs=-1)
            top_3_ensemble.fit(self.X_train_scaled, self.y_train)
            top_3_pred_proba = top_3_ensemble.predict_proba(self.X_test_scaled)[:, 1]
            top_3_pred = (top_3_pred_proba > 0.5).astype(int)
            
            top_3_accuracy = accuracy_score(self.y_test, top_3_pred)
            top_3_auc = roc_auc_score(self.y_test, top_3_pred_proba)
            
            ensemble_results['voting_top3'] = {
                'name': 'Voting Ensemble (Top 3)',
                'accuracy': top_3_accuracy,
                'auc': top_3_auc,
                'predictions': top_3_pred_proba,
                'models': [name for name, _ in top_3_models]
            }
            
            print(f"   ✅ Top 3 Ensemble: {top_3_accuracy:.4f} ({top_3_accuracy*100:.2f}%)")
            print(f"      Models: {[name.replace('_', ' ').title() for name, _ in top_3_models]}")
            
        except Exception as e:
            print(f"   ❌ Top 3 Ensemble failed: {e}")
        
        # 3. Weighted Average Ensemble
        print("\n⚖️  Testing Weighted Average Ensemble...")
        try:
            # Use accuracy as weights
            accuracies = [results['accuracy'] for results in self.individual_results.values()]
            predictions = [results['predictions'] for results in self.individual_results.values()]
            
            # Normalize weights to sum to 1
            weights = np.array(accuracies) / sum(accuracies)
            
            # Weighted average of predictions
            weighted_pred_proba = np.zeros(len(self.y_test))
            for i, (weight, pred) in enumerate(zip(weights, predictions)):
                weighted_pred_proba += weight * pred
            
            weighted_pred = (weighted_pred_proba > 0.5).astype(int)
            weighted_accuracy = accuracy_score(self.y_test, weighted_pred)
            weighted_auc = roc_auc_score(self.y_test, weighted_pred_proba)
            
            ensemble_results['weighted_average'] = {
                'name': 'Weighted Average Ensemble',
                'accuracy': weighted_accuracy,
                'auc': weighted_auc,
                'predictions': weighted_pred_proba,
                'weights': dict(zip(self.individual_results.keys(), weights))
            }
            
            print(f"   ✅ Weighted Average: {weighted_accuracy:.4f} ({weighted_accuracy*100:.2f}%)")
            print("      Weights:")
            for name, weight in zip(self.individual_results.keys(), weights):
                print(f"         {name.replace('_', ' ').title()}: {weight:.3f}")
            
        except Exception as e:
            print(f"   ❌ Weighted Average failed: {e}")
        
        # 4. Stacking Ensemble with Meta-learner
        print("\n🥞 Testing Stacking Ensemble...")
        try:
            from sklearn.ensemble import StackingClassifier
            
            stacking_models = []
            for name, model in trained_models:
                if name == 'gradient_boosting':
                    stacking_models.append(('gb', GradientBoostingClassifier(random_state=42)))
                elif name == 'random_forest':
                    stacking_models.append(('rf', RandomForestClassifier(random_state=42, n_jobs=-1)))
                elif name == 'svm':
                    stacking_models.append(('svm', SVC(probability=True, random_state=42)))
                elif name == 'neural_network_sklearn':
                    stacking_models.append(('nn', MLPClassifier(hidden_layer_sizes=(64, 32), random_state=42, max_iter=300)))
            
            # Use logistic regression as meta-learner
            stacking_ensemble = StackingClassifier(
                estimators=stacking_models,
                final_estimator=LogisticRegression(random_state=42),
                cv=3,
                n_jobs=-1
            )
            
            stacking_ensemble.fit(self.X_train_scaled, self.y_train)
            stacking_pred_proba = stacking_ensemble.predict_proba(self.X_test_scaled)[:, 1]
            stacking_pred = (stacking_pred_proba > 0.5).astype(int)
            
            stacking_accuracy = accuracy_score(self.y_test, stacking_pred)
            stacking_auc = roc_auc_score(self.y_test, stacking_pred_proba)
            
            ensemble_results['stacking'] = {
                'name': 'Stacking Ensemble (LogReg Meta)',
                'accuracy': stacking_accuracy,
                'auc': stacking_auc,
                'predictions': stacking_pred_proba,
                'meta_learner': 'Logistic Regression'
            }
            
            print(f"   ✅ Stacking Ensemble: {stacking_accuracy:.4f} ({stacking_accuracy*100:.2f}%)")
            
        except Exception as e:
            print(f"   ❌ Stacking Ensemble failed: {e}")
        
        self.ensemble_results = ensemble_results
        return ensemble_results
    
    def generate_ensemble_report(self):
        """Generate comprehensive ensemble experiment report"""
        print("\n" + "="*80)
        print("🏆 ENSEMBLE EXPERIMENT RESULTS")
        print("="*80)
        
        # Individual model performance
        print("\n📊 INDIVIDUAL MODEL PERFORMANCE:")
        individual_sorted = sorted(self.individual_results.items(), 
                                 key=lambda x: x[1]['accuracy'], reverse=True)
        
        for i, (name, results) in enumerate(individual_sorted, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            print(f"   {medal} {name.replace('_', ' ').title()}: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
        
        # Ensemble performance
        if hasattr(self, 'ensemble_results') and self.ensemble_results:
            print("\n🎯 ENSEMBLE PERFORMANCE:")
            ensemble_sorted = sorted(self.ensemble_results.items(), 
                                   key=lambda x: x[1]['accuracy'], reverse=True)
            
            for i, (name, results) in enumerate(ensemble_sorted, 1):
                medal = "🏆" if i == 1 else "🥇" if i == 2 else "🥈" if i == 3 else f"{i}."
                print(f"   {medal} {results['name']}: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
                
                if 'weights' in results:
                    print("      Weights:", {k.replace('_', ' ').title(): f"{v:.3f}" 
                                          for k, v in results['weights'].items()})
        
        # Best overall performance
        all_results = {}
        
        # Add individual models
        for name, results in self.individual_results.items():
            all_results[f"Individual: {name.replace('_', ' ').title()}"] = results['accuracy']
        
        # Add ensemble models
        if hasattr(self, 'ensemble_results'):
            for name, results in self.ensemble_results.items():
                all_results[f"Ensemble: {results['name']}"] = results['accuracy']
        
        best_model, best_accuracy = max(all_results.items(), key=lambda x: x[1])
        
        print(f"\n🎯 BEST OVERALL PERFORMANCE:")
        print(f"   Model: {best_model}")
        print(f"   Accuracy: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")
        
        # Performance improvement analysis
        best_individual = max(self.individual_results.items(), key=lambda x: x[1]['accuracy'])
        best_individual_acc = best_individual[1]['accuracy']
        
        if hasattr(self, 'ensemble_results') and self.ensemble_results:
            best_ensemble = max(self.ensemble_results.items(), key=lambda x: x[1]['accuracy'])
            best_ensemble_acc = best_ensemble[1]['accuracy']
            
            improvement = (best_ensemble_acc - best_individual_acc) * 100
            
            print(f"\n📈 ENSEMBLE IMPROVEMENT:")
            print(f"   Best Individual: {best_individual[0].replace('_', ' ').title()} ({best_individual_acc*100:.2f}%)")
            print(f"   Best Ensemble: {best_ensemble[1]['name']} ({best_ensemble_acc*100:.2f}%)")
            
            if improvement > 0:
                print(f"   🚀 Improvement: +{improvement:.2f}% accuracy")
                print(f"   📊 Relative gain: {(improvement/best_individual_acc/100)*100:.1f}%")
            else:
                print(f"   ⚠️  No improvement: {improvement:.2f}%")
        
        # Create visualizations
        self.create_ensemble_visualizations()
    
    def create_ensemble_visualizations(self):
        """Create ensemble experiment visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Fight Prediction - Ensemble Experiment Results', fontsize=16, fontweight='bold')
        
        # 1. Individual vs Ensemble Performance
        all_names = []
        all_accuracies = []
        all_types = []
        
        # Individual models
        for name, results in self.individual_results.items():
            all_names.append(name.replace('_', ' ').title())
            all_accuracies.append(results['accuracy'])
            all_types.append('Individual')
        
        # Ensemble models
        if hasattr(self, 'ensemble_results'):
            for name, results in self.ensemble_results.items():
                all_names.append(results['name'])
                all_accuracies.append(results['accuracy'])
                all_types.append('Ensemble')
        
        # Create color map
        colors = ['#FF6B6B' if t == 'Individual' else '#4ECDC4' for t in all_types]
        
        bars = axes[0,0].bar(range(len(all_names)), all_accuracies, color=colors, alpha=0.8)
        axes[0,0].set_ylabel('Accuracy')
        axes[0,0].set_title('Individual vs Ensemble Performance')
        axes[0,0].set_xticks(range(len(all_names)))
        axes[0,0].set_xticklabels(all_names, rotation=45, ha='right')
        
        # Add value labels
        for bar, acc in zip(bars, all_accuracies):
            height = bar.get_height()
            axes[0,0].text(bar.get_x() + bar.get_width()/2., height + 0.002,
                          f'{acc:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
        
        # Add legend
        individual_patch = plt.Rectangle((0,0),1,1, color='#FF6B6B', alpha=0.8, label='Individual')
        ensemble_patch = plt.Rectangle((0,0),1,1, color='#4ECDC4', alpha=0.8, label='Ensemble')
        axes[0,0].legend(handles=[individual_patch, ensemble_patch])
        
        # 2. ROC Curves comparison
        colors_roc = ['#FF6B6B', '#45B7D1', '#96CEB4', '#FECA57', '#F38BA8', '#A8E6CF']
        
        # Plot individual models
        for i, (name, results) in enumerate(self.individual_results.items()):
            fpr, tpr, _ = roc_curve(self.y_test, results['predictions'])
            axes[0,1].plot(fpr, tpr, 
                          label=f'{name.replace("_", " ").title()} (AUC: {results["auc"]:.3f})',
                          color=colors_roc[i % len(colors_roc)], linewidth=2)
        
        # Plot ensemble models
        if hasattr(self, 'ensemble_results'):
            for i, (name, results) in enumerate(self.ensemble_results.items()):
                fpr, tpr, _ = roc_curve(self.y_test, results['predictions'])
                axes[0,1].plot(fpr, tpr, 
                              label=f'{results["name"]} (AUC: {results["auc"]:.3f})',
                              color=colors_roc[(len(self.individual_results) + i) % len(colors_roc)], 
                              linewidth=3, linestyle='--')
        
        axes[0,1].plot([0,1], [0,1], 'k--', alpha=0.5)
        axes[0,1].set_xlabel('False Positive Rate')
        axes[0,1].set_ylabel('True Positive Rate')
        axes[0,1].set_title('ROC Curves - All Models')
        axes[0,1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. Accuracy improvement chart
        if hasattr(self, 'ensemble_results') and self.ensemble_results:
            best_individual_acc = max(results['accuracy'] for results in self.individual_results.values())
            
            ensemble_names = []
            improvements = []
            
            for name, results in self.ensemble_results.items():
                ensemble_names.append(results['name'])
                improvement = (results['accuracy'] - best_individual_acc) * 100
                improvements.append(improvement)
            
            bars = axes[1,0].bar(ensemble_names, improvements, 
                                color=['green' if imp > 0 else 'red' for imp in improvements], alpha=0.8)
            axes[1,0].set_ylabel('Accuracy Improvement (%)')
            axes[1,0].set_title('Ensemble Improvement over Best Individual')
            axes[1,0].tick_params(axis='x', rotation=45)
            axes[1,0].axhline(y=0, color='black', linestyle='-', alpha=0.5)
            
            # Add value labels
            for bar, imp in zip(bars, improvements):
                height = bar.get_height()
                axes[1,0].text(bar.get_x() + bar.get_width()/2., 
                              height + (0.05 if height > 0 else -0.05),
                              f'{imp:.2f}%', ha='center', 
                              va='bottom' if height > 0 else 'top', fontweight='bold')
        
        # 4. Cross-validation scores
        model_names_cv = [name.replace('_', ' ').title() for name in self.individual_results.keys()]
        cv_means = [results['cv_mean'] for results in self.individual_results.values()]
        cv_stds = [results['cv_std'] for results in self.individual_results.values()]
        
        bars = axes[1,1].bar(model_names_cv, cv_means, yerr=cv_stds, 
                            color='#45B7D1', alpha=0.8, capsize=5)
        axes[1,1].set_ylabel('Cross-Validation Score')
        axes[1,1].set_title('Cross-Validation Performance (Individual Models)')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Save visualization
        viz_dir = os.path.join(self.base_dir, 'visualizations')
        os.makedirs(viz_dir, exist_ok=True)
        plt.savefig(os.path.join(viz_dir, 'ensemble_experiment.png'), dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"\n📈 Ensemble experiment visualizations saved to visualizations/ensemble_experiment.png")

def main():
    print("🥊 Fight Prediction - Ensemble Experiment")
    print("   Testing different ensemble combinations for superior performance")
    print("="*80)
    
    experiment = FightEnsembleExperiment()
    experiment.load_and_prepare_data()
    experiment.train_individual_models()
    experiment.create_ensemble_combinations()
    experiment.generate_ensemble_report()

if __name__ == "__main__":
    main()