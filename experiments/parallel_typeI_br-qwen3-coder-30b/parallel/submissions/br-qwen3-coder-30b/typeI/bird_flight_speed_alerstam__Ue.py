"""Cruising airspeed as a function of wing loading in flapping flight."""
import numpy as np

USED_INPUTS = ["mass_kg", "wing_area_m2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    mass = X[:, 0]
    wing_area = X[:, 1]
    
    # Compute wing loading (mass divided by wing area)
    wing_loading = mass / wing_area
    
    # Apply the fitted relationship: Ue = a * sqrt(wing_loading) + b
    # where a = 2.349478 and b = 8.996047
    return 2.349478 * np.sqrt(wing_loading) + 8.996047