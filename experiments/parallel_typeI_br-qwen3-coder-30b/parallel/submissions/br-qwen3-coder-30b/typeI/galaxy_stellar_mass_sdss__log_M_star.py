"""Stellar mass as a function of absolute magnitude and distance modulus."""
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
    
    # Absolute magnitude in g-band
    abs_g = g - DM
    
    # Stellar mass relation: log_M_star = A * abs_g + B
    # From our analysis, A ≈ -0.2290, B ≈ 4.3277
    return -0.2290 * abs_g + 4.3277