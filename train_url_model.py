"""
Malicious URL Classification Model Trainer
Extracts 9 lexical features from URL strings and trains a Random Forest Classifier.
Evaluates accuracy, precision, recall, f1-score, and generates a confusion matrix.
Saves model artifact to models/url_model.joblib and plot to static/images/url_confusion_matrix.png.
"""

import os
import sys
import datetime
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Import feature extractor from url_classifier
from url_classifier import extract_url_features, FEATURE_NAMES

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "urls.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "url_model.joblib")
IMAGES_DIR = os.path.join(BASE_DIR, "static", "images")
CM_IMAGE_PATH = os.path.join(IMAGES_DIR, "url_confusion_matrix.png")


def validate_and_load_data(filepath):
    """Validates existence and columns of the URL dataset."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"URL dataset not found at '{filepath}'. Please check the datasets directory.")
    
    df = pd.read_csv(filepath)
    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError(f"Dataset must contain 'url' and 'label' columns. Found: {list(df.columns)}")
        
    initial_count = len(df)
    df = df.dropna(subset=["url", "label"])
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["url"] = df["url"].astype(str).str.strip()
    df = df[df["url"].str.len() > 0]
    
    # Filter valid labels: legitimate and malicious
    df = df[df["label"].isin(["legitimate", "malicious"])]
    
    if len(df) == 0:
        raise ValueError("No valid URL records found in the dataset after cleaning.")
        
    print(f"[*] Loaded URL dataset: {len(df)} valid records (from {initial_count} initial).")
    class_counts = df["label"].value_counts().to_dict()
    print(f"[*] Class distribution: {class_counts}")
    
    if len(class_counts) < 2:
        raise ValueError("Dataset must contain both 'legitimate' and 'malicious' samples for training.")
        
    return df


def plot_and_save_confusion_matrix(cm, classes, output_path, metrics):
    """Renders a styled confusion matrix with Matplotlib and saves to disk."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(6, 5), facecolor="#0B132B")
    ax.set_facecolor("#1C2541")
    
    cax = ax.matshow(cm, cmap="Blues", alpha=0.85)
    fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    
    ax.set_xticks(range(len(classes)))
    ax.set_yticks(range(len(classes)))
    ax.set_xticklabels([c.upper() for c in classes], color="#E0E6ED", fontsize=10, fontweight="bold")
    ax.set_yticklabels([c.upper() for c in classes], color="#E0E6ED", fontsize=10, fontweight="bold")
    
    ax.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)
    
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            val = cm[i, j]
            ax.text(
                j, i, f"{val}",
                ha="center", va="center",
                color="#0B132B" if val > cm.max() / 2 else "#E0E6ED",
                fontsize=14, fontweight="bold"
            )
            
    plt.xlabel("Predicted Label", color="#4CC9F0", fontsize=12, labelpad=10, fontweight="bold")
    plt.ylabel("True Label", color="#4CC9F0", fontsize=12, labelpad=10, fontweight="bold")
    plt.title(
        f"URL Confusion Matrix\nAccuracy: {metrics['accuracy']*100:.1f}% | F1: {metrics['f1_score']*100:.1f}%",
        color="#00F5D4", fontsize=12, pad=15, fontweight="bold"
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[+] Confusion matrix plot saved: {output_path}")


def train_url_model():
    """Main training routine for URL classification."""
    print("=" * 60)
    print("      MALICIOUS URL CLASSIFICATION MODEL TRAINING")
    print("=" * 60)
    
    df = validate_and_load_data(DATASET_PATH)
    
    print("[*] Extracting 9 lexical features for each URL...")
    feature_list = []
    for idx, raw_url in enumerate(df["url"]):
        feats = extract_url_features(raw_url)
        feature_list.append(feats)
        
    X = pd.DataFrame(feature_list)[FEATURE_NAMES]
    y = df["label"].map({"legitimate": 0, "malicious": 1})
    
    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
    
    print(f"[*] Training samples: {len(X_train)} | Testing samples: {len(X_test)}")
    print(f"[*] Features used ({len(FEATURE_NAMES)}): {', '.join(FEATURE_NAMES)}")
    
    # Random Forest Classifier
    rf = RandomForestClassifier(
        n_estimators=120,
        max_depth=10,
        min_samples_split=3,
        random_state=42
    )
    
    print("[*] Fitting Random Forest Classifier...")
    rf.fit(X_train, y_train)
    
    # Evaluation
    y_pred = rf.predict(X_test)
    y_pred_proba = rf.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    
    # Feature importances
    importances = dict(zip(FEATURE_NAMES, [round(float(v), 4) for v in rf.feature_importances_]))
    
    metrics = {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "classes": ["legitimate", "malicious"],
        "feature_importances": importances,
        "trained_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print("\n" + "=" * 40)
    print("       EVALUATION METRICS")
    print("=" * 40)
    print(f" Accuracy : {metrics['accuracy'] * 100:.2f}%")
    print(f" Precision: {metrics['precision'] * 100:.2f}%")
    print(f" Recall   : {metrics['recall'] * 100:.2f}%")
    print(f" F1-Score : {metrics['f1_score'] * 100:.2f}%")
    print("=" * 40)
    print("\nFeature Importances:")
    for feat, imp in sorted(importances.items(), key=lambda x: x[1], reverse=True):
        print(f" - {feat:25s}: {imp:.4f}")
        
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["legitimate", "malicious"]))
    print("Confusion Matrix:")
    print(cm)
    
    # Save visual plot
    plot_and_save_confusion_matrix(cm, ["legitimate", "malicious"], CM_IMAGE_PATH, metrics)
    
    # Save model artifact
    os.makedirs(MODEL_DIR, exist_ok=True)
    payload = {
        "model": rf,
        "feature_names": FEATURE_NAMES,
        "metrics": metrics,
        "classes": ["legitimate", "malicious"]
    }
    joblib.dump(payload, MODEL_PATH)
    print(f"\n[+] Successfully saved trained URL model to: {MODEL_PATH}")
    print("=" * 60 + "\n")
    return metrics


if __name__ == "__main__":
    train_url_model()

