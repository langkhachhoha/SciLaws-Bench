"""Exponential decay form for proton electric Sachs form factor ratio."""
import numpy as np

USED_INPUTS = ["Q2_GeV2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q2 = X[:, 0]
    # Fitted constant from experimental data
    a = 0.2370
    return np.exp(-a * q2)