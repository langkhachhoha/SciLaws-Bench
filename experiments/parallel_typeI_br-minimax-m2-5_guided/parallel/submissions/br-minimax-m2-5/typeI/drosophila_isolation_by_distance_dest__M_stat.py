"""Isolation by distance: M = a * sqrt(d) where a is a constant."""
import numpy as np

USED_INPUTS = ["distance_km"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    return 0.00138 * np.sqrt(x)