"""Post-merger GW frequency formula: f2 = 38 * M^(-1) * κ₂ᵀ^(-1/3)."""
import numpy as np

USED_INPUTS = ["mass", "kap2t"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    mass = X[:, 0]
    kap2t = X[:, 1]
    return 38.0 * mass**(-1) * kap2t**(-1/3)