"""Frequency scaling with mass and tidal coupling parameter."""
import numpy as np

USED_INPUTS = ["mass", "kap2t"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    mass = X[:, 0]
    kap2t = X[:, 1]
    # Based on the data analysis, f2 scales as mass / kap2t^(1/3)
    return 116.8 * mass / (kap2t ** (1/3))