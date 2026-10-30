"""Exponential decay model for arthropod species richness vs habitat modification index."""
import numpy as np

USED_INPUTS = ["d"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    d = X[:, 0]
    # Based on the exponential decay model: S = A * exp(-k*d) + C_min
    # Using fitted parameters: A ≈ 41.875, k ≈ 0.109, C_min ≈ 1.108
    # For clean submission, using rounded values that maintain good fit quality
    return 41.875 * np.exp(-0.109 * d) + 1.108