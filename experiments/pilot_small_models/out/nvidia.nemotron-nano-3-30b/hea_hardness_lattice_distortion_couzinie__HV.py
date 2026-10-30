"""Linear fit using VEC and dHmix."""
import numpy as np

USED_INPUTS = ["VEC", "dHmix"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x_vec = X[:, 0]
    dHmix = X[:, 1]
    return 113.515 * x_vec + 86.687 * dHmix - 1770.39