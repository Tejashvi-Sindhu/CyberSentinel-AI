"""Transparent risk triage score, not a probability of compromise."""
def assess_risk(label: str, attack_probability: float, anomaly_strength: float = 0.0, use_anomaly: bool = True, thresholds: dict | None = None) -> tuple[float, str]:
    thresholds = thresholds or {"MEDIUM":25,"HIGH":50,"CRITICAL":75}
    benign = str(label).strip().upper() == "BENIGN"
    p = 0.0 if benign else max(0.0,min(1.0,float(attack_probability)))
    a = max(0.0,min(1.0,float(anomaly_strength))) if use_anomaly else 0.0
    score = max(0.0,min(100.0,75*p+25*a))
    level = "CRITICAL" if score >= thresholds["CRITICAL"] else "HIGH" if score >= thresholds["HIGH"] else "MEDIUM" if score >= thresholds["MEDIUM"] else "LOW"
    return float(score),level

def explain_risk(label, attack_probability, anomaly_percentile, score, level, use_anomaly=True):
    return f"Predicted class: {label}. Risk triage score: {score:.1f}/100 ({level}). This score is a triage aid, not proof of compromise."
