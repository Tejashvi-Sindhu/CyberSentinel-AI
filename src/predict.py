"""Load trained models and analyse compatible network-flow frames."""
from dataclasses import dataclass
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from src.preprocessing import align_features
from src.risk_assessment import assess_risk

@dataclass
class DetectionSettings:
    use_anomaly: bool = False

@dataclass
class PredictionOutput:
    results: pd.DataFrame

def load_bundle(mode="binary",model_dir="models"):
    path=Path(model_dir)/f"{mode}_model.joblib"
    if not path.exists(): raise FileNotFoundError(f"Model not found at {path}. Train it first.")
    return joblib.load(path)

def predict_dataframe(frame: pd.DataFrame,bundle: dict,settings: DetectionSettings|None=None):
    settings=settings or DetectionSettings()
    X=align_features(frame,bundle["features"])
    model=bundle["model"]
    labels=model.predict(X)
    probabilities=model.predict_proba(X) if hasattr(model,"predict_proba") else None
    classes=list(model.classes_) if hasattr(model,"classes_") else []
    rows=[]
    for i,label in enumerate(labels):
        prob=float(max(probabilities[i])) if probabilities is not None else 0.0
        attack_prob=0.0 if str(label).upper()=="BENIGN" else prob
        score,level=assess_risk(str(label),attack_prob,0.0,settings.use_anomaly)
        rows.append({"prediction":str(label),"confidence":prob,"risk_score":score,"risk_level":level,"status":"BENIGN" if str(label).upper()=="BENIGN" else "ATTACK"})
    return PredictionOutput(pd.DataFrame(rows,index=frame.index))
