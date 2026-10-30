"""Solar collector efficiency model based on irradiance and temperature difference."""
import numpy as np

USED_INPUTS = ["G_W_m2", "T_in_C", "T_amb_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    G = X[:, 0]
    T_in = X[:, 1]
    T_amb = X[:, 2]
    
    # Temperature difference
    delta_T = T_in - T_amb
    
    # Solar collector efficiency model
    # eta = G / (G + 0.019243 * delta_T + 0.001044 * delta_T^2)
    eta = G / (G + 0.019243 * delta_T + 0.001044 * delta_T**2)
    
    return eta