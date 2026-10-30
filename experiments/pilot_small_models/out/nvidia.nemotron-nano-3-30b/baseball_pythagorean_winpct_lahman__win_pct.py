"""Linear fit using win_pct = 1 - (R+RA)/(2*G)."""
import numpy as np

USED_INPUTS = ["R", "RA", "G"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    r = X[:, 0]
    ra = X[:, 1]
    g = X[:, 2]
    return 1.0 - (r + ra) / (2.0 * g)