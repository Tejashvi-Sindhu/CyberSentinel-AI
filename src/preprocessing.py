"""Feature header normalization and numeric validation."""
import re
import numpy as np
import pandas as pd

def normalize_name(value: object) -> str:
    text = str(value).strip().lower().replace("∞", "inf")
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")

def normalize_frame_columns(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out.columns = [normalize_name(c) for c in out.columns]
    if out.columns.duplicated().any():
        raise ValueError("Column names collide after normalization.")
    return out

def find_missing_features(frame: pd.DataFrame, schema: list[str]) -> list[str]:
    return [normalize_name(c) for c in schema if normalize_name(c) not in set(normalize_frame_columns(frame).columns)]

def align_features(frame: pd.DataFrame, schema: list[str]) -> pd.DataFrame:
    normalized = normalize_frame_columns(frame)
    wanted = [normalize_name(c) for c in schema]
    missing = [c for c in wanted if c not in normalized.columns]
    if missing:
        raise ValueError("Missing required feature columns: " + ", ".join(missing))
    X = normalized[wanted].copy()
    for col in X:
        X[col] = pd.to_numeric(X[col], errors="coerce")
    return X.replace([np.inf, -np.inf], np.nan)
