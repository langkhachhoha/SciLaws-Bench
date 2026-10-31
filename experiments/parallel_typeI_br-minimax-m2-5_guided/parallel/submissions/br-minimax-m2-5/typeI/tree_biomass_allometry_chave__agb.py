"""Chave allometric equation for tropical tree aboveground biomass.

AGB = 0.0509 * rho * D^2 * H

where:
- rho = wood_density (g/cm³)
- D = diameter_cm (cm) 
- H = height_m (m)
"""
import numpy as np

USED_INPUTS = ["wood_density", "diameter_cm", "height_m"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    rho = X[:, 0]  # wood_density (g/cm³)
    D = X[:, 1]    # diameter_cm (cm)
    H = X[:, 2]    # height_m (m)
    return 0.0509 * rho * D**2 * H