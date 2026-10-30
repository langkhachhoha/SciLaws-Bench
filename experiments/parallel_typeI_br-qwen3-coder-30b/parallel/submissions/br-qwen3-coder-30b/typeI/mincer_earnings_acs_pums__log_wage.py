"""Linear model with schooling and experience effects."""
import numpy as np

USED_INPUTS = ["SCHL_years", "exp"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    s = X[:, 0]
    x = X[:, 1]
    return 0.5 * s + 0.05 * x + 1.0