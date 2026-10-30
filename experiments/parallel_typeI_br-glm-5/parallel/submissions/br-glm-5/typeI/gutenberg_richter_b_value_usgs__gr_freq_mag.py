"""Gutenberg-Richter law for earthquake frequency-magnitude relationship."""
import numpy as np

USED_INPUTS = ["M_threshold"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    M = X[:, 0]
    # Standard Gutenberg-Richter law: log10_N = a - b*M
    a = 8.90
    b = 1.14
    return a - b * M