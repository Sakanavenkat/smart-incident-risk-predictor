"""Simple training script placeholder for Random Forest model.
Run this after placing sample CSV data in `ml/data/sample.csv`.
"""
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib


def load_data(path):
    """Load CSV data."""
    return pd.read_csv(path)


def train():
    """Train Random Forest model."""
    data_path = os.path.join(os.path.dirname(__file__), "data", "sample.csv")
    model_path = os.path.join(os.path.dirname(__file__), "model.joblib")
    
    if not os.path.exists(data_path):
        print(f"No sample data found at {data_path}")
        print("Please add a sample.csv file with a 'label' column for training.")
        return
    
    df = load_data(data_path)
    print(f"Loaded {len(df)} rows from {data_path}")
    
    # Check for required label column
    if "label" not in df.columns:
        print("Error: 'label' column required in sample.csv for supervised training")
        return
    
    # Separate features and labels
    feature_cols = [col for col in df.columns if col not in ("ticket_id", "label")]
    print(f"Using features: {feature_cols}")
    
    X = df[feature_cols].fillna(0)
    y = df["label"]
    
    # Encode categorical features
    label_encoders = {}
    for col in X.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    clf = RandomForestClassifier(
        n_estimators=100,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)
    
    # Evaluate
    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)
    print(f"Train score: {train_score:.4f}")
    print(f"Test score: {test_score:.4f}")
    
    # Save model
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    train()
