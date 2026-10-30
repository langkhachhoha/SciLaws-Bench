"""Melt pool depth follows approximate power-law scaling: d ~ P^b / V^c / D where
b≈0.9, c≈0.6. This captures the key physics: depth increases with power,
decreases with velocity, and scales inversely with beam diameter.
"""
import numpy as np

USED_INPUTS = ["laser_power_W", "scan_velocity_mm_per_s", "beam_diameter_um"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    P = X[:, 0]  # laser_power_W
    V = X[:, 1]  # scan_velocity_mm_per_s
    D = X[:, 2]  # beam_diameter_um
    
    a = 3600.0
    b = 0.9
    c = 0.59
    
    return a * (P ** b) / (V ** c) / D