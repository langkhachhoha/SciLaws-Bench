"""Linear model: HV increases with VEC and decreases with dHmix."""
import numpy as np

USED_INPUTS = ["VEC", "dHmix"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    VEC = X[:, 0]
    dHmix = X[:, 1]
    return -31.4 + 86.4 * VEC - 8.1 * dHmix