"""Isolation Forest helpers; unusual does not mean malicious."""
import numpy as np
from sklearn.ensemble import IsolationForest

def fit_anomaly_model(X_benign, seed=42, max_rows=50000):
    if X_benign is None or len(X_benign) < 50:
        return None
    X = X_benign.sample(max_rows, random_state=seed) if len(X_benign) > max_rows else X_benign
    return IsolationForest(n_estimators=100, max_samples=256, contamination="auto", random_state=seed, n_jobs=-1).fit(X)

def anomaly_scores(model, X):
    return np.zeros(len(X), dtype=float) if model is None else -model.decision_function(X)
