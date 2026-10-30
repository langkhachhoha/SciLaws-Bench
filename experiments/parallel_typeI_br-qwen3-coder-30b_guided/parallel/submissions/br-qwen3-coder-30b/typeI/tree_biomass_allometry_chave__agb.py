"""Allometric relationship for aboveground biomass: AGB = 0.054 * wood_density * diameter_cm^2 * height_m"""
import numpy as np

USED_INPUTS = ["wood_density", "diameter_cm", "height_m"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    rho = X[:, 0]
    d = X[:, 1]
    h = X[:, 2]
    return 0.054 * rho * d**2 * h