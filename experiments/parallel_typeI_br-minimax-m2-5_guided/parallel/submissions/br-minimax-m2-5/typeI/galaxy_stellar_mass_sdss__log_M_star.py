"""Stellar mass estimation from galaxy photometry.

log_M_star = a*(g - r) + b*(i - DM) + c

This follows the standard stellar mass estimation formula:
log(M) = log(L_i) + log(M/L_i) / log(L_i) = -0.4*(i-DM)
/ log(M/L_i) depends on color (g-r)

Coefficients derived from fitting to simulator data.
"""
import numpy as np

USED_INPUTS = ["g", "r", "i", "DM"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    g = X[:, 0]
    r = X[:, 1]
    i = X[:, 2]
    DM = X[:, 3]
    
    # Formula: log_M_star = a*(g-r) + b*(i-DM) + c
    # where c ≈ 0 (by construction of the physics)
    a = 0.3286
    b = -0.4678
    c = 0.0223
    
    return a * (g - r) + b * (i - DM) + c