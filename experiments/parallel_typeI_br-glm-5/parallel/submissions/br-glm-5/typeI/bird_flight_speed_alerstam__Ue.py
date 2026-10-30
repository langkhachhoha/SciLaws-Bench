"""Cruising airspeed of migratory birds in flapping flight.

The equivalent airspeed scales with the square root of wing loading (mass/wing_area):
Ue = sqrt(16 * mass/wing_area + 115)

This relationship arises from aerodynamic optimization - the minimum power and maximum
range speeds both scale with the square root of wing loading. The constant term 
represents a baseline speed component, while the coefficient 16 encompasses drag 
and efficiency parameters."""
import numpy as np

USED_INPUTS = ["mass_kg", "wing_area_m2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    mass = X[:, 0]  # mass_kg
    wing_area = X[:, 1]  # wing_area_m2
    wing_loading = mass / wing_area
    ue = np.sqrt(16.0 * wing_loading + 115.0)
    return ue