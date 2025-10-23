"""
Create comprehensive visualizations of the normalized UFC data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def create_visualizations():
    """Create all visualizations"""
    print("\n" + "="*60)
    print("CREATING DATA VISUALIZATIONS")
    print("="*60)
    
    # Load the normalized data
    print("\nLoading normalized data...")
    df = pd.read_csv('data/UFC dataset/Large set/large_dataset.csv')
    print(f"Loaded {len(df)} fights")
    
    # Create output directory
    viz_dir = Path('visualizations')
    viz_dir.mkdir(exist_ok=True)
    
    # 1. Winner Distribution
    print("\n1. Creating winner distribution plot...")
    plt.figure(figsize=(10, 6))
    winner_counts = df['winner'].value_counts()
    colors = ['#FF6B6B', '#4ECDC4', '#FFE66D']
    plt.bar(winner_counts.index, winner_counts.values, color=colors, edgecolor='black', linewidth=1.5)
    plt.title('Distribution of Fight Winners', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Winner', fontsize=12)
    plt.ylabel('Number of Fights', fontsize=12)
    for i, v in enumerate(winner_counts.values):
        plt.text(i, v + 50, str(v), ha='center', va='bottom', fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(viz_dir / '01_winner_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved 01_winner_distribution.png")
    
    # 2. Method Distribution
    print("2. Creating finish method distribution plot...")
    plt.figure(figsize=(12, 8))
    method_counts = df['method'].value_counts().head(10)
    colors = sns.color_palette('viridis', len(method_counts))
    plt.barh(range(len(method_counts)), method_counts.values, color=colors, edgecolor='black')
    plt.yticks(range(len(method_counts)), method_counts.index)
    plt.title('Top 10 Fight Finish Methods', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Number of Fights', fontsize=12)
    plt.ylabel('Method', fontsize=12)
    for i, v in enumerate(method_counts.values):
        plt.text(v + 20, i, str(v), va='center', fontsize=10)
    plt.tight_layout()
    plt.savefig(viz_dir / '02_method_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved 02_method_distribution.png")
    
    # 3. Weight Class Distribution
    print("3. Creating weight class distribution plot...")
    plt.figure(figsize=(12, 8))
    weight_counts = df['weight_class'].value_counts()
    colors = sns.color_palette('coolwarm', len(weight_counts))
    plt.barh(range(len(weight_counts)), weight_counts.values, color=colors, edgecolor='black')
    plt.yticks(range(len(weight_counts)), weight_counts.index, fontsize=10)
    plt.title('Fights by Weight Class', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Number of Fights', fontsize=12)
    plt.ylabel('Weight Class', fontsize=12)
    plt.tight_layout()
    plt.savefig(viz_dir / '03_weight_class_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved 03_weight_class_distribution.png")
    
    # 4. Physical Attributes Comparison
    print("4. Creating physical attributes comparison...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Height
    axes[0, 0].hist([df['r_height'].dropna(), df['b_height'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[0, 0].set_title('Height Distribution', fontweight='bold', fontsize=12)
    axes[0, 0].set_xlabel('Height (cm)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Weight
    axes[0, 1].hist([df['r_weight'].dropna(), df['b_weight'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[0, 1].set_title('Weight Distribution', fontweight='bold', fontsize=12)
    axes[0, 1].set_xlabel('Weight (kg)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Reach
    axes[1, 0].hist([df['r_reach'].dropna(), df['b_reach'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[1, 0].set_title('Reach Distribution', fontweight='bold', fontsize=12)
    axes[1, 0].set_xlabel('Reach (cm)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Age
    axes[1, 1].hist([df['r_age'].dropna(), df['b_age'].dropna()], 
                    bins=30, label=['Red Corner', 'Blue Corner'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[1, 1].set_title('Age Distribution', fontweight='bold', fontsize=12)
    axes[1, 1].set_xlabel('Age (years)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('Physical Attributes: Red vs Blue Corner', 
                 fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(viz_dir / '04_physical_attributes.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved 04_physical_attributes.png")
    
    # 5. Win Rate Analysis
    print("5. Creating win rate analysis...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Calculate win rates
    df['r_win_rate'] = df['r_wins_total'] / (df['r_wins_total'] + df['r_losses_total'])
    df['b_win_rate'] = df['b_wins_total'] / (df['b_wins_total'] + df['b_losses_total'])
    
    axes[0].hist(df['r_win_rate'].dropna(), bins=30, alpha=0.8, 
                color='#FF6B6B', edgecolor='black')
    axes[0].set_title('Red Corner Win Rate Distribution', fontweight='bold', fontsize=12)
    axes[0].set_xlabel('Win Rate')
    axes[0].set_ylabel('Frequency')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].hist(df['b_win_rate'].dropna(), bins=30, alpha=0.8, 
                color='#4ECDC4', edgecolor='black')
    axes[1].set_title('Blue Corner Win Rate Distribution', fontweight='bold', fontsize=12)
    axes[1].set_xlabel('Win Rate')
    axes[1].set_ylabel('Frequency')
    axes[1].grid(True, alpha=0.3)
    
    plt.suptitle('Fighter Win Rate Distributions', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(viz_dir / '05_win_rate_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved 05_win_rate_analysis.png")
    
    # 6. Striking Stats
    print("6. Creating striking statistics comparison...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].hist([df['r_SLpM_total'].dropna(), df['b_SLpM_total'].dropna()], 
                    bins=30, label=['Red', 'Blue'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[0, 0].set_title('Strikes Landed per Minute', fontweight='bold')
    axes[0, 0].set_xlabel('SLpM')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].hist([df['r_sig_str_acc_total'].dropna(), df['b_sig_str_acc_total'].dropna()], 
                    bins=30, label=['Red', 'Blue'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[0, 1].set_title('Striking Accuracy', fontweight='bold')
    axes[0, 1].set_xlabel('Accuracy')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].hist([df['r_SApM_total'].dropna(), df['b_SApM_total'].dropna()], 
                    bins=30, label=['Red', 'Blue'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[1, 0].set_title('Strikes Absorbed per Minute', fontweight='bold')
    axes[1, 0].set_xlabel('SApM')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].hist([df['r_str_def_total'].dropna(), df['b_str_def_total'].dropna()], 
                    bins=30, label=['Red', 'Blue'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[1, 1].set_title('Strike Defense', fontweight='bold')
    axes[1, 1].set_xlabel('Defense %')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('Striking Statistics Comparison', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(viz_dir / '06_striking_stats.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved 06_striking_stats.png")
    
    # 7. Grappling Stats
    print("7. Creating grappling statistics comparison...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].hist([df['r_td_avg'].dropna(), df['b_td_avg'].dropna()], 
                    bins=30, label=['Red', 'Blue'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[0, 0].set_title('Takedown Average (per 15 min)', fontweight='bold')
    axes[0, 0].set_xlabel('TD Average')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].hist([df['r_td_acc_total'].dropna(), df['b_td_acc_total'].dropna()], 
                    bins=30, label=['Red', 'Blue'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[0, 1].set_title('Takedown Accuracy', fontweight='bold')
    axes[0, 1].set_xlabel('TD Accuracy')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].hist([df['r_td_def_total'].dropna(), df['b_td_def_total'].dropna()], 
                    bins=30, label=['Red', 'Blue'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[1, 0].set_title('Takedown Defense', fontweight='bold')
    axes[1, 0].set_xlabel('TD Defense %')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].hist([df['r_sub_avg'].dropna(), df['b_sub_avg'].dropna()], 
                    bins=30, label=['Red', 'Blue'], alpha=0.7,
                    color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
    axes[1, 1].set_title('Submission Average (per 15 min)', fontweight='bold')
    axes[1, 1].set_xlabel('Sub Average')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('Grappling Statistics Comparison', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(viz_dir / '07_grappling_stats.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved 07_grappling_stats.png")
    
    # 8. Correlation Heatmap
    print("8. Creating correlation heatmap...")
    plt.figure(figsize=(14, 12))
    
    key_features = [
        'r_SLpM_total', 'r_sig_str_acc_total', 'r_td_avg', 
        'r_td_acc_total', 'r_str_def_total', 'r_td_def_total', 'r_sub_avg',
        'r_height', 'r_weight', 'r_reach', 'r_age'
    ]
    
    key_features = [col for col in key_features if col in df.columns]
    corr_data = df[key_features].dropna()
    correlation = corr_data.corr()
    
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Heatmap - Red Corner Fighter Statistics', 
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(viz_dir / '08_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved 08_correlation_heatmap.png")
    
    # 9. Experience vs Win Rate
    print("9. Creating experience vs win rate scatter plot...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    df['r_total_fights'] = df['r_wins_total'] + df['r_losses_total']
    df['b_total_fights'] = df['b_wins_total'] + df['b_losses_total']
    
    df_clean = df.dropna(subset=['r_total_fights', 'r_win_rate'])
    axes[0].scatter(df_clean['r_total_fights'], df_clean['r_win_rate'], 
                   alpha=0.3, color='#FF6B6B', edgecolors='black', linewidth=0.5, s=30)
    axes[0].set_xlabel('Total Fights (Experience)', fontsize=12)
    axes[0].set_ylabel('Win Rate', fontsize=12)
    axes[0].set_title('Red Corner: Experience vs Win Rate', fontweight='bold', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(0, df_clean['r_total_fights'].quantile(0.95))
    
    df_clean = df.dropna(subset=['b_total_fights', 'b_win_rate'])
    axes[1].scatter(df_clean['b_total_fights'], df_clean['b_win_rate'], 
                   alpha=0.3, color='#4ECDC4', edgecolors='black', linewidth=0.5, s=30)
    axes[1].set_xlabel('Total Fights (Experience)', fontsize=12)
    axes[1].set_ylabel('Win Rate', fontsize=12)
    axes[1].set_title('Blue Corner: Experience vs Win Rate', fontweight='bold', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim(0, df_clean['b_total_fights'].quantile(0.95))
    
    plt.suptitle('Fighter Experience vs Success Rate', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(viz_dir / '09_experience_vs_winrate.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved 09_experience_vs_winrate.png")
    
    # 10. Stance Distribution
    print("10. Creating stance distribution plot...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    r_stance_counts = df['r_stance'].value_counts().head(5)
    axes[0].pie(r_stance_counts.values, labels=r_stance_counts.index, 
                autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Reds_r', 5),
                wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    axes[0].set_title('Red Corner Fighter Stances', fontweight='bold', fontsize=14)
    
    b_stance_counts = df['b_stance'].value_counts().head(5)
    axes[1].pie(b_stance_counts.values, labels=b_stance_counts.index, 
                autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Blues_r', 5),
                wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    axes[1].set_title('Blue Corner Fighter Stances', fontweight='bold', fontsize=14)
    
    plt.suptitle('Fighter Stance Distribution', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(viz_dir / '10_stance_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved 10_stance_distribution.png")
    
    print(f"\n{'='*60}")
    print(f"✅ ALL VISUALIZATIONS COMPLETE!")
    print(f"{'='*60}")
    print(f"\n📁 All {10} visualizations saved in '{viz_dir}/' directory")
    print(f"\n📊 Visualization Files Created:")
    for i in range(1, 11):
        png_file = list(viz_dir.glob(f'{i:02d}_*.png'))[0]
        print(f"   {png_file.name}")

if __name__ == '__main__':
    create_visualizations()