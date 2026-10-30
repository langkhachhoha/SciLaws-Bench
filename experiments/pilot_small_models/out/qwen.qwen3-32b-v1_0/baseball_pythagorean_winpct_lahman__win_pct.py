"""Win percentage based on runs scored and allowed."""
import numpy as np

USED_INPUTS = ["R", "RA", "G"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    R = X[:, 0]
    RA = X[:, 1]
    G = X[:, 2]
    # Pythagorean expectation with exponent 2
    win_pct = R**2 / (R**2 + RA**2)
    return win_pct