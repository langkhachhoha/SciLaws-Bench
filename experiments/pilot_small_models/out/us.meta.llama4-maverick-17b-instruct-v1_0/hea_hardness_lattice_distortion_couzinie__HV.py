"""Vickers hardness formula based on VEC and dHmix."""
import numpy as np

USED_INPUTS = ["VEC", "dHmix"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    VEC = X[:, 0]
    dHmix = X[:, 1]
    return 76.1 * VEC - 8.46 * dHmix + 0.935 * VEC * dHmix + 134.6