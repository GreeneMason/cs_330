# Machine Learning Pipeline for Normalized UFC Data

## Overview
This document explains how to build a complete ML pipeline using the normalized UFC dataset. The pipeline will take you from raw normalized data through to trained models that can predict fight outcomes.

## Pipeline Architecture

```
Raw Data → Normalization → Feature Selection → Train/Test Split → 
Model Training → Hyperparameter Tuning → Evaluation → Deployment
```

## Detailed Pipeline Steps

### 1. Data Loading & Preprocessing
```python
from scripts.normalize_large_dataset import UFCDataNormalizer
import pandas as pd
from sklearn.model_selection import train_test_split

# Load and normalize data
normalizer = UFCDataNormalizer()
normalizer.load_data()
normalizer.handle_missing_values()

# Get feature-engineered dataset
df = normalizer.create_feature_engineered_dataset()
```

### 2. Feature Selection Strategy

**A. Pre-fight Features Only (No Data Leakage)**
These are features known BEFORE the fight:
- Fighter statistics (_total columns)
- Physical attributes (height, weight, reach, age)
- Career records (wins, losses)
- Calculated differentials
- Engineered features (win_rate, BMI, efficiency scores)

**B. Features to EXCLUDE (In-fight statistics)**
These create data leakage:
- r_kd, b_kd (knockdowns in THIS fight)
- r_sig_str, b_sig_str (strikes in THIS fight)
- r_td, b_td (takedowns in THIS fight)
- Any column without "_total" suffix that's fight-specific

**C. Target Variables**
Depending on your prediction goal:
- `winner`: Classification (Red/Blue/Draw)
- `method`: Multi-class (KO/TKO, Submission, Decision)
- `finish_round`: Regression (which round fight ends)
- `time_sec`: Regression (fight duration)

### 3. Feature Engineering Layer

```python
def create_ml_features(df):
    """
    Create ML-ready features from normalized data
    """
    features = pd.DataFrame()
    
    # Basic differentials
    features['win_rate_diff'] = df['r_win_rate'] - df['b_win_rate']
    features['experience_diff'] = df['experience_diff']
    features['age_diff'] = df['age_diff']
    features['height_diff'] = df['height_diff']
    features['weight_diff'] = df['weight_diff']
    features['reach_diff'] = df['reach_diff']
    
    # Performance differentials
    features['striking_eff_diff'] = df['striking_efficiency_diff']
    features['grappling_eff_diff'] = df['grappling_efficiency_diff']
    features['defensive_rating_diff'] = df['defensive_rating_diff']
    
    # Fighter style indicators
    features['r_striker_score'] = df['r_SLpM_total'] * df['r_sig_str_acc_total']
    features['b_striker_score'] = df['b_SLpM_total'] * df['b_sig_str_acc_total']
    features['striker_advantage'] = features['r_striker_score'] - features['b_striker_score']
    
    features['r_grappler_score'] = df['r_td_avg'] * df['r_td_acc_total']
    features['b_grappler_score'] = df['b_td_avg'] * df['b_td_acc_total']
    features['grappler_advantage'] = features['r_grappler_score'] - features['b_grappler_score']
    
    # Physical advantages
    features['bmi_diff'] = df['bmi_diff']
    
    # Categorical features (encoded)
    features['r_stance_encoded'] = df['r_stance_encoded']
    features['b_stance_encoded'] = df['b_stance_encoded']
    features['is_title_bout'] = df['is_title_bout']
    features['weight_class_encoded'] = df['weight_class_encoded']
    
    return features
```

### 4. Train/Test Split Strategy

**Option A: Random Split (Simple)**
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

**Option B: Temporal Split (Recommended)**
```python
# Split by date to prevent temporal leakage
# Use older fights for training, recent fights for testing
df['event_date'] = pd.to_datetime(df['event_date'])
train_df = df[df['event_date'] < '2023-01-01']
test_df = df[df['event_date'] >= '2023-01-01']
```

**Option C: Fighter-based Split**
```python
# Ensure fighters in test set weren't in training
# More realistic for predicting new fighters
```

### 5. Model Selection

**A. Binary Classification (Winner Prediction)**

**Models to try:**
1. **XGBoost Classifier** (Recommended)
   - Handles non-linear relationships
   - Built-in feature importance
   - Robust to outliers
   
2. **Random Forest**
   - Good for feature interactions
   - Less prone to overfitting
   
3. **Logistic Regression**
   - Baseline model
   - Interpretable coefficients
   
4. **Neural Network**
   - Can capture complex patterns
   - Requires more data

**B. Multi-class Classification (Method Prediction)**
Same models as above, configured for multi-class

**C. Regression (Fight Duration)**
- XGBoost Regressor
- Random Forest Regressor
- Linear Regression (baseline)

### 6. Hyperparameter Tuning

**XGBoost Example:**
```python
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.8, 0.9, 1.0],
    'colsample_bytree': [0.8, 0.9, 1.0],
    'min_child_weight': [1, 3, 5]
}

grid_search = GridSearchCV(
    XGBClassifier(),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
```

### 7. Model Evaluation

**Metrics to track:**

**Classification:**
- Accuracy
- Precision/Recall/F1-score
- ROC-AUC
- Confusion Matrix
- Class-wise performance

**Regression:**
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² score

**Feature Importance:**
- SHAP values
- Permutation importance
- Built-in feature importance

### 8. Cross-Validation Strategy

**Time-Series CV (Recommended):**
```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, val_idx in tscv.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    # Train and evaluate
```

### 9. Ensemble Methods

Combine multiple models:
```python
# Voting Classifier
ensemble = VotingClassifier(
    estimators=[
        ('xgb', xgb_model),
        ('rf', rf_model),
        ('lr', lr_model)
    ],
    voting='soft'
)
```

### 10. Model Interpretation

**SHAP Analysis:**
```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test)

# Individual prediction explanation
shap.force_plot(explainer.expected_value, 
                shap_values[0], X_test.iloc[0])
```

## Complete Pipeline Example

```python
class UFCMLPipeline:
    def __init__(self):
        self.normalizer = UFCDataNormalizer()
        self.models = {}
        self.scalers = {}
        
    def prepare_data(self):
        # Load and normalize
        self.normalizer.load_data()
        self.normalizer.handle_missing_values()
        self.df = self.normalizer.create_feature_engineered_dataset()
        
        # Create features
        self.X = create_ml_features(self.df)
        self.y = (self.df['winner'] == 'Red').astype(int)
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(self.X, self.y, test_size=0.2, 
                           random_state=42, stratify=self.y)
    
    def train_models(self):
        # Train multiple models
        self.models['xgb'] = XGBClassifier()
        self.models['rf'] = RandomForestClassifier()
        
        for name, model in self.models.items():
            model.fit(self.X_train, self.y_train)
            
    def evaluate(self):
        for name, model in self.models.items():
            y_pred = model.predict(self.X_test)
            accuracy = accuracy_score(self.y_test, y_pred)
            print(f"{name} accuracy: {accuracy:.3f}")
```

## Pipeline Outputs

1. **Trained Models**: Serialized models ready for predictions
2. **Feature Importance**: Which stats matter most
3. **Performance Metrics**: How well models predict
4. **Prediction API**: Interface for making new predictions
5. **Visualization Dashboard**: Interactive results exploration

## Next Steps After Pipeline

1. **Model Deployment**: Create REST API for predictions
2. **Monitoring**: Track model performance over time
3. **Retraining**: Update models with new fight data
4. **A/B Testing**: Compare model versions
5. **Production Integration**: Connect to live data sources

## Advantages of This Pipeline

1. **No Data Leakage**: Only uses pre-fight information
2. **Reproducible**: Clear steps from data to predictions
3. **Scalable**: Easy to add new features or models
4. **Interpretable**: SHAP values explain predictions
5. **Validated**: Cross-validation ensures robustness
6. **Production-Ready**: Can be deployed to production

## Common Pitfalls to Avoid

1. ❌ Using in-fight statistics for pre-fight predictions
2. ❌ Not handling temporal ordering in data
3. ❌ Ignoring class imbalance
4. ❌ Overfitting on small datasets
5. ❌ Not validating on truly held-out data
6. ❌ Forgetting to scale features consistently
7. ❌ Not checking for data leakage