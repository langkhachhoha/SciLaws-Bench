"""Velocity as a function of distance and sex using power law with sex correction."""
import numpy as np

USED_INPUTS = ["distance_m", "sex_M"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    distance_m = X[:, 0]
    sex_M = X[:, 1]
    
    # Power law coefficients from fitting
    A = 13.24
    B = -0.083
    delta = 0.10
    
    # Velocity calculation: v = A * d^B * (1 + delta * sex_M)
    velocity = A * (distance_m ** B) * (1 + delta * sex_M)
    
    return velocity