"""Central project configuration."""
APP_NAME = "CyberSentinel AI"
BENIGN_LABEL = "BENIGN"
RISK_THRESHOLDS = {"MEDIUM":25,"HIGH":50,"CRITICAL":75}
ATTACK_SEVERITY = {"dos":0.8,"ddos":0.9,"infiltration":1.0,"bot":0.85,"portscan":0.65,"web":0.7}
DEFAULT_ATTACK_SEVERITY = 0.7
RISK_WEIGHTS_WITH_ANOMALY = {"attack":55,"severity":25,"anomaly":20}
RISK_WEIGHTS_NO_ANOMALY = {"attack":70,"severity":30,"anomaly":0}
