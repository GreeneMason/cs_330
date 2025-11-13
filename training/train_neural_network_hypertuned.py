"""
Hyperparameter Tuning for Fighter-Aware Neural Network
Implements Step 3 from the Neural Network Training Guide
"""

import pandas as pd
import numpy as np
import tensorflow as tf
import keras_tuner as kt
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
import warnings
import json
from datetime import datetime
warnings.filterwarnings('ignore')


class HyperparameterTunedNeuralNetwork:
    """Neural network with automated hyperparameter tuning"""
    
    def __init__(self, data_path='../data/event_normalized_large_dataset.csv', 
                 events_path='../data/events_reference.csv'):
        self.data_path = data_path
        self.events_path = events_path
        self.best_model = None
        self.feature_columns = None
        self.red_features = None
        self.blue_features = None
        self.diff_features = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.tuner = None
        
        # Directories
        self.model_dir = Path('../models/neural_network')
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.tuning_dir = Path('../models/neural_network/tuning')
        self.tuning_dir.mkdir(parents=True, exist_ok=True)
        self.viz_dir = Path('../visualizations/neural_network')
        self.viz_dir.mkdir(parents=True, exist_ok=True)
        
    def load_data(self):
        """Load the event-normalized dataset"""
        print("\n" + "="*60)
        print("LOADING DATA FOR HYPERPARAMETER TUNING")
        print("="*60)
        
        print(f"Loading fights from: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df)} fights")
        
        print(f"Loading events from: {self.events_path}")
        self.events_df = pd.read_csv(self.events_path)
        print(f"Loaded {len(self.events_df)} unique events")
        
        # Display basic info
        print(f"Dataset shape: {self.df.shape}")
        print(f"Missing values: {self.df.isnull().sum().sum()}")
        
        target_counts = self.df['winner'].value_counts()
        print(f"Target distribution:")
        for winner, count in target_counts.items():
            print(f"  - {winner}: {count} ({count/len(self.df)*100:.1f}%)")
    
    def identify_fighter_features(self):
        """Identify and categorize features for fighter-aware processing"""
        print("\n" + "="*60)
        print("CATEGORIZING FEATURES FOR TUNABLE ARCHITECTURE")
        print("="*60)
        
        # Exclude non-feature columns AND string columns that have encoded versions
        excluded_cols = ['event_id', 'r_fighter', 'b_fighter', 'winner', 
                        'method', 'referee', 'gender', 'weight_class', 'winner_encoded',
                        'r_stance', 'b_stance']  # Exclude raw stance strings, use encoded versions
        
        all_features = [col for col in self.df.columns if col not in excluded_cols]
        
        # Only include numeric columns (exclude any remaining object columns)
        numeric_features = []
        for col in all_features:
            if self.df[col].dtype in ['int64', 'float64']:
                numeric_features.append(col)
            else:
                print(f"⚠️  Excluding non-numeric column: {col} (dtype: {self.df[col].dtype})")
        
        all_features = numeric_features
        
        # Categorize features
        self.red_features = [col for col in all_features if col.startswith('r_')]
        self.blue_features = [col for col in all_features if col.startswith('b_')]
        self.diff_features = [col for col in all_features if col.endswith('_diff')]
        
        # Other features
        encoded_features = [col for col in all_features 
                          if col.endswith('_encoded') and not col.startswith(('r_', 'b_'))]
        other_features = [col for col in all_features 
                         if col not in self.red_features + self.blue_features + 
                            self.diff_features + encoded_features]
        
        print(f"Red fighter features: {len(self.red_features)}")
        print(f"Blue fighter features: {len(self.blue_features)}")
        print(f"Differential features: {len(self.diff_features)}")
        print(f"Encoded categorical: {len(encoded_features)}")
        print(f"Other features: {len(other_features)}")
        
        # Store all features
        self.feature_columns = (self.red_features + self.blue_features + 
                               self.diff_features + encoded_features + other_features)
        
        print(f"Total features for tuning: {len(self.feature_columns)}")
        
        # Verify all features are numeric
        non_numeric = [col for col in self.feature_columns if self.df[col].dtype not in ['int64', 'float64']]
        if non_numeric:
            print(f"⚠️  Warning: Non-numeric features found: {non_numeric}")
        else:
            print("✓ All features are numeric")
        
    def prepare_features(self):
        """Prepare features for hyperparameter tuning"""
        print("\n" + "="*60)
        print("PREPARING FEATURES FOR HYPERPARAMETER TUNING")
        print("="*60)
        
        self.identify_fighter_features()
        
        # Prepare feature matrix
        X = self.df[self.feature_columns].copy()
        y = self.df['winner'].copy()
        
        # Handle missing values
        if X.isnull().any().any():
            print("Filling missing values with column medians")
            X = X.fillna(X.median())
        
        # Encode target variable
        y_encoded = self.label_encoder.fit_transform(y)
        
        print(f"Target classes: {list(self.label_encoder.classes_)}")
        print(f"Feature matrix shape: {X.shape}")
        
        return X, y_encoded
    
    def build_tuned_fighter_aware_model(self, hp):
        """Build tunable fighter-aware model with hyperparameter optimization"""
        
        # Calculate feature dimensions
        red_dim = len(self.red_features)
        blue_dim = len(self.blue_features)
        other_dim = len(self.feature_columns) - red_dim - blue_dim
        total_dim = len(self.feature_columns)
        
        # Input layer
        inputs = tf.keras.Input(shape=(total_dim,), name='combined_input')
        
        # Split features
        red_features_input = tf.keras.layers.Lambda(
            lambda x: x[:, :red_dim], name='red_features_split'
        )(inputs)
        
        blue_features_input = tf.keras.layers.Lambda(
            lambda x: x[:, red_dim:red_dim+blue_dim], name='blue_features_split'
        )(inputs)
        
        other_features_input = tf.keras.layers.Lambda(
            lambda x: x[:, red_dim+blue_dim:], name='other_features_split'
        )(inputs)
        
        # Tunable red fighter processing
        red_units_1 = hp.Int('red_units_1', min_value=32, max_value=128, step=16)
        red_units_2 = hp.Int('red_units_2', min_value=16, max_value=64, step=8)
        red_dropout_1 = hp.Float('red_dropout_1', min_value=0.0, max_value=0.5, step=0.1)
        red_dropout_2 = hp.Float('red_dropout_2', min_value=0.0, max_value=0.4, step=0.1)
        
        red_processed = tf.keras.layers.Dense(red_units_1, activation='relu')(red_features_input)
        red_processed = tf.keras.layers.Dropout(red_dropout_1)(red_processed)
        red_processed = tf.keras.layers.Dense(red_units_2, activation='relu')(red_processed)
        if hp.Boolean('red_batch_norm'):
            red_processed = tf.keras.layers.BatchNormalization()(red_processed)
        red_processed = tf.keras.layers.Dropout(red_dropout_2)(red_processed)
        
        # Tunable blue fighter processing (symmetric to red)
        blue_units_1 = hp.Int('blue_units_1', min_value=32, max_value=128, step=16)
        blue_units_2 = hp.Int('blue_units_2', min_value=16, max_value=64, step=8)
        blue_dropout_1 = hp.Float('blue_dropout_1', min_value=0.0, max_value=0.5, step=0.1)
        blue_dropout_2 = hp.Float('blue_dropout_2', min_value=0.0, max_value=0.4, step=0.1)
        
        blue_processed = tf.keras.layers.Dense(blue_units_1, activation='relu')(blue_features_input)
        blue_processed = tf.keras.layers.Dropout(blue_dropout_1)(blue_processed)
        blue_processed = tf.keras.layers.Dense(blue_units_2, activation='relu')(blue_processed)
        if hp.Boolean('blue_batch_norm'):
            blue_processed = tf.keras.layers.BatchNormalization()(blue_processed)
        blue_processed = tf.keras.layers.Dropout(blue_dropout_2)(blue_processed)
        
        # Tunable other features processing
        other_units = hp.Int('other_units', min_value=16, max_value=64, step=8)
        other_dropout = hp.Float('other_dropout', min_value=0.0, max_value=0.4, step=0.1)
        
        other_processed = tf.keras.layers.Dense(other_units, activation='relu')(other_features_input)
        other_processed = tf.keras.layers.Dropout(other_dropout)(other_processed)
        
        # Combine features
        combined = tf.keras.layers.Concatenate()([red_processed, blue_processed, other_processed])
        
        # Tunable decision layers
        num_decision_layers = hp.Int('num_decision_layers', min_value=2, max_value=4)
        
        x = combined
        for i in range(num_decision_layers):
            units = hp.Int(f'decision_units_{i}', min_value=32, max_value=256, step=32)
            dropout = hp.Float(f'decision_dropout_{i}', min_value=0.1, max_value=0.5, step=0.1)
            
            x = tf.keras.layers.Dense(units, activation='relu')(x)
            if hp.Boolean(f'decision_batch_norm_{i}'):
                x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.Dropout(dropout)(x)
        
        # Output layer
        outputs = tf.keras.layers.Dense(1, activation='sigmoid', name='winner_prediction')(x)
        
        # Create model
        model = tf.keras.Model(inputs=inputs, outputs=outputs, name='TunedFighterAwarePredictor')
        
        # Tunable optimizer settings
        learning_rate = hp.Float('learning_rate', min_value=1e-4, max_value=1e-2, sampling='LOG')
        optimizer_choice = hp.Choice('optimizer', ['adam', 'rmsprop'])
        
        if optimizer_choice == 'adam':
            optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        else:
            optimizer = tf.keras.optimizers.RMSprop(learning_rate=learning_rate)
        
        # Compile model
        model.compile(
            optimizer=optimizer,
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def run_hyperparameter_search(self, X, y, max_trials=30, epochs_per_trial=50):
        """Run hyperparameter search using Keras Tuner"""
        print("\n" + "="*60)
        print("RUNNING HYPERPARAMETER SEARCH")
        print("="*60)
        
        # Split data for tuning
        X_tune, X_val, y_tune, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_tune_scaled = self.scaler.fit_transform(X_tune)
        X_val_scaled = self.scaler.transform(X_val)
        
        print(f"Tuning set: {len(X_tune)} samples")
        print(f"Validation set: {len(X_val)} samples")
        print(f"Max trials: {max_trials}")
        print(f"Epochs per trial: {epochs_per_trial}")
        
        # Create tuner
        self.tuner = kt.RandomSearch(
            self.build_tuned_fighter_aware_model,
            objective='val_accuracy',
            max_trials=max_trials,
            directory=self.tuning_dir,
            project_name='ufc_fighter_aware_tuning',
            overwrite=True  # Start fresh
        )
        
        # Define callbacks for each trial
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=15,
            restore_best_weights=True
        )
        
        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=8,
            min_lr=1e-6
        )
        
        print("\nStarting hyperparameter search...")
        print("This may take a while depending on max_trials and epochs_per_trial")
        
        # Run the search
        self.tuner.search(
            X_tune_scaled, y_tune,
            validation_data=(X_val_scaled, y_val),
            epochs=epochs_per_trial,
            batch_size=32,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        # Get best hyperparameters
        best_hps = self.tuner.get_best_hyperparameters(num_trials=1)[0]
        
        print("\n" + "="*60)
        print("BEST HYPERPARAMETERS FOUND")
        print("="*60)
        
        # Display best hyperparameters
        print("Fighter processing:")
        print(f"  Red fighter units: {best_hps.get('red_units_1')} -> {best_hps.get('red_units_2')}")
        print(f"  Blue fighter units: {best_hps.get('blue_units_1')} -> {best_hps.get('blue_units_2')}")
        print(f"  Other features units: {best_hps.get('other_units')}")
        
        print("Decision layers:")
        num_layers = best_hps.get('num_decision_layers')
        print(f"  Number of layers: {num_layers}")
        for i in range(num_layers):
            units = best_hps.get(f'decision_units_{i}')
            dropout = best_hps.get(f'decision_dropout_{i}')
            batch_norm = best_hps.get(f'decision_batch_norm_{i}')
            print(f"  Layer {i+1}: {units} units, {dropout:.1f} dropout, batch_norm: {batch_norm}")
        
        print("Training:")
        print(f"  Learning rate: {best_hps.get('learning_rate'):.1e}")
        print(f"  Optimizer: {best_hps.get('optimizer')}")
        
        # Get best model
        self.best_model = self.tuner.get_best_models(num_models=1)[0]
        
        # Save hyperparameters
        hp_dict = {param: best_hps.get(param) for param in best_hps.space}
        with open(self.model_dir / 'best_hyperparameters.json', 'w') as f:
            json.dump(hp_dict, f, indent=2, default=str)
        
        return best_hps
    
    def evaluate_best_model(self, X_test, y_test):
        """Evaluate the best model found by hyperparameter tuning"""
        print("\n" + "="*60)
        print("EVALUATING BEST TUNED MODEL")
        print("="*60)
        
        if self.best_model is None:
            print("No model available for evaluation")
            return None
        
        # Scale test data
        X_test_scaled = self.scaler.transform(X_test)
        
        # Make predictions
        y_pred_proba = self.best_model.predict(X_test_scaled)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Test Accuracy: {accuracy:.4f}")
        
        # Classification report
        class_names = self.label_encoder.classes_
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=class_names))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.title('Hyperparameter Tuned Neural Network - Confusion Matrix')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'tuned_model_confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'accuracy': accuracy,
            'y_pred_proba': y_pred_proba,
            'y_pred': y_pred,
            'classification_report': classification_report(y_test, y_pred, target_names=class_names)
        }
    
    def save_best_model(self, results):
        """Save the best tuned model and all components"""
        print("\n" + "="*60)
        print("SAVING BEST TUNED MODEL")
        print("="*60)
        
        if self.best_model is None:
            print("No model to save")
            return
        
        # Save the tuned model
        model_path = self.model_dir / 'best_tuned_neural_network_model.h5'
        self.best_model.save(model_path)
        print(f"Saved tuned model to: {model_path}")
        
        # Save preprocessing components
        scaler_path = self.model_dir / 'tuned_neural_network_scaler.pkl'
        joblib.dump(self.scaler, scaler_path)
        print(f"Saved scaler to: {scaler_path}")
        
        encoder_path = self.model_dir / 'tuned_neural_network_label_encoder.pkl'
        joblib.dump(self.label_encoder, encoder_path)
        print(f"Saved label encoder to: {encoder_path}")
        
        features_path = self.model_dir / 'tuned_neural_network_features.pkl'
        joblib.dump(self.feature_columns, features_path)
        print(f"Saved feature list to: {features_path}")
        
        # Save metadata
        metadata = {
            'model_type': 'hyperparameter_tuned_fighter_aware_neural_network',
            'num_features': len(self.feature_columns),
            'red_features': len(self.red_features),
            'blue_features': len(self.blue_features),
            'diff_features': len(self.diff_features),
            'test_accuracy': float(results['accuracy']),
            'training_date': datetime.now().isoformat(),
            'model_parameters': int(self.best_model.count_params()),
            'tuning_trials': len(self.tuner.oracle.trials) if self.tuner else 0
        }
        
        metadata_path = self.model_dir / 'tuned_neural_network_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Saved metadata to: {metadata_path}")
    
    def run_complete_hyperparameter_tuning(self, max_trials=30, epochs_per_trial=50):
        """Run the complete hyperparameter tuning pipeline"""
        print("🔧 HYPERPARAMETER TUNING PIPELINE")
        print("Fighter-Aware Neural Network Optimization")
        print("=" * 80)
        
        # Load and prepare data
        self.load_data()
        X, y = self.prepare_features()
        
        # Split data for final test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nFinal train/test split:")
        print(f"Training set (for tuning): {len(X_train)} samples")
        print(f"Test set (for final evaluation): {len(X_test)} samples")
        
        # Run hyperparameter search
        best_hps = self.run_hyperparameter_search(X_train, y_train, max_trials, epochs_per_trial)
        
        # Evaluate best model
        results = self.evaluate_best_model(X_test, y_test)
        
        # Save everything
        self.save_best_model(results)
        
        print("\n" + "="*80)
        print("🎉 HYPERPARAMETER TUNING COMPLETE!")
        print("="*80)
        print(f"Best test accuracy: {results['accuracy']:.4f}")
        print(f"Total trials run: {len(self.tuner.oracle.trials)}")
        print(f"Model parameters: {self.best_model.count_params():,}")
        print(f"Tuned model saved to: {self.model_dir}")
        
        return results, best_hps


def main():
    """Main hyperparameter tuning function"""
    # Create tuner with customizable parameters
    tuner = HyperparameterTunedNeuralNetwork()
    
    # Run tuning with specified parameters
    # Adjust max_trials and epochs_per_trial based on available time/compute
    results, best_hps = tuner.run_complete_hyperparameter_tuning(
        max_trials=20,  # Reduced for faster testing - increase for better results
        epochs_per_trial=30  # Reduced for faster testing - increase for better results
    )
    
    print(f"\nHyperparameter tuning completed!")
    print(f"Best accuracy: {results['accuracy']:.4f}")


if __name__ == "__main__":
    main()