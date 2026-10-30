"""Melt pool depth model based on laser power, scan velocity, and beam diameter."""
import numpy as np

USED_INPUTS = ["laser_power_W", "scan_velocity_mm_per_s", "beam_diameter_um"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    P = X[:, 0]  # laser_power_W
    V = X[:, 1]  # scan_velocity_mm_per_s
    D = X[:, 2]  # beam_diameter_um
    
    # Based on the experimental data analysis, the melt pool depth follows:
    # d = k * P^0.5 / (V * D)
    # Using the fitted constant k ≈ 475542 from the experimental data
    k = 475542.051
    
    # Avoid division by zero
    eps = 1e-12
    V = np.maximum(V, eps)
    D = np.maximum(D, eps)
    
    return k * np.sqrt(P) / (V * D)