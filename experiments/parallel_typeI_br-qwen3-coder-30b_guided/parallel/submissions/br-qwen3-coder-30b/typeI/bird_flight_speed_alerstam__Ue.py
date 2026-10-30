"""Cruising airspeed of migratory birds in flapping flight. Based on aerodynamic scaling law Ue = 74 * mass^(2/3) / wing_area^(1/2)."""
import numpy as np

USED_INPUTS = ["mass_kg", "wing_area_m2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    mass = X[:, 0]
    wing_area = X[:, 1]
    # Ue = 74 * mass^(2/3) / wing_area^(1/2)
    return 74 * mass**(2/3) / wing_area**(1/2)