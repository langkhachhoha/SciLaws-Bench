"""Thermocline depth scales logarithmically with lake surface area."""
import numpy as np

USED_INPUTS = ["A_s_km2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    A_s = X[:, 0]
    # Based on the fitted relationship z_t = 1.1248 * ln(A_s) + 7.4372
    # Rounded to maintain simplicity while preserving accuracy
    return 1.12 * np.log(A_s) + 7.44