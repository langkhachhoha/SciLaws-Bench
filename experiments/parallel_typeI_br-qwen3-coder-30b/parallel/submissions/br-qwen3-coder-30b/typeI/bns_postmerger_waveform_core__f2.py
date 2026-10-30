"""Inverse relationship with mass and kap2t."""
import numpy as np

USED_INPUTS = ["mass", "kap2t"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    mass = X[:, 0]
    kap2t = X[:, 1]
    return 529.906686 / (mass * kap2t) + 0.820923