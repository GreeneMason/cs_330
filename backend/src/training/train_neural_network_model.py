"""
Neural Network Pipeline for UFC Fight Prediction
Uses fighter-aware architecture that processes red and blue fighter features separately
Compatible with existing event-normalized dataset interface
"""

import pandas as pd
import numpy as np
import tensorflow as tf
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


class EventNormalizedNeuralNetwork:
    """Neural network predictor using event-normalized data with fighter-aware architecture"""
    
    def __init__(self, data_path='../../shared/data/event_normalized_large_dataset.csv', 
                 events_path='data/events_reference.csv'):
        self.data_path = data_path
        self.events_path = events_path
        self.model = None
        self.best_model = None
        self.feature_columns = None
        self.red_features = None
        self.blue_features = None
        self.diff_features = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        
        # Neural network specific directories
        self.model_dir = Path('models/neural_network')
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Visualization directory
        self.viz_dir = Path('visualizations/neural_network')
        self.viz_dir.mkdir(parents=True, exist_ok=True)
        
    def load_data(self):
        """Load the event-normalized dataset"""
        print("\n" + "="*60)
        print("LOADING EVENT-NORMALIZED DATA FOR NEURAL NETWORK")
        print("="*60)
        
        print(f"Loading fights from: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        print(f"✓ Loaded {len(self.df)} fights")
        
        print(f"Loading events from: {self.events_path}")
        self.events_df = pd.read_csv(self.events_path)
        print(f"✓ Loaded {len(self.events_df)} unique events")
        
        # Display basic dataset info
        print(f"\nDataset shape: {self.df.shape}")
        print(f"Missing values: {self.df.isnull().sum().sum()}")
        
        # Show target distribution
        target_counts = self.df['winner'].value_counts()
        print(f"\nTarget distribution:")
        for winner, count in target_counts.items():
            print(f"  - {winner}: {count} ({count/len(self.df)*100:.1f}%)")
    
    def identify_fighter_features(self):
        """Identify and categorize red fighter, blue fighter, and differential features"""
        print("\n" + "="*60)
        print("ANALYZING FIGHTER-SPECIFIC FEATURES")
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
        
        # Encoded categorical features (not fighter-specific)
        encoded_features = [col for col in all_features 
                          if col.endswith('_encoded') and not col.startswith(('r_', 'b_'))]
        
        # Other features (like is_title_bout, finish_round, etc.)
        other_features = [col for col in all_features 
                         if col not in self.red_features + self.blue_features + 
                            self.diff_features + encoded_features]
        
        print(f"Red fighter features: {len(self.red_features)}")
        print(f"Blue fighter features: {len(self.blue_features)}")
        print(f"Differential features: {len(self.diff_features)}")
        print(f"Encoded categorical: {len(encoded_features)}")
        print(f"Other features: {len(other_features)}")
        
        # Store feature categorization
        self.feature_categories = {
            'red_features': self.red_features,
            'blue_features': self.blue_features,
            'diff_features': self.diff_features,
            'encoded_features': encoded_features,
            'other_features': other_features
        }
        
        # All features for the model
        self.feature_columns = (self.red_features + self.blue_features + 
                               self.diff_features + encoded_features + other_features)
        
        print(f"\nTotal features for model: {len(self.feature_columns)}")
        
        # Verify red and blue features match
        red_base = [col[2:] for col in self.red_features]  # Remove 'r_' prefix
        blue_base = [col[2:] for col in self.blue_features]  # Remove 'b_' prefix
        
        matching_features = set(red_base) & set(blue_base)
        print(f"Matching red/blue feature pairs: {len(matching_features)}")
        
        if len(matching_features) < len(red_base):
            print("⚠️  Warning: Not all red features have blue counterparts")
            
        # Verify all features are numeric
        non_numeric = [col for col in self.feature_columns if self.df[col].dtype not in ['int64', 'float64']]
        if non_numeric:
            print(f"⚠️  Warning: Non-numeric features found: {non_numeric}")
        else:
            print("✓ All features are numeric")
    
    def prepare_features(self):
        """Prepare features for the fighter-aware neural network"""
        print("\n" + "="*60)
        print("PREPARING FEATURES FOR FIGHTER-AWARE NEURAL NETWORK")
        print("="*60)
        
        # Identify feature categories
        self.identify_fighter_features()
        
        # Prepare feature matrix
        X = self.df[self.feature_columns].copy()
        y = self.df['winner'].copy()
        
        # Handle missing values
        if X.isnull().any().any():
            print("⚠️  Filling missing values with column medians")
            X = X.fillna(X.median())
        
        # Encode target variable
        y_encoded = self.label_encoder.fit_transform(y)
        
        print(f"✓ Target classes: {list(self.label_encoder.classes_)}")
        print(f"✓ Feature matrix shape: {X.shape}")
        print(f"✓ Target distribution:")
        target_counts = pd.Series(y).value_counts()
        for class_name, count in target_counts.items():
            print(f"   - {class_name}: {count} ({count/len(y)*100:.1f}%)")
        
        return X, y_encoded
    
    def create_fighter_aware_model(self, input_dim):
        """Create fighter-aware neural network model"""
        print("\n" + "="*60)
        print("CREATING FIGHTER-AWARE NEURAL NETWORK")
        print("="*60)
        
        # Calculate feature dimensions
        red_dim = len(self.red_features)
        blue_dim = len(self.blue_features)
        other_dim = input_dim - red_dim - blue_dim
        
        print(f"Red fighter features: {red_dim}")
        print(f"Blue fighter features: {blue_dim}")
        print(f"Other features (diffs, encoded, etc.): {other_dim}")
        
        # Input layer
        inputs = tf.keras.Input(shape=(input_dim,), name='combined_input')
        
        # Split features
        red_features_input = tf.keras.layers.Lambda(
            lambda x: x[:, :red_dim], 
            name='red_features_split'
        )(inputs)
        
        blue_features_input = tf.keras.layers.Lambda(
            lambda x: x[:, red_dim:red_dim+blue_dim], 
            name='blue_features_split'
        )(inputs)
        
        other_features_input = tf.keras.layers.Lambda(
            lambda x: x[:, red_dim+blue_dim:], 
            name='other_features_split'
        )(inputs)
        
        # Red fighter processing branch
        red_processed = tf.keras.layers.Dense(
            64, activation='relu', name='red_dense_1'
        )(red_features_input)
        red_processed = tf.keras.layers.Dropout(0.3, name='red_dropout_1')(red_processed)
        red_processed = tf.keras.layers.Dense(
            32, activation='relu', name='red_dense_2'
        )(red_processed)
        
        # Blue fighter processing branch
        blue_processed = tf.keras.layers.Dense(
            64, activation='relu', name='blue_dense_1'
        )(blue_features_input)
        blue_processed = tf.keras.layers.Dropout(0.3, name='blue_dropout_1')(blue_processed)
        blue_processed = tf.keras.layers.Dense(
            32, activation='relu', name='blue_dense_2'
        )(blue_processed)
        
        # Other features processing (differentials, encoded features)
        other_processed = tf.keras.layers.Dense(
            32, activation='relu', name='other_dense_1'
        )(other_features_input)
        other_processed = tf.keras.layers.Dropout(0.2, name='other_dropout_1')(other_processed)
        
        # Combine all processed features
        combined = tf.keras.layers.Concatenate(name='feature_combination')([
            red_processed, blue_processed, other_processed
        ])
        
        # Final decision layers
        x = tf.keras.layers.Dense(128, activation='relu', name='decision_dense_1')(combined)
        x = tf.keras.layers.Dropout(0.4, name='decision_dropout_1')(x)
        x = tf.keras.layers.Dense(64, activation='relu', name='decision_dense_2')(x)
        x = tf.keras.layers.Dropout(0.3, name='decision_dropout_2')(x)
        x = tf.keras.layers.Dense(32, activation='relu', name='decision_dense_3')(x)
        
        # Output layer
        outputs = tf.keras.layers.Dense(1, activation='sigmoid', name='winner_prediction')(x)
        
        # Create model
        model = tf.keras.Model(inputs=inputs, outputs=outputs, name='FighterAwareUFCPredictor')
        
        # Compile model
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        print("✓ Fighter-aware neural network created successfully")
        print(f"✓ Model parameters: {model.count_params():,}")
        
        # Save model summary
        model_summary = []
        model.summary(print_fn=lambda x: model_summary.append(x))
        
        with open(self.model_dir / 'model_architecture.txt', 'w') as f:
            f.write('\n'.join(model_summary))
        
        return model
    
    def train_with_cross_validation(self, X, y, n_splits=5):
        """Train with stratified k-fold cross validation"""
        print("\n" + "="*60)
        print("TRAINING WITH CROSS VALIDATION")
        print("="*60)
        
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        
        fold_scores = []
        fold_histories = []
        best_model = None
        best_score = 0
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
            print(f"\n--- Training Fold {fold + 1}/{n_splits} ---")
            
            # Split data for this fold
            X_train_fold, X_val_fold = X.iloc[train_idx], X.iloc[val_idx]
            y_train_fold, y_val_fold = y[train_idx], y[val_idx]
            
            # Scale features
            fold_scaler = StandardScaler()
            X_train_scaled = fold_scaler.fit_transform(X_train_fold)
            X_val_scaled = fold_scaler.transform(X_val_fold)
            
            # Create model for this fold
            model = self.create_fighter_aware_model(X_train_scaled.shape[1])
            
            # Callbacks
            early_stopping = tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=20,
                restore_best_weights=True,
                verbose=1
            )
            
            reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=10,
                min_lr=0.00001,
                verbose=1
            )
            
            # Train model
            history = model.fit(
                X_train_scaled, y_train_fold,
                validation_data=(X_val_scaled, y_val_fold),
                epochs=200,
                batch_size=32,
                callbacks=[early_stopping, reduce_lr],
                verbose=1
            )
            
            # Evaluate fold
            val_score = model.evaluate(X_val_scaled, y_val_fold, verbose=0)[1]
            fold_scores.append(val_score)
            fold_histories.append(history.history)
            
            print(f"Fold {fold + 1} validation accuracy: {val_score:.4f}")
            
            # Keep best model
            if val_score > best_score:
                best_score = val_score
                best_model = model
                self.scaler = fold_scaler  # Save the scaler from best fold
        
        # Calculate cross-validation statistics
        cv_mean = np.mean(fold_scores)
        cv_std = np.std(fold_scores)
        
        print(f"\n--- Cross Validation Results ---")
        print(f"Mean accuracy: {cv_mean:.4f} (+/- {cv_std*2:.4f})")
        print(f"Individual fold scores: {[f'{score:.4f}' for score in fold_scores]}")
        
        self.best_model = best_model
        self.cv_scores = fold_scores
        self.cv_mean = cv_mean
        self.cv_std = cv_std
        
        return best_model, fold_histories
    
    def evaluate_model(self, model, X_test, y_test):
        """Evaluate model performance"""
        print("\n" + "="*60)
        print("EVALUATING MODEL PERFORMANCE")
        print("="*60)
        
        # Scale test data
        X_test_scaled = self.scaler.transform(X_test)
        
        # Predictions
        y_pred_proba = model.predict(X_test_scaled)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Test Accuracy: {accuracy:.4f}")
        print(f"Cross-validation mean: {self.cv_mean:.4f} (+/- {self.cv_std*2:.4f})")
        
        print("\nClassification Report:")
        class_names = self.label_encoder.classes_
        print(classification_report(y_test, y_pred, target_names=class_names))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.title('Neural Network - Confusion Matrix')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'accuracy': accuracy,
            'cv_mean': self.cv_mean,
            'cv_std': self.cv_std,
            'y_pred_proba': y_pred_proba,
            'y_pred': y_pred,
            'classification_report': classification_report(y_test, y_pred, target_names=class_names)
        }
    
    def save_model(self):
        """Save the trained model and preprocessing components"""
        print("\n" + "="*60)
        print("SAVING MODEL AND COMPONENTS")
        print("="*60)
        
        if self.best_model is None:
            print("❌ No trained model to save")
            return
        
        # Save neural network model
        model_path = self.model_dir / 'best_neural_network_model.h5'
        self.best_model.save(model_path)
        print(f"✓ Saved model to: {model_path}")
        
        # Save preprocessing components
        scaler_path = self.model_dir / 'neural_network_scaler.pkl'
        joblib.dump(self.scaler, scaler_path)
        print(f"✓ Saved scaler to: {scaler_path}")
        
        encoder_path = self.model_dir / 'neural_network_label_encoder.pkl'
        joblib.dump(self.label_encoder, encoder_path)
        print(f"✓ Saved label encoder to: {encoder_path}")
        
        features_path = self.model_dir / 'neural_network_features.pkl'
        joblib.dump(self.feature_columns, features_path)
        print(f"✓ Saved feature list to: {features_path}")
        
        # Save feature categories
        categories_path = self.model_dir / 'neural_network_feature_categories.pkl'
        joblib.dump(self.feature_categories, categories_path)
        print(f"✓ Saved feature categories to: {categories_path}")
        
        # Save training metadata
        metadata = {
            'model_type': 'fighter_aware_neural_network',
            'num_features': len(self.feature_columns),
            'red_features': len(self.red_features),
            'blue_features': len(self.blue_features),
            'diff_features': len(self.diff_features),
            'cv_mean_accuracy': float(self.cv_mean),
            'cv_std_accuracy': float(self.cv_std),
            'training_date': datetime.now().isoformat(),
            'model_parameters': int(self.best_model.count_params())
        }
        
        metadata_path = self.model_dir / 'neural_network_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Saved metadata to: {metadata_path}")
    
    def plot_training_history(self, fold_histories):
        """Plot training history from cross validation"""
        print("\n" + "="*60)
        print("CREATING TRAINING VISUALIZATIONS")
        print("="*60)
        
        # Average metrics across folds
        metrics = ['accuracy', 'val_accuracy', 'loss', 'val_loss']
        avg_history = {}
        
        for metric in metrics:
            fold_values = []
            max_epochs = max(len(hist[metric]) for hist in fold_histories)
            
            for hist in fold_histories:
                # Pad shorter histories with last value
                values = hist[metric]
                if len(values) < max_epochs:
                    values = values + [values[-1]] * (max_epochs - len(values))
                fold_values.append(values)
            
            avg_history[metric] = np.mean(fold_values, axis=0)
        
        # Create plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Accuracy plot
        axes[0, 0].plot(avg_history['accuracy'], label='Training Accuracy')
        axes[0, 0].plot(avg_history['val_accuracy'], label='Validation Accuracy')
        axes[0, 0].set_title('Model Accuracy (Cross-Validation Average)')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss plot
        axes[0, 1].plot(avg_history['loss'], label='Training Loss')
        axes[0, 1].plot(avg_history['val_loss'], label='Validation Loss')
        axes[0, 1].set_title('Model Loss (Cross-Validation Average)')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # CV scores distribution
        axes[1, 0].bar(range(1, len(self.cv_scores) + 1), self.cv_scores)
        axes[1, 0].axhline(y=self.cv_mean, color='red', linestyle='--', 
                          label=f'Mean: {self.cv_mean:.4f}')
        axes[1, 0].set_title('Cross-Validation Fold Scores')
        axes[1, 0].set_xlabel('Fold')
        axes[1, 0].set_ylabel('Accuracy')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Model architecture visualization (simplified)
        arch_info = [
            f"Red Fighter Features: {len(self.red_features)}",
            f"Blue Fighter Features: {len(self.blue_features)}",
            f"Other Features: {len(self.feature_columns) - len(self.red_features) - len(self.blue_features)}",
            f"Total Parameters: {self.best_model.count_params():,}",
            f"CV Accuracy: {self.cv_mean:.4f} ± {self.cv_std:.4f}"
        ]
        
        axes[1, 1].axis('off')
        axes[1, 1].text(0.1, 0.5, '\n'.join(arch_info), fontsize=12, 
                       verticalalignment='center', fontfamily='monospace')
        axes[1, 1].set_title('Model Architecture Summary')
        
        plt.tight_layout()
        plt.savefig(self.viz_dir / 'training_history.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def run_complete_training(self):
        """Run the complete training pipeline"""
        print("🥊 NEURAL NETWORK TRAINING PIPELINE")
        print("Fighter-Aware Architecture for UFC Fight Prediction")
        print("=" * 80)
        
        # Load data
        self.load_data()
        
        # Prepare features
        X, y = self.prepare_features()
        
        # Split data for final test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nFinal train/test split:")
        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        
        # Train with cross validation on training set
        best_model, fold_histories = self.train_with_cross_validation(X_train, y_train)
        
        # Plot training history
        self.plot_training_history(fold_histories)
        
        # Evaluate on test set
        test_results = self.evaluate_model(best_model, X_test, y_test)
        
        # Save everything
        self.save_model()
        
        print("\n" + "="*80)
        print("🎉 NEURAL NETWORK TRAINING COMPLETE!")
        print("="*80)
        print(f"Final test accuracy: {test_results['accuracy']:.4f}")
        print(f"Cross-validation mean: {test_results['cv_mean']:.4f} ± {test_results['cv_std']:.4f}")
        print(f"Model saved to: {self.model_dir}")
        print(f"Visualizations saved to: {self.viz_dir}")
        
        return test_results


def main():
    """Main training function"""
    # Create and run trainer
    trainer = EventNormalizedNeuralNetwork()
    results = trainer.run_complete_training()
    
    print("\n🏆 Training completed successfully!")
    print(f"Accuracy: {results['accuracy']:.4f}")


if __name__ == "__main__":
    main()