"""Gutenberg-Richter law: log10_N = a - b*M, with a≈9.002 and b≈1.155"""
import numpy as np

USED_INPUTS = ["M_threshold"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    M = X[:, 0]
    # Gutenberg-Richter: log10_N = a - b*M
    return 9.002 - 1.155 * M