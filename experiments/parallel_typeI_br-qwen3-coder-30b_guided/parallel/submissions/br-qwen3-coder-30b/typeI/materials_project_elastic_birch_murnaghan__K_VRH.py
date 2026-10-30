"""Bulk modulus as a function of atomic volume following inverse power law relationship."""
import numpy as np

USED_INPUTS = ["V_atomic_A3"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    V = X[:, 0]
    # Based on fitting the data, K_VRH_GPa ~ 10086.0376 / V^1.5245
    # Using rounded constants for submission
    return 10086.0376 / (V ** 1.5245)