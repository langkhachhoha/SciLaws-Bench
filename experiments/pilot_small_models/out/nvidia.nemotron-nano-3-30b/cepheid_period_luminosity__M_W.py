"""Linear scaling with log P and feh."""
import numpy as np

USED_INPUTS = ["log_P", "feh"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    f = X[:, 1]
    return -0.5 * x - 0.5 * f - 1.0