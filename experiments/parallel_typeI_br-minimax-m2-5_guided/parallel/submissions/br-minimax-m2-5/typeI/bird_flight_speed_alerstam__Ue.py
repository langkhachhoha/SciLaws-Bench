"""Cruising airspeed = minimum speed + constant * sqrt(mass/wing_area)."""
import numpy as np

USED_INPUTS = ["mass_kg", "wing_area_m2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    m = X[:, 0]  # mass_kg
    S = X[:, 1]  # wing_area_m2
    # Ue = Ue_min + k * sqrt(m/S)
    # This corresponds to minimum flapping speed + speed needed for lift
    return 6.83 + 3.71 * np.sqrt(m / S)