"""Riegel model with 1/d correction and sex effect.

Velocity model for running world records:
v = d^(1-n)/k + c/d + s*sex_M

This combines the standard Riegel power-law (t = k*d^n) with 
a short-distance correction term and additive sex effect.
"""
import numpy as np

USED_INPUTS = ["distance_m", "sex_M"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    d = X[:, 0]  # distance_m
    sex_M = X[:, 1]  # sex_M (1 for men, 0 for women)
    
    # Riegel model parameters
    k = 0.09  # Riegel coefficient
    n = 1.07  # Riegel exponent (standard for running)
    c = 95.0  # short-distance correction coefficient
    s = 0.65  # sex effect (men are ~0.65 m/s faster)
    
    # Velocity prediction
    v = np.power(d, 1-n) / k + c / d + s * sex_M
    
    return v