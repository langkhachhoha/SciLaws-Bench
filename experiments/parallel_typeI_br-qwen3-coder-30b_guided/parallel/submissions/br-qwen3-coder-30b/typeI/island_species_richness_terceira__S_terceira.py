"""Exponential decay model for arthropod species richness vs anthropogenic disturbance."""
import numpy as np

USED_INPUTS = ["d"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    d = X[:, 0]
    # Based on the fitted exponential decay model: S = 33.5 * exp(-0.096 * d) + 1.14
    return 33.5 * np.exp(-0.096 * d) + 1.14