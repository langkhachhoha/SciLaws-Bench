"""Linear fit using one input."""
import numpy as np

USED_INPUTS = ["VEC", "dHmix"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    y = X[:, 1]
    return -3.31 * x + 1.07 + 0.5 * y