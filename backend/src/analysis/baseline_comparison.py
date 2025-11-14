"""
Baseline Model Comparison
Compare different machine learning approaches on UFC fight prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class BaselineComparison:
    def __init__(self):
        self.models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'SVM': SVC(probability=True, random_state=42)
        }
        self.results = {}
        
    def load_and_prepare_data(self):
        """Load and prepare the UFC dataset"""
        print("🔄 Loading UFC fight data...")
        
        # Load data
        self.df = pd.read_csv('../../shared/data/event_normalized_large_dataset.csv')
        print(f"📊 Dataset: {len(self.df)} fights with {self.df.shape[1]} columns")
        
        # Remove non-numeric columns for baseline comparison
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        feature_columns = [col for col in numeric_columns if col not in ['winner_encoded', 'event_id']]
        
        # Prepare features and target
        X = self.df[feature_columns].fillna(0)
        y = self.df['winner_encoded']  # 1 = Red wins, 0 = Blue wins
        
        print(f"📈 Features: {len(feature_columns)} numeric columns")
        print(f"   Target distribution: Red wins: {sum(y)} ({sum(y)/len(y)*100:.1f}%)")
        print(f"   Target distribution: Blue wins: {len(y)-sum(y)} ({(len(y)-sum(y))/len(y)*100:.1f}%)")
        
        # Train/test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features for algorithms that need it
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"   Train set: {len(self.X_train)} fights")
        print(f"   Test set: {len(self.X_test)} fights")
        
    def train_and_evaluate_models(self):
        """Train and evaluate all baseline models"""
        print("\n🏋️ Training and evaluating models...")
        print("="*60)
        
        for model_name, model in self.models.items():
            print(f"\n🔄 Training {model_name}...")
            
            try:
                # Use scaled features for SVM and Logistic Regression
                if model_name in ['SVM', 'Logistic Regression']:
                    model.fit(self.X_train_scaled, self.y_train)
                    y_pred = model.predict(self.X_test_scaled)
                    y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
                    
                    # Cross-validation with scaled features
                    cv_scores = cross_val_score(model, self.X_train_scaled, self.y_train, cv=5)
                else:
                    model.fit(self.X_train, self.y_train)
                    y_pred = model.predict(self.X_test)
                    y_pred_proba = model.predict_proba(self.X_test)[:, 1]
                    
                    # Cross-validation with original features
                    cv_scores = cross_val_score(model, self.X_train, self.y_train, cv=5)
                
                # Calculate metrics
                accuracy = accuracy_score(self.y_test, y_pred)
                auc = roc_auc_score(self.y_test, y_pred_proba)
                cv_mean = cv_scores.mean()
                cv_std = cv_scores.std()
                
                # Store results
                self.results[model_name] = {
                    'accuracy': accuracy,
                    'auc': auc,
                    'cv_mean': cv_mean,
                    'cv_std': cv_std,
                    'predictions': y_pred,
                    'probabilities': y_pred_proba
                }
                
                print(f"   ✅ {model_name} Results:")
                print(f"      Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
                print(f"      AUC: {auc:.4f}")
                print(f"      CV Score: {cv_mean:.4f} ± {cv_std:.4f}")
                
            except Exception as e:
                print(f"   ❌ {model_name} failed: {e}")
                
        return self.results
    
    def generate_comparison_report(self):
        """Generate comprehensive comparison report"""
        print("\n" + "="*80)
        print("🏆 BASELINE MODEL COMPARISON RESULTS")
        print("="*80)
        
        if not self.results:
            print("❌ No results available")
            return
            
        # Sort models by accuracy
        sorted_models = sorted(self.results.items(), key=lambda x: x[1]['accuracy'], reverse=True)
        
        print(f"\n📊 PERFORMANCE RANKING (Test Set Accuracy):")
        for i, (model_name, results) in enumerate(sorted_models, 1):
            accuracy = results['accuracy']
            auc = results['auc']
            cv_score = results['cv_mean']
            
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            print(f"   {medal} {model_name}")
            print(f"      Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
            print(f"      AUC Score: {auc:.4f}")
            print(f"      Cross-Val: {cv_score:.4f} ± {results['cv_std']:.4f}")
            print()
        
        # Best model analysis
        best_model_name, best_results = sorted_models[0]
        print(f"🎯 BEST MODEL: {best_model_name}")
        print(f"   Achieved {best_results['accuracy']*100:.2f}% accuracy on test set")
        print(f"   AUC: {best_results['auc']:.4f} (excellent discrimination)")
        
        # Model agreement analysis
        if len(self.results) > 1:
            print(f"\n🤝 MODEL CONSENSUS ANALYSIS:")
            predictions = {name: results['predictions'] for name, results in self.results.items()}
            
            # Calculate pairwise agreement
            model_names = list(predictions.keys())
            agreements = {}
            
            for i in range(len(model_names)):
                for j in range(i+1, len(model_names)):
                    model1, model2 = model_names[i], model_names[j]
                    agreement = np.mean(predictions[model1] == predictions[model2])
                    agreements[f"{model1} vs {model2}"] = agreement
            
            avg_agreement = np.mean(list(agreements.values()))
            print(f"   Average Model Agreement: {avg_agreement*100:.1f}%")
            
            if avg_agreement > 0.8:
                print("   ✅ High consensus - models generally agree")
            elif avg_agreement > 0.6:
                print("   ⚠️  Moderate consensus - some disagreement")  
            else:
                print("   ❌ Low consensus - significant model disagreement")
        
        self.create_visualizations()
        
    def create_visualizations(self):
        """Create comparison visualizations"""
        if not self.results:
            return
            
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('UFC Fight Prediction - Baseline Model Comparison', fontsize=16, fontweight='bold')
        
        # 1. Accuracy comparison bar chart
        model_names = list(self.results.keys())
        accuracies = [self.results[name]['accuracy'] for name in model_names]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        bars = axes[0,0].bar(model_names, accuracies, color=colors[:len(model_names)], alpha=0.8)
        axes[0,0].set_ylabel('Test Accuracy')
        axes[0,0].set_title('Model Accuracy Comparison')
        axes[0,0].tick_params(axis='x', rotation=45)
        axes[0,0].set_ylim(min(accuracies) - 0.02, max(accuracies) + 0.02)
        
        # Add value labels
        for bar, acc in zip(bars, accuracies):
            height = bar.get_height()
            axes[0,0].text(bar.get_x() + bar.get_width()/2., height + 0.002,
                          f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # 2. ROC Curves
        for i, (model_name, results) in enumerate(self.results.items()):
            fpr, tpr, _ = roc_curve(self.y_test, results['probabilities'])
            axes[0,1].plot(fpr, tpr, label=f'{model_name} (AUC: {results["auc"]:.3f})',
                          color=colors[i % len(colors)], linewidth=2)
        
        axes[0,1].plot([0,1], [0,1], 'k--', alpha=0.5)
        axes[0,1].set_xlabel('False Positive Rate')
        axes[0,1].set_ylabel('True Positive Rate')
        axes[0,1].set_title('ROC Curve Comparison')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. Cross-validation scores
        cv_means = [self.results[name]['cv_mean'] for name in model_names]
        cv_stds = [self.results[name]['cv_std'] for name in model_names]
        
        bars = axes[1,0].bar(model_names, cv_means, yerr=cv_stds, 
                            color=colors[:len(model_names)], alpha=0.8, capsize=5)
        axes[1,0].set_ylabel('Cross-Validation Score')
        axes[1,0].set_title('Cross-Validation Performance')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # 4. Prediction confidence distribution (best model)
        best_model_name = max(self.results.keys(), key=lambda x: self.results[x]['accuracy'])
        best_probs = self.results[best_model_name]['probabilities']
        
        axes[1,1].hist(best_probs, bins=30, alpha=0.7, color='#FF6B6B', edgecolor='black')
        axes[1,1].axvline(0.5, color='red', linestyle='--', alpha=0.7, label='Decision Threshold')
        axes[1,1].set_xlabel('Prediction Probability')
        axes[1,1].set_ylabel('Frequency')
        axes[1,1].set_title(f'{best_model_name} - Prediction Distribution')
        axes[1,1].legend()
        
        plt.tight_layout()
        plt.savefig('visualizations/baseline_model_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"\n📈 Visualizations saved to visualizations/baseline_model_comparison.png")

def main():
    print("🥊 UFC Fight Prediction - Baseline Model Comparison")
    print("="*60)
    
    comparator = BaselineComparison()
    comparator.load_and_prepare_data()
    comparator.train_and_evaluate_models()
    comparator.generate_comparison_report()

if __name__ == "__main__":
    main()