# UFC Large Dataset Normalization Guide

## Overview
The large_dataset.csv contains 7,439 UFC fights with 95 columns including detailed fight statistics, fighter information, and computed differentials.

## Normalization Strategy

### 1. Database Normalization (3NF)
Breaking the dataset into properly normalized tables:

#### Tables Created:
- **events**: Event-level information (event_name, weight_class, referee, etc.)
- **fighters**: Fighter-specific information (name, height, reach, stance)
- **fights**: Fight outcomes (winner, method, round, time)
- **fight_statistics**: Detailed per-fight statistics

**Benefits:**
- Eliminates data redundancy
- Easier to update fighter information
- Better query performance
- Data integrity enforcement

### 2. Missing Value Handling
Strategy by column type:
- **Accuracy/Percentage columns**: Fill with median
- **Difference columns (_diff)**: Fill with 0 (no difference)
- **Time columns**: Fill with median
- **Categorical columns**: Fill with 'Unknown'

### 3. Feature Scaling

#### Min-Max Scaling (0-1 range)
Applied to:
- Accuracy metrics (sig_str_acc, td_acc, str_def, td_def)
- Percentage-based features

#### Standard Scaling (z-score)
Applied to:
- Rate metrics (SLpM, SApM, avg stats)
- Count metrics (knockdowns, strikes, takedowns)
- Physical attributes (height, weight, reach, age)
- Difference columns

### 4. Feature Engineering
New features created:

#### Performance Metrics:
- `win_rate`: Wins / Total fights
- `win_rate_diff`: Difference in win rates
- `total_fights`: Experience level
- `experience_diff`: Experience advantage

#### Physical Metrics:
- `bmi`: Body Mass Index
- `bmi_diff`: BMI advantage

#### Combat Efficiency:
- `striking_efficiency`: SLpM × Accuracy
- `grappling_efficiency`: TD Average × TD Accuracy
- `defensive_rating`: (Strike Defense + TD Defense) / 2

### 5. Categorical Encoding
Label encoding applied to:
- `stance` (Orthodox, Southpaw, Switch, etc.)
- `winner` (Red, Blue, Draw, No Contest)
- `method` (KO/TKO, Submission, Decision, etc.)
- `gender` (Men, Women)
- `weight_class`

## Usage

### Run the Normalization Script:
```bash
python scripts/normalize_large_dataset.py
```

### Outputs:
1. **normalized_ufc.db**: SQLite database with normalized tables
2. **normalized_large_dataset.csv**: Processed CSV with all transformations

### Using the Normalized Data:

```python
from scripts.normalize_large_dataset import UFCDataNormalizer

# Initialize
normalizer = UFCDataNormalizer()

# Load and process
normalizer.load_data()
normalizer.handle_missing_values()

# Create normalized database
normalizer.create_normalized_database()

# Create feature-engineered dataset
normalized_df = normalizer.create_feature_engineered_dataset()

# Scale features for ML
scaled_df = normalizer.scale_features()
```

## Column Categories

### Red Corner (r_) Features:
- In-fight stats: r_kd, r_sig_str, r_td, r_sub_att, etc.
- Career totals: r_wins_total, r_losses_total
- Physical: r_height, r_weight, r_reach, r_age
- Performance: r_SLpM_total, r_sig_str_acc_total, etc.

### Blue Corner (b_) Features:
- Same structure as red corner

### Differential Features (*_diff):
- Pre-computed differences between fighters
- Useful for direct comparison modeling

## Recommendations for ML Models

### 1. Classification (Winner Prediction)
**Recommended features:**
- Win rate differences
- Physical advantages
- Striking/grappling efficiency
- Defensive ratings
- Experience differential

### 2. Regression (Fight Duration/Rounds)
**Recommended features:**
- Fighter stamina indicators
- Historical finish rates
- Style matchup features

### 3. Multi-class (Method Prediction)
**Recommended features:**
- Finish type history
- Striking vs grappling efficiency
- Submission attempt rates

## Best Practices

1. **Always check for data leakage**: Don't use in-fight stats for pre-fight predictions
2. **Separate training/test by date**: Ensure no temporal leakage
3. **Feature selection**: Use feature importance to reduce dimensionality
4. **Cross-validation**: Use time-series CV for temporal data
5. **Handle class imbalance**: Winner distribution may be imbalanced

## Next Steps

1. Exploratory Data Analysis (EDA)
2. Feature importance analysis
3. Model selection and training
4. Hyperparameter tuning
5. Model evaluation and validation