import pandas as pd
import numpy as np
from xgboost import XGBClassifier, XGBRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
from sklearn.cluster import KMeans
import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

class UFCAnalyzer:
    def __init__(self, db_path='data/ufc_database.db'):
        self.db_path = Path(db_path)
        self.df = self.load_data()
        self.feature_columns = [
            'wins', 'losses', 'height', 'weight', 'reach', 'age',
            'slpm', 'sig_str_acc', 'sapm', 'str_def',
            'td_avg', 'td_acc', 'td_def', 'sub_avg'
        ]
        self.le_stance = LabelEncoder()
        self.scaler = StandardScaler()
        self.prepare_data()

    def load_data(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql('SELECT * FROM fighter_stats', conn)
        conn.close()
        return df

    def prepare_data(self):
        # Drop rows with missing values
        self.df = self.df.dropna()
        
        # Calculate derived features
        self.df['win_rate'] = self.df['wins'] / (self.df['wins'] + self.df['losses'])
        self.df['finish_rate'] = 0  # Placeholder - we'll need actual finish data
        
        # Encode categorical variables
        self.df['stance_encoded'] = self.le_stance.fit_transform(self.df['stance'].fillna('Unknown'))
        
        # Scale numerical features
        self.df[self.feature_columns] = self.scaler.fit_transform(self.df[self.feature_columns])

    def predict_win_probability(self, fighter1_name, fighter2_name):
        """Predict win probability for a specific matchup"""
        if fighter1_name not in self.df['name'].values or fighter2_name not in self.df['name'].values:
            return "One or both fighters not found in database."
        
        fighter1 = self.df[self.df['name'] == fighter1_name].iloc[0]
        fighter2 = self.df[self.df['name'] == fighter2_name].iloc[0]
        
        # Create feature vector for the matchup
        matchup_features = []
        for col in self.feature_columns + ['stance_encoded', 'win_rate']:
            matchup_features.append(fighter1[col] - fighter2[col])  # Difference in stats
            matchup_features.append(fighter1[col])  # Fighter 1 stats
            matchup_features.append(fighter2[col])  # Fighter 2 stats
        
        # Train model on historical matchups (if we had them)
        # For now, we'll use a simple comparison of win rates
        prob = 1 / (1 + np.exp(-(fighter1['win_rate'] - fighter2['win_rate'])))
        
        return {
            'fighter1': fighter1_name,
            'fighter2': fighter2_name,
            'win_probability': prob,
            'fighter1_stats': fighter1[self.feature_columns].to_dict(),
            'fighter2_stats': fighter2[self.feature_columns].to_dict()
        }

    def classify_fighting_styles(self, n_clusters=4):
        """Classify fighters by fighting style using clustering"""
        # Select features relevant to fighting style
        style_features = [
            'slpm', 'sig_str_acc', 'sapm', 'str_def',
            'td_avg', 'td_acc', 'td_def', 'sub_avg'
        ]
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.df['fighting_style'] = kmeans.fit_predict(self.df[style_features])
        
        # Analyze cluster characteristics
        cluster_analysis = []
        for cluster in range(n_clusters):
            cluster_fighters = self.df[self.df['fighting_style'] == cluster]
            cluster_stats = cluster_fighters[style_features].mean()
            
            # Determine style based on dominant stats
            style_name = self.determine_style_name(cluster_stats)
            
            cluster_analysis.append({
                'style_name': style_name,
                'count': len(cluster_fighters),
                'avg_stats': cluster_stats.to_dict(),
                'top_fighters': cluster_fighters.nlargest(3, 'win_rate')['name'].tolist()
            })
        
        return cluster_analysis

    def determine_style_name(self, stats):
        """Determine fighting style name based on stats"""
        if stats['td_avg'] > 2 and stats['sub_avg'] > 0.5:
            return "Grappler"
        elif stats['slpm'] > 4 and stats['sig_str_acc'] > 0.4:
            return "Striker"
        elif stats['td_avg'] > 1.5 and stats['slpm'] > 3:
            return "Hybrid"
        else:
            return "Defensive"

    def analyze_success_factors(self):
        """Analyze what factors contribute most to fighter success"""
        # Create success metrics
        self.df['success_score'] = (
            self.df['win_rate'] * 0.6 +  # Win rate importance
            self.df['wins'] * 0.3 +      # Total wins importance
            (1 - self.df['losses'] / self.df['wins'].max()) * 0.1  # Loss minimization
        )
        
        # Calculate correlations with success
        correlations = self.df[self.feature_columns + ['stance_encoded']].corrwith(self.df['success_score'])
        
        # Create feature importance model
        X = self.df[self.feature_columns + ['stance_encoded']]
        y = self.df['success_score']
        model = XGBRegressor(random_state=42)
        model.fit(X, y)
        
        # Combine correlation and feature importance
        success_factors = pd.DataFrame({
            'feature': X.columns,
            'correlation': correlations,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return success_factors

    def plot_success_factors(self, success_factors):
        """Plot success factors analysis"""
        plt.figure(figsize=(12, 6))
        
        # Plot feature importance
        plt.subplot(1, 2, 1)
        sns.barplot(x='importance', y='feature', data=success_factors.head(10))
        plt.title('Top 10 Success Factors (Feature Importance)')
        
        # Plot correlations
        plt.subplot(1, 2, 2)
        sns.barplot(x='correlation', y='feature', data=success_factors.head(10))
        plt.title('Top 10 Success Factors (Correlation)')
        
        plt.tight_layout()
        plt.savefig('success_factors.png')
        plt.close()

    def analyze_all(self):
        """Run all analyses and return comprehensive results"""
        results = {
            'fighting_styles': self.classify_fighting_styles(),
            'success_factors': self.analyze_success_factors()
        }
        
        # Example matchup prediction
        example_fighters = self.df['name'].sample(2).tolist()
        results['example_matchup'] = self.predict_win_probability(example_fighters[0], example_fighters[1])
        
        # Plot results
        self.plot_success_factors(results['success_factors'])
        
        return results

def main():
    analyzer = UFCAnalyzer()
    results = analyzer.analyze_all()
    
    # Print fighting styles analysis
    print("\nFighting Styles Analysis:")
    for style in results['fighting_styles']:
        print(f"\n{style['style_name']}:")
        print(f"Number of fighters: {style['count']}")
        print(f"Top fighters: {', '.join(style['top_fighters'])}")
        print("Average stats:")
        for stat, value in style['avg_stats'].items():
            print(f"  {stat}: {value:.2f}")
    
    # Print example matchup prediction
    print("\nExample Matchup Prediction:")
    matchup = results['example_matchup']
    print(f"{matchup['fighter1']} vs {matchup['fighter2']}")
    print(f"Win probability for {matchup['fighter1']}: {matchup['win_probability']:.2%}")
    
    # Print top success factors
    print("\nTop Success Factors:")
    print(results['success_factors'].head(10))
    print("\nSuccess factors plot has been saved as 'success_factors.png'")

if __name__ == '__main__':
    main()