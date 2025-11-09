"""
Master script to run normalization, ML pipeline, and create visualizations.
"""

import sys
import os
sys.path.append('scripts')
sys.path.append('src/ufc_analysis')

from normalize_large_dataset import UFCDataNormalizer
from ml_pipeline import UFCMLPipeline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def create_data_visualizations(normalizer):
    """
    Create comprehensive visualizations of the normalized data.
    """
    print("\n" + "="*60)
    print("CREATING DATA VISUALIZATIONS")
    print("="*60)
    
    df = normalizer.df
    
    # Create output directory
    viz_dir = Path('visualizations')
    viz_dir.mkdir(exist_ok=True)
    
    # 1. Winner Distribution
    print("\n1. Creating winner distribution plot...")
    plt.figure(figsize=(10, 6))
    winner_counts = df['winner'].value_counts()
    sns.barplot(x=winner_counts.index, y=winner_counts.values)
    plt.title('Distribution of Fight Winners', fontsize=16, fontweight='bold')
    plt.xlabel('Winner', fontsize=12)
    plt.ylabel('Number of Fights', fontsize=12)
    plt.tight_layout()
    plt.savefig(viz_dir / '01_winner_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Method Distribution
    print("2. Creating finish method distribution plot...")
    plt.figure(figsize=(12, 6))
    method_counts = df['method'].value_counts().head(10)
    sns.barplot(x=method_counts.values, y=method_counts.index, palette='viridis')
    plt.title('Top 10 Fight Finish Methods', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Fights', fontsize=12)
    plt.ylabel('Method', fontsize=12)
    plt.tight_layout()
    plt.savefig(viz_dir / '02_method_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Weight Class Distribution
    print("3. Creating weight class distribution plot...")
    plt.figure(figsize=(12, 8))
    weight_counts = df['weight_class'].value_counts()
    sns.barplot(y=weight_counts.index, x=weight_counts.values, palette='coolwarm')
    plt.title('Fights by Weight Class', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Fights', fontsize=12)
    plt.ylabel('Weight Class', fontsize=12)
    plt.tight_layout()
    plt.savefig(viz_dir / '03_weight_class_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Physical Attributes Comparison
    print("4. Creating physical attributes comparison...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Height comparison
    axes[0, 0].hist([df['r_height'].dropna(), df['b_height'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7)
    axes[0, 0].set_title('Height Distribution', fontweight='bold')
    axes[0, 0].set_xlabel('Height (cm)')
    axes[0, 0].legend()
    
    # Weight comparison
    axes[0, 1].hist([df['r_weight'].dropna(), df['b_weight'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7, color=['red', 'blue'])
    axes[0, 1].set_title('Weight Distribution', fontweight='bold')
    axes[0, 1].set_xlabel('Weight (kg)')
    axes[0, 1].legend()
    
    # Reach comparison
    axes[1, 0].hist([df['r_reach'].dropna(), df['b_reach'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7, color=['orange', 'cyan'])
    axes[1, 0].set_title('Reach Distribution', fontweight='bold')
    axes[1, 0].set_xlabel('Reach (cm)')
    axes[1, 0].legend()
    
    # Age comparison
    axes[1, 1].hist([df['r_age'].dropna(), df['b_age'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7, color=['green', 'purple'])
    axes[1, 1].set_title('Age Distribution', fontweight='bold')
    axes[1, 1].set_xlabel('Age (years)')
    axes[1, 1].legend()
    
    plt.suptitle('Physical Attributes Comparison: Red vs Blue Corner', 
                 fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(viz_dir / '04_physical_attributes.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Win Rate Analysis
    print("5. Creating win rate analysis...")
    plt.figure(figsize=(12, 6))
    
    # Calculate win rates
    df_clean = df.dropna(subset=['r_win_rate', 'b_win_rate'])
    
    plt.subplot(1, 2, 1)
    plt.hist(df_clean['r_win_rate'], bins=30, alpha=0.7, color='red', edgecolor='black')
    plt.title('Red Corner Win Rate Distribution', fontweight='bold')
    plt.xlabel('Win Rate')
    plt.ylabel('Frequency')
    
    plt.subplot(1, 2, 2)
    plt.hist(df_clean['b_win_rate'], bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.title('Blue Corner Win Rate Distribution', fontweight='bold')
    plt.xlabel('Win Rate')
    plt.ylabel('Frequency')
    
    plt.suptitle('Fighter Win Rate Distributions', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(viz_dir / '05_win_rate_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Striking Stats Comparison
    print("6. Creating striking statistics comparison...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Strikes landed per minute
    axes[0, 0].hist([df['r_SLpM_total'].dropna(), df['b_SLpM_total'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7)
    axes[0, 0].set_title('Strikes Landed per Minute', fontweight='bold')
    axes[0, 0].set_xlabel('SLpM')
    axes[0, 0].legend()
    
    # Striking accuracy
    axes[0, 1].hist([df['r_sig_str_acc_total'].dropna(), df['b_sig_str_acc_total'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7, color=['red', 'blue'])
    axes[0, 1].set_title('Striking Accuracy', fontweight='bold')
    axes[0, 1].set_xlabel('Accuracy')
    axes[0, 1].legend()
    
    # Strikes absorbed per minute
    axes[1, 0].hist([df['r_SApM_total'].dropna(), df['b_SApM_total'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7, color=['orange', 'cyan'])
    axes[1, 0].set_title('Strikes Absorbed per Minute', fontweight='bold')
    axes[1, 0].set_xlabel('SApM')
    axes[1, 0].legend()
    
    # Strike defense
    axes[1, 1].hist([df['r_str_def_total'].dropna(), df['b_str_def_total'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7, color=['green', 'purple'])
    axes[1, 1].set_title('Strike Defense', fontweight='bold')
    axes[1, 1].set_xlabel('Defense %')
    axes[1, 1].legend()
    
    plt.suptitle('Striking Statistics Comparison', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(viz_dir / '06_striking_stats.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 7. Grappling Stats Comparison
    print("7. Creating grappling statistics comparison...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Takedown average
    axes[0, 0].hist([df['r_td_avg'].dropna(), df['b_td_avg'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7)
    axes[0, 0].set_title('Takedown Average per 15 min', fontweight='bold')
    axes[0, 0].set_xlabel('TD Average')
    axes[0, 0].legend()
    
    # Takedown accuracy
    axes[0, 1].hist([df['r_td_acc_total'].dropna(), df['b_td_acc_total'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7, color=['red', 'blue'])
    axes[0, 1].set_title('Takedown Accuracy', fontweight='bold')
    axes[0, 1].set_xlabel('TD Accuracy')
    axes[0, 1].legend()
    
    # Takedown defense
    axes[1, 0].hist([df['r_td_def_total'].dropna(), df['b_td_def_total'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7, color=['orange', 'cyan'])
    axes[1, 0].set_title('Takedown Defense', fontweight='bold')
    axes[1, 0].set_xlabel('TD Defense %')
    axes[1, 0].legend()
    
    # Submission average
    axes[1, 1].hist([df['r_sub_avg'].dropna(), df['b_sub_avg'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7, color=['green', 'purple'])
    axes[1, 1].set_title('Submission Average per 15 min', fontweight='bold')
    axes[1, 1].set_xlabel('Sub Average')
    axes[1, 1].legend()
    
    plt.suptitle('Grappling Statistics Comparison', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(viz_dir / '07_grappling_stats.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 8. Correlation Heatmap of Key Features
    print("8. Creating correlation heatmap...")
    plt.figure(figsize=(14, 12))
    
    # Select key features for correlation
    key_features = [
        'r_win_rate', 'r_SLpM_total', 'r_sig_str_acc_total', 'r_td_avg', 
        'r_td_acc_total', 'r_str_def_total', 'r_td_def_total', 'r_sub_avg',
        'r_height', 'r_weight', 'r_reach', 'r_age'
    ]
    
    corr_data = df[key_features].dropna()
    correlation = corr_data.corr()
    
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1)
    plt.title('Correlation Heatmap of Fighter Statistics (Red Corner)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(viz_dir / '08_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 9. Experience vs Win Rate
    print("9. Creating experience vs win rate scatter plot...")
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    df_clean = df.dropna(subset=['r_total_fights', 'r_win_rate'])
    plt.scatter(df_clean['r_total_fights'], df_clean['r_win_rate'], 
                alpha=0.3, color='red', edgecolors='black', linewidth=0.5)
    plt.xlabel('Total Fights (Experience)', fontsize=12)
    plt.ylabel('Win Rate', fontsize=12)
    plt.title('Red Corner: Experience vs Win Rate', fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    df_clean = df.dropna(subset=['b_total_fights', 'b_win_rate'])
    plt.scatter(df_clean['b_total_fights'], df_clean['b_win_rate'], 
                alpha=0.3, color='blue', edgecolors='black', linewidth=0.5)
    plt.xlabel('Total Fights (Experience)', fontsize=12)
    plt.ylabel('Win Rate', fontsize=12)
    plt.title('Blue Corner: Experience vs Win Rate', fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.suptitle('Fighter Experience vs Success Rate', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(viz_dir / '09_experience_vs_winrate.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 10. Stance Distribution
    print("10. Creating stance distribution plot...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Red corner stances
    r_stance_counts = df['r_stance'].value_counts().head(5)
    axes[0].pie(r_stance_counts.values, labels=r_stance_counts.index, 
                autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Reds', 5))
    axes[0].set_title('Red Corner Fighter Stances', fontweight='bold', fontsize=14)
    
    # Blue corner stances
    b_stance_counts = df['b_stance'].value_counts().head(5)
    axes[1].pie(b_stance_counts.values, labels=b_stance_counts.index, 
                autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Blues', 5))
    axes[1].set_title('Blue Corner Fighter Stances', fontweight='bold', fontsize=14)
    
    plt.suptitle('Fighter Stance Distribution', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(viz_dir / '10_stance_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✅ All visualizations saved in '{viz_dir}/' directory!")
    print(f"   Created 10 comprehensive visualization files")

def main():
    print("\n" + "🥊" * 30)
    print("COMPLETE UFC ANALYSIS PIPELINE")
    print("🥊" * 30 + "\n")
    
    # PHASE 1: NORMALIZATION
    print("\n" + "="*60)
    print("PHASE 1: DATA NORMALIZATION")
    print("="*60)
    
    normalizer = UFCDataNormalizer()
    normalizer.load_data()
    normalizer.handle_missing_values()
    
    # Create normalized database
    normalizer.create_normalized_database()
    
    # Create feature-engineered dataset
    normalized_df = normalizer.create_feature_engineered_dataset()
    
    # Save normalized CSV
    normalizer.save_normalized_csv()
    
    print("\n✅ PHASE 1 COMPLETE - Data normalized and saved!")
    
    # PHASE 2: VISUALIZATIONS
    print("\n" + "="*60)
    print("PHASE 2: DATA VISUALIZATIONS")
    print("="*60)
    
    create_data_visualizations(normalizer)
    
    print("\n✅ PHASE 2 COMPLETE - Visualizations created!")
    
    # PHASE 3: ML PIPELINE
    print("\n" + "="*60)
    print("PHASE 3: MACHINE LEARNING PIPELINE")
    print("="*60)
    
    pipeline = UFCMLPipeline()
    results = pipeline.run_full_pipeline()
    
    print("\n✅ PHASE 3 COMPLETE - ML models trained and evaluated!")
    
    # FINAL SUMMARY
    print("\n" + "="*60)
    print("🎉 ALL PHASES COMPLETE! 🎉")
    print("="*60)
    
    print("\n📁 Output Files Created:")
    print("   1. data/normalized_ufc.db - Normalized database")
    print("   2. data/normalized_large_dataset.csv - Processed CSV")
    print("   3. visualizations/ - 10 comprehensive visualizations")
    print("   4. models/ - Trained ML models")
    print("   5. feature_importance.png - Feature importance plot")
    print("   6. shap_summary.png - SHAP analysis")
    
    print("\n📊 Visualization Files:")
    print("   01_winner_distribution.png")
    print("   02_method_distribution.png")
    print("   03_weight_class_distribution.png")
    print("   04_physical_attributes.png")
    print("   05_win_rate_analysis.png")
    print("   06_striking_stats.png")
    print("   07_grappling_stats.png")
    print("   08_correlation_heatmap.png")
    print("   09_experience_vs_winrate.png")
    print("   10_stance_distribution.png")
    
    print("\n🤖 ML Models:")
    print("   - Logistic Regression")
    print("   - Random Forest")
    print("   - XGBoost (tuned)")
    
    print("\n" + "="*60)
    print("Ready for analysis and predictions!")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()