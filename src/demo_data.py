"""Synthetic data generator for UI and pipeline smoke tests only."""
import numpy as np
import pandas as pd

FEATURES = ["Flow Duration", "Total Fwd Packets", "Total Backward Packets", "Flow Bytes/s", "Flow Packets/s", "Packet Length Mean", "SYN Flag Count", "Destination Port"]

def generate_demo_dataset(n: int = 2000, seed: int = 42) -> pd.DataFrame:
    if n < 2:
        raise ValueError("n must be at least 2")
    rng = np.random.default_rng(seed)
    labels = rng.choice(["BENIGN", "DoS"], size=n, p=[0.72, 0.28])
    attack = labels != "BENIGN"
    duration = rng.lognormal(2.3, 0.8, n)
    fwd = rng.poisson(7, n) + 1
    back = rng.poisson(5, n) + 1
    byte_rate = rng.lognormal(5.1, 1.0, n)
    packet_rate = rng.lognormal(1.7, 0.7, n)
    packet_mean = rng.normal(650, 140, n).clip(40, 1500)
    syn = rng.poisson(1, n)
    port = rng.choice([53, 80, 443, 8080, 22, 3389], n)
    duration[attack] *= 0.45
    fwd[attack] += rng.integers(10, 70, attack.sum())
    byte_rate[attack] *= 4
    packet_rate[attack] *= 3
    syn[attack] += rng.integers(3, 15, attack.sum())
    return pd.DataFrame({"Flow Duration":duration,"Total Fwd Packets":fwd,"Total Backward Packets":back,"Flow Bytes/s":byte_rate,"Flow Packets/s":packet_rate,"Packet Length Mean":packet_mean,"SYN Flag Count":syn,"Destination Port":port,"Label":labels})
