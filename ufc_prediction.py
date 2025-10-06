import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import sqlite3
from pathlib import Path

def load_data():
    # Connect to the SQLite database
    db_path = Path('data/ufc_database.db')
    conn = sqlite3.connect(db_path)
    
    # Load the fighter stats
    df = pd.read_sql('SELECT * FROM fighter_stats', conn)
    conn.close()
    
    return df

def prepare_features(df):
    # Drop any rows with missing values
    df = df.dropna()
    
    # Create feature columns (excluding name and stance)
    feature_columns = ['wins', 'losses', 'height', 'weight', 'reach', 'age',
                      'slpm', 'sig_str_acc', 'sapm', 'str_def',
                      'td_avg', 'td_acc', 'td_def', 'sub_avg']
    
    # Calculate win rate
    df['win_rate'] = df['wins'] / (df['wins'] + df['losses'])
    feature_columns.append('win_rate')
    
    # Encode stance if you want to use it as a feature
    le = LabelEncoder()
    df['stance_encoded'] = le.fit_transform(df['stance'].fillna('Unknown'))
    feature_columns.append('stance_encoded')
    
    # Create target variable (whether fighter has more wins than losses)
    y = (df['wins'] > df['losses']).astype(int)
    
    # Create feature matrix
    X = df[feature_columns]
    
    return X, y, feature_columns

def train_model(X, y):
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Initialize XGBoost classifier
    model = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions on test set
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Print feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    })
    print("\nFeature Importance:")
    print(feature_importance.sort_values('importance', ascending=False))
    
    return model, X_test, y_test, accuracy

def main():
    print("Loading data...")
    df = load_data()
    
    print("Preparing features...")
    X, y, feature_columns = prepare_features(df)
    
    print("Training model...")
    model, X_test, y_test, accuracy = train_model(X, y)
    
    print(f"\nModel Accuracy: {accuracy:.2%}")
    
    # Example prediction
    print("\nExample Prediction:")
    example_fighter = X_test.iloc[0]
    prediction = model.predict([example_fighter])[0]
    print(f"Fighter stats:")
    for col, val in zip(feature_columns, example_fighter):
        print(f"{col}: {val:.2f}")
    print(f"Predicted to have more wins than losses: {bool(prediction)}")
    print(f"Actual: {bool(y_test.iloc[0])}")

if __name__ == '__main__':
    main()