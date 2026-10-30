"""Standard PV power model: P = P_STC * (G/1000) * (1 + gamma*(T-25))"""
import numpy as np

USED_INPUTS = ["G_W_m2", "T_module_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    G = X[:, 0]  # Irradiance in W/m²
    T = X[:, 1]  # Module temperature in °C
    
    # Standard PV model parameters
    P_STC = 203.3  # Power at STC (W)
    gamma = -0.00242  # Temperature coefficient per °C
    
    # Standard formula
    P = P_STC * (G / 1000) * (1 + gamma * (T - 25))
    
    return P