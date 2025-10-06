# API Documentation

## UFCAnalyzer Class

The main class for analyzing UFC fighter data and making predictions.

### Class Constructor

```python
def __init__(self, db_path='data/ufc_database.db')
```
- **Parameters:**
  - `db_path` (str): Path to the SQLite database containing fighter data
- **Returns:** UFCAnalyzer instance

### Methods

#### predict_win_probability
```python
def predict_win_probability(self, fighter1_name: str, fighter2_name: str) -> dict
```
Predicts the win probability for a specific matchup between two fighters.

- **Parameters:**
  - `fighter1_name` (str): Name of the first fighter
  - `fighter2_name` (str): Name of the second fighter
- **Returns:**
  - dict: Contains the following keys:
    - `fighter1`: Name of first fighter
    - `fighter2`: Name of second fighter
    - `win_probability`: Probability of fighter1 winning
    - `fighter1_stats`: Dictionary of fighter1's stats
    - `fighter2_stats`: Dictionary of fighter2's stats

#### classify_fighting_styles
```python
def classify_fighting_styles(self, n_clusters: int = 4) -> list
```
Classifies fighters into different fighting style categories using clustering.

- **Parameters:**
  - `n_clusters` (int): Number of fighting style clusters to identify
- **Returns:**
  - list: List of dictionaries containing:
    - `style_name`: Identified style name
    - `count`: Number of fighters in this style
    - `avg_stats`: Average stats for this style
    - `top_fighters`: List of top fighters in this style

#### analyze_success_factors
```python
def analyze_success_factors(self) -> dict
```
Analyzes what factors contribute most to fighter success.

- **Returns:**
  - dict: Contains:
    - `feature_importance`: DataFrame of feature importance scores
    - `model_cv_score`: Cross-validation score
    - `model_cv_std`: Standard deviation of CV scores
    - `top_interactions`: List of important feature interactions
    - `interpretation`: Human-readable interpretation of results

### Example Usage

```python
from ufc_analysis import UFCAnalyzer

# Initialize analyzer
analyzer = UFCAnalyzer()

# Predict win probability
prediction = analyzer.predict_win_probability("Fighter A", "Fighter B")
print(f"Win probability: {prediction['win_probability']:.2%}")

# Analyze fighting styles
styles = analyzer.classify_fighting_styles()
for style in styles:
    print(f"Style: {style['style_name']}, Fighters: {style['count']}")

# Get success factors
factors = analyzer.analyze_success_factors()
print("\nTop success factors:")
print(factors['interpretation'])
```

### Advanced Features

#### Feature Engineering
The analyzer creates several derived features:
- `striking_efficiency`: Combined striking accuracy and volume
- `grappling_efficiency`: Combined takedown success
- `defensive_ability`: Combined defensive stats
- `physical_advantage`: Combined physical attributes

#### Model Details
- Uses XGBoost with cross-validation
- SHAP values for interpretability
- Confidence intervals for feature importance
- Stability scores across different data splits