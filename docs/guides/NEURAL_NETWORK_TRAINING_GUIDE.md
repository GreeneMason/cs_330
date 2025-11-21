# Neural Network Model Training Guide

## Overview

This guide outlines the steps to create a neural network model using the event-normalized large dataset that maintains the same interface as the current decision tree/ensemble models, enabling direct comparison between approaches.

## Current Architecture Analysis

### Existing Model Structure
- **Dataset**: `data/event_normalized_large_dataset.csv` (7,440 fights)
- **Features**: 87 columns including fighter stats, differentials, and encoded categorical variables
- **Target**: `winner_encoded` (0=Blue, 1=Red)
- **Models**: XGBoost, Random Forest, Logistic Regression with grid search
- **Interface**: `EventNormalizedUFCPredictor` class with consistent API

### Key Interface Components
1. **Training**: `train_event_normalized_model.py` - trains models and saves artifacts
2. **Prediction**: `predict_event_normalized.py` - loads models and provides interactive interface
3. **Artifacts**: Models saved to `models/` with consistent naming convention
4. **Features**: Automatic feature selection and scaling

## Neural Network Implementation Plan

### Step 1: Environment Setup

#### Additional Dependencies
Add to `requirements.txt`:
```
tensorflow>=2.13.0
keras-tuner>=1.4.0
tensorboard>=2.13.0
```

#### Installation Command
```powershell
pip install tensorflow keras-tuner tensorboard
```

### Step 2: Neural Network Training Script

Create `train_neural_network_model.py` with the following structure:

#### Class Architecture
```python
class EventNormalizedNeuralNetwork:
    """Neural network predictor using event-normalized data"""
    
    def __init__(self, data_path='data/event_normalized_large_dataset.csv', 
                 events_path='data/events_reference.csv'):
        # Maintain same initialization as existing predictor
        self.data_path = data_path
        self.events_path = events_path
        self.model = None
        self.best_model = None
        self.feature_columns = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        
        # Neural network specific
        self.model_dir = Path('models/neural_network')
        self.model_dir.mkdir(parents=True, exist_ok=True)
```

#### Neural Network Architecture Options

**Option 1: Simple Dense Network**
```python
def create_simple_model(self, input_dim):
    """Create a simple feedforward neural network"""
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(input_dim,)),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    return model
```

**Option 2: Advanced Architecture with Batch Normalization**
```python
def create_advanced_model(self, input_dim):
    """Create an advanced neural network with batch normalization"""
    inputs = tf.keras.Input(shape=(input_dim,))
    
    # Feature extraction layers
    x = tf.keras.layers.Dense(256, activation='relu')(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.4)(x)
    
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    
    # Output layer
    outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model
```

**Option 3: Fighter-Specific Feature Processing**
```python
def create_fighter_aware_model(self, input_dim):
    """Create a model that processes red and blue fighter features separately"""
    inputs = tf.keras.Input(shape=(input_dim,))
    
    # Assume first half of features are red fighter, second half are blue fighter
    red_features = tf.keras.layers.Lambda(lambda x: x[:, :input_dim//2])(inputs)
    blue_features = tf.keras.layers.Lambda(lambda x: x[:, input_dim//2:])(inputs)
    
    # Separate processing for each fighter
    red_processed = tf.keras.layers.Dense(64, activation='relu')(red_features)
    blue_processed = tf.keras.layers.Dense(64, activation='relu')(blue_features)
    
    # Combine features
    combined = tf.keras.layers.Concatenate()([red_processed, blue_processed])
    
    x = tf.keras.layers.Dense(128, activation='relu')(combined)
    x = tf.keras.layers.Dropout(0.3)(x)
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    
    outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model
```

### Step 3: Hyperparameter Tuning with Keras Tuner

#### Tuner Configuration
```python
def build_tuned_model(self, hp, input_dim):
    """Build model with hyperparameter tuning"""
    model = tf.keras.Sequential()
    
    # Tunable architecture
    model.add(tf.keras.layers.Dense(
        hp.Int('first_dense', 64, 512, step=64),
        activation='relu',
        input_shape=(input_dim,)
    ))
    model.add(tf.keras.layers.Dropout(hp.Float('first_dropout', 0.0, 0.5, step=0.1)))
    
    # Variable number of hidden layers
    for i in range(hp.Int('num_layers', 1, 4)):
        model.add(tf.keras.layers.Dense(
            hp.Int(f'dense_{i}', 32, 256, step=32),
            activation='relu'
        ))
        model.add(tf.keras.layers.Dropout(hp.Float(f'dropout_{i}', 0.0, 0.4, step=0.1)))
    
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    
    # Tunable optimizer
    model.compile(
        optimizer=tf.keras.optimizers.Adam(hp.Float('learning_rate', 1e-4, 1e-2, sampling='LOG')),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model
```

### Step 4: Training Pipeline

#### Data Preparation (Same as Existing)
```python
def prepare_features(self):
    """Prepare features using same logic as existing model"""
    # Reuse existing feature selection logic
    excluded_cols = ['event_id', 'r_fighter', 'b_fighter', 'winner', 
                     'method', 'referee', 'gender', 'weight_class']
    
    self.feature_columns = [col for col in self.df.columns 
                           if col not in excluded_cols]
    
    X = self.df[self.feature_columns].copy()
    y = self.df['winner_encoded'].copy()
    
    # Same preprocessing as existing model
    X = X.fillna(X.median())
    
    return X, y
```

#### Training Methods
```python
def train_with_cross_validation(self, X, y, model_type='simple'):
    """Train with k-fold cross validation"""
    from sklearn.model_selection import StratifiedKFold
    
    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    fold_scores = []
    
    for fold, (train_idx, val_idx) in enumerate(kfold.split(X, y)):
        print(f"Training fold {fold + 1}/5")
        
        X_train_fold, X_val_fold = X.iloc[train_idx], X.iloc[val_idx]
        y_train_fold, y_val_fold = y.iloc[train_idx], y.iloc[val_idx]
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train_fold)
        X_val_scaled = self.scaler.transform(X_val_fold)
        
        # Create and train model
        model = self.create_model(X_train_scaled.shape[1], model_type)
        
        early_stopping = tf.keras.callbacks.EarlyStopping(
            patience=20, restore_best_weights=True
        )
        
        history = model.fit(
            X_train_scaled, y_train_fold,
            validation_data=(X_val_scaled, y_val_fold),
            epochs=200,
            batch_size=32,
            callbacks=[early_stopping],
            verbose=0
        )
        
        val_score = model.evaluate(X_val_scaled, y_val_fold, verbose=0)[1]
        fold_scores.append(val_score)
        
    return np.mean(fold_scores), np.std(fold_scores)

def train_with_hyperparameter_tuning(self, X, y):
    """Train with automated hyperparameter tuning"""
    import keras_tuner as kt
    
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    X_train_scaled = self.scaler.fit_transform(X_train)
    X_val_scaled = self.scaler.transform(X_val)
    
    # Create tuner
    tuner = kt.RandomSearch(
        lambda hp: self.build_tuned_model(hp, X_train_scaled.shape[1]),
        objective='val_accuracy',
        max_trials=20,
        directory='models/neural_network',
        project_name='ufc_nn_tuning'
    )
    
    # Search for best hyperparameters
    tuner.search(
        X_train_scaled, y_train,
        validation_data=(X_val_scaled, y_val),
        epochs=100,
        batch_size=32,
        callbacks=[tf.keras.callbacks.EarlyStopping(patience=10)]
    )
    
    # Get best model
    best_model = tuner.get_best_models()[0]
    return best_model
```

### Step 5: Model Comparison Framework

#### Evaluation Metrics (Same as Existing)
```python
def evaluate_model(self, model, X_test, y_test):
    """Evaluate model using same metrics as existing models"""
    y_pred_proba = model.predict(X_test)
    y_pred = (y_pred_proba > 0.5).astype(int)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'classification_report': classification_report(y_test, y_pred),
        'confusion_matrix': confusion_matrix(y_test, y_pred)
    }
    
    return metrics, y_pred_proba
```

### Step 6: Modified Prediction Interface

#### Neural Network Predictor Class
```python
class EventNormalizedNeuralNetworkPredictor:
    """Neural network predictor with same interface as existing predictor"""
    
    def __init__(self):
        self.model_dir = Path('models/neural_network')
        self.data_dir = Path('data')
        self.model = None
        self.scaler = None
        self.feature_columns = None
        # Maintain same interface methods as existing predictor
    
    def load_model(self):
        """Load neural network model with same signature"""
        try:
            self.model = tf.keras.models.load_model(
                self.model_dir / 'best_neural_network_model.h5'
            )
            self.scaler = joblib.load(
                self.model_dir / 'neural_network_scaler.pkl'
            )
            self.feature_columns = joblib.load(
                self.model_dir / 'neural_network_features.pkl'
            )
            return True
        except Exception as e:
            print(f"❌ Error loading neural network model: {e}")
            return False
    
    # Same interface methods as existing predictor:
    # - predict_fight_interactive()
    # - predict_from_event()
    # - predict_manual_entry()
    # - predict_quick()
    # - browse_events()
```

### Step 7: Model Comparison Script

#### Create `compare_models.py`
```python
def compare_decision_tree_vs_neural_network():
    """Compare decision tree ensemble vs neural network models"""
    
    # Load both models
    dt_predictor = EventNormalizedUFCPredictor()
    nn_predictor = EventNormalizedNeuralNetworkPredictor()
    
    # Load test data
    test_data = load_test_dataset()
    
    # Get predictions from both models
    dt_predictions = dt_predictor.predict_batch(test_data)
    nn_predictions = nn_predictor.predict_batch(test_data)
    
    # Compare metrics
    comparison_results = {
        'decision_tree': calculate_metrics(dt_predictions),
        'neural_network': calculate_metrics(nn_predictions)
    }
    
    # Visualize comparison
    create_comparison_plots(comparison_results)
    
    return comparison_results
```

### Step 8: File Structure

```
models/
├── neural_network/
│   ├── best_neural_network_model.h5
│   ├── neural_network_scaler.pkl
│   ├── neural_network_features.pkl
│   ├── training_history.json
│   └── model_architecture.png
├── decision_tree/ (existing models)
│   ├── event_normalized_best_model.pkl
│   ├── event_normalized_scaler.pkl
│   └── ...
```

### Step 9: Execution Steps

1. **Install Dependencies**
   ```powershell
   pip install tensorflow keras-tuner tensorboard
   ```

2. **Train Neural Network Model**
   ```powershell
   python train_neural_network_model.py
   ```

3. **Test Neural Network Predictor**
   ```powershell
   python predict_neural_network.py
   ```

4. **Compare Models**
   ```powershell
   python compare_models.py
   ```

### Step 10: Advanced Features to Implement

#### TensorBoard Integration
```python
def setup_tensorboard_logging(self, log_dir='logs/neural_network'):
    """Set up TensorBoard logging for training visualization"""
    return [
        tf.keras.callbacks.TensorBoard(
            log_dir=log_dir,
            histogram_freq=1,
            write_graph=True,
            write_images=True
        )
    ]
```

#### Feature Importance Analysis
```python
def analyze_feature_importance(self, model, X_test, y_test):
    """Analyze feature importance using SHAP"""
    import shap
    
    explainer = shap.DeepExplainer(model, X_test[:100])
    shap_values = explainer.shap_values(X_test[:100])
    
    # Create SHAP plots
    shap.summary_plot(shap_values, X_test[:100], 
                      feature_names=self.feature_columns)
```

#### Model Ensemble
```python
def create_ensemble_predictor(self):
    """Combine decision tree and neural network predictions"""
    dt_pred = self.dt_model.predict_proba(X)[:, 1]
    nn_pred = self.nn_model.predict(X).flatten()
    
    # Weighted average (can be optimized)
    ensemble_pred = 0.6 * dt_pred + 0.4 * nn_pred
    return ensemble_pred
```

## Benefits of This Approach

1. **Direct Comparison**: Same data preprocessing and evaluation metrics
2. **Consistent Interface**: Users can switch between models seamlessly
3. **Comprehensive Evaluation**: Multiple neural network architectures tested
4. **Production Ready**: Same artifact saving and loading patterns
5. **Extensible**: Easy to add more model types to comparison

## Expected Performance Improvements

- **Complex Pattern Recognition**: Neural networks may capture non-linear relationships better
- **Feature Interaction Learning**: Automatic feature interaction discovery
- **Scalability**: Better performance on larger datasets
- **Ensemble Potential**: Can combine with existing models for improved accuracy

## Next Steps After Implementation

1. Train both models on same data splits
2. Compare accuracy, precision, recall on test set
3. Analyze feature importance differences
4. Test on new fight data
5. Optimize ensemble combination weights
6. Deploy best performing model configuration