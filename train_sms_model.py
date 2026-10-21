"""
SMS Spam Detection Model Trainer
Trains a TF-IDF + Multinomial Naive Bayes pipeline on labeled SMS data.
Evaluates accuracy, precision, recall, f1-score, and outputs confusion matrix.
Saves model artifact to models/sms_model.joblib and plot to static/images/sms_confusion_matrix.png.
"""

import os
import sys
import datetime
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless server rendering
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "sms_spam.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "sms_model.joblib")
IMAGES_DIR = os.path.join(BASE_DIR, "static", "images")
CM_IMAGE_PATH = os.path.join(IMAGES_DIR, "sms_confusion_matrix.png")


def validate_and_load_data(filepath):
    """Validates existence and required columns of the SMS dataset."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"SMS dataset not found at '{filepath}'. Please check the datasets directory.")
    
    df = pd.read_csv(filepath)
    if "label" not in df.columns or "message" not in df.columns:
        raise ValueError(f"Dataset must contain 'label' and 'message' columns. Found: {list(df.columns)}")
    
    # Drop empty or malformed rows
    initial_count = len(df)
    df = df.dropna(subset=["label", "message"])
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["message"] = df["message"].astype(str).str.strip()
    df = df[df["message"].str.len() > 0]
    
    # Filter only valid classes: ham and spam
    df = df[df["label"].isin(["ham", "spam"])]
    
    if len(df) == 0:
        raise ValueError("No valid rows found in the dataset after cleaning.")
    
    print(f"[*] Loaded SMS dataset: {len(df)} valid records (from {initial_count} initial).")
    class_counts = df["label"].value_counts().to_dict()
    print(f"[*] Class distribution: {class_counts}")
    
    if len(class_counts) < 2:
        raise ValueError("Dataset must contain both 'ham' and 'spam' samples for training.")
        
    return df


def plot_and_save_confusion_matrix(cm, classes, output_path, metrics):
    """Renders a styled confusion matrix with Matplotlib and saves to disk."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(6, 5), facecolor="#0B132B")
    ax.set_facecolor("#1C2541")
    
    # Heatmap rendering
    cax = ax.matshow(cm, cmap="Blues", alpha=0.85)
    fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    
    # Set labels
    ax.set_xticks(range(len(classes)))
    ax.set_yticks(range(len(classes)))
    ax.set_xticklabels([c.upper() for c in classes], color="#E0E6ED", fontsize=11, fontweight="bold")
    ax.set_yticklabels([c.upper() for c in classes], color="#E0E6ED", fontsize=11, fontweight="bold")
    
    ax.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)
    
    # Annotate numbers in grid
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
        f"SMS Confusion Matrix\nAccuracy: {metrics['accuracy']*100:.1f}% | F1: {metrics['f1_score']*100:.1f}%",
        color="#00F5D4", fontsize=12, pad=15, fontweight="bold"
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[+] Confusion matrix plot saved: {output_path}")


def train_sms_model():
    """Main training routine for SMS spam classifier."""
    print("=" * 60)
    print("       SMS SPAM DETECTION MODEL TRAINING PIPELINE")
    print("=" * 60)
    
    df = validate_and_load_data(DATASET_PATH)
    
    X = df["message"]
    y = df["label"].map({"ham": 0, "spam": 1})
    
    # Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
    
    print(f"[*] Training samples: {len(X_train)} | Testing samples: {len(X_test)}")
    
    # Pipeline: TF-IDF Vectorizer + Multinomial Naive Bayes
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_features=4000,
            sublinear_tf=True
        )),
        ("classifier", MultinomialNB(alpha=0.1))
    ])
    
    print("[*] Fitting TF-IDF Vectorizer and Multinomial Naive Bayes...")
    pipeline.fit(X_train, y_train)
    
    # Evaluation
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    
    metrics = {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "classes": ["ham", "spam"],
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
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["ham", "spam"]))
    print("Confusion Matrix:")
    print(cm)
    
    # Save visual plot
    plot_and_save_confusion_matrix(cm, ["ham", "spam"], CM_IMAGE_PATH, metrics)
    
    # Save model artifact
    os.makedirs(MODEL_DIR, exist_ok=True)
    payload = {
        "pipeline": pipeline,
        "metrics": metrics,
        "classes": ["ham", "spam"]
    }
    joblib.dump(payload, MODEL_PATH)
    print(f"\n[+] Successfully saved trained SMS model to: {MODEL_PATH}")
    print("=" * 60 + "\n")
    return metrics


if __name__ == "__main__":
    train_sms_model()

