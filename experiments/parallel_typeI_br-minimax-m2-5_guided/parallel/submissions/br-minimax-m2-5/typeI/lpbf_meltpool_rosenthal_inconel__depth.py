"""Melt pool depth scales with laser power to ~1/3 power, inversely with scan velocity to ~2/3 power, and inversely with beam diameter to ~1 power, matching heat conduction scaling in LPBF."""
import numpy as np

USED_INPUTS = ["laser_power_W", "scan_velocity_mm_per_s", "beam_diameter_um"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    P = X[:, 0]  # laser_power_W
    V = X[:, 1]  # scan_velocity_mm_per_s
    D = X[:, 2]  # beam_diameter_um
    
    # Fitted formula: d = k * P^a * V^b * D^c
    # where a ≈ 1/3, b ≈ -2/3, c ≈ -1
    k = 50790.19
    a = 0.3681
    b = -0.6417
    c = -0.8929
    
    return k * P**a * V**b * D**c