# Tutorial: Getting Started with UFC Fight Analysis

This tutorial will walk you through common use cases of the UFC Fight Analysis package.

## Basic Usage

### 1. Setting Up

```python
from ufc_analysis import UFCAnalyzer

# Initialize the analyzer
analyzer = UFCAnalyzer()
```

### 2. Simple Win Prediction

```python
# Predict win probability for a matchup
result = analyzer.predict_win_probability(
    fighter1_name="Israel Adesanya",
    fighter2_name="Alex Pereira"
)

print(f"Win probability: {result['win_probability']:.2%}")
```

### 3. Analyzing Fighting Styles

```python
# Get fighting style classifications
styles = analyzer.classify_fighting_styles()

# Print results
for style in styles:
    print(f"\nStyle: {style['style_name']}")
    print(f"Number of fighters: {style['count']}")
    print("Top fighters:", ", ".join(style['top_fighters']))
```

## Advanced Analysis

### 1. Success Factor Analysis

```python
# Get comprehensive success factor analysis
factors = analyzer.analyze_success_factors()

# Print interpretation
print(factors['interpretation'])

# Show top feature importance
print("\nTop 5 Important Features:")
print(factors['feature_importance'].head())
```

### 2. Custom Analysis

```python
# Get raw fighter data
fighter_data = analyzer.df

# Calculate custom metrics
fighter_data['finish_rate'] = fighter_data['wins'] / (fighter_data['wins'] + fighter_data['losses'])
fighter_data['striking_defense'] = fighter_data['str_def']

# Find top defensive fighters
top_defensive = fighter_data.nlargest(5, 'striking_defense')
print("\nTop Defensive Fighters:")
print(top_defensive[['name', 'striking_defense']])
```

## Visualization Examples

### 1. Feature Importance Plot

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Get feature importance data
importance = analyzer.analyze_success_factors()['feature_importance']

# Create plot
plt.figure(figsize=(12, 6))
sns.barplot(data=importance.head(10), x='importance_mean', y='feature')
plt.title('Top 10 Success Factors in UFC')
plt.xlabel('Importance Score')
plt.ylabel('Feature')
plt.tight_layout()
plt.show()
```

### 2. Style Distribution Plot

```python
# Get style classifications
styles = analyzer.classify_fighting_styles()

# Create style distribution plot
style_counts = [s['count'] for s in styles]
style_names = [s['style_name'] for s in styles]

plt.figure(figsize=(10, 6))
plt.pie(style_counts, labels=style_names, autopct='%1.1f%%')
plt.title('Distribution of Fighting Styles')
plt.axis('equal')
plt.show()
```

## Working with Results

### 1. Saving Analysis Results

```python
import json

# Run analysis
results = analyzer.analyze_success_factors()

# Save to file
with open('analysis_results.json', 'w') as f:
    json.dump(results, f, indent=4)
```

### 2. Creating Reports

```python
# Generate comprehensive report
def create_fighter_report(analyzer, fighter_name):
    # Get fighter data
    fighter = analyzer.df[analyzer.df['name'] == fighter_name].iloc[0]
    
    # Get style classification
    styles = analyzer.classify_fighting_styles()
    fighter_style = next(s for s in styles 
                        if fighter_name in s['top_fighters'])
    
    # Create report
    report = {
        'name': fighter_name,
        'style': fighter_style['style_name'],
        'win_rate': f"{fighter['win_rate']:.2%}",
        'key_stats': {
            'strikes_per_min': fighter['slpm'],
            'takedowns_per_15min': fighter['td_avg'],
            'submission_avg': fighter['sub_avg']
        }
    }
    
    return report

# Example usage
report = create_fighter_report(analyzer, "Fighter Name")
print(json.dumps(report, indent=2))
```

## Tips and Best Practices

1. **Data Quality**
   - Always check for missing values
   - Verify fighter names match exactly
   - Use recent data when available

2. **Performance**
   - Cache results for frequently used analyses
   - Use batch processing for multiple predictions
   - Consider using parallel processing for large datasets

3. **Analysis**
   - Consider context when interpreting results
   - Look at multiple metrics
   - Account for fighting style matchups

4. **Visualization**
   - Use appropriate plot types
   - Include error bars when applicable
   - Make plots readable and informative