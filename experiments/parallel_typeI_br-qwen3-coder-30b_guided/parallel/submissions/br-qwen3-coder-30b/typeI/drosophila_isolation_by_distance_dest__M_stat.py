"""Isolation by distance model with exponential saturation."""
import numpy as np

USED_INPUTS = ["distance_km"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    distance_km = X[:, 0]
    # Exponential saturation model: M_stat = A * (1 - exp(-B * distance))
    # Based on fitting to the data, A ≈ 0.1518, B ≈ 2.48e-04
    A = 0.1518
    B = 2.48e-04
    return A * (1 - np.exp(-B * distance_km))