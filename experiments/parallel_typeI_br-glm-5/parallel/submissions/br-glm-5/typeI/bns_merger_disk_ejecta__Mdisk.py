"""Accretion disk mass follows sqrt threshold model: Mdisk = a * sqrt(C_thr - C1) for C1 < C_thr."""
import numpy as np

USED_INPUTS = ["C1"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    C1 = X[:, 0]
    a = 0.82
    C_thr = 0.172
    return a * np.sqrt(np.maximum(C_thr - C1, 0))