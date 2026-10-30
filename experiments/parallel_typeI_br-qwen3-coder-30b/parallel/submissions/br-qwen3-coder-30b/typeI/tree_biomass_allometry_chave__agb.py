"""Allometric biomass model with diameter, wood density, and height."""
import numpy as np

USED_INPUTS = ["wood_density", "diameter_cm", "height_m"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    rho = X[:, 0]  # wood density
    D = X[:, 1]    # diameter
    H = X[:, 2]    # height
    
    # Allometric model: AGB = k * D^a * rho^b * H^c
    # Based on the fitted parameters from experimental data
    # k = 0.031641, a = 2.188, b = 0.727, c = 0.870
    k = 0.031641
    a = 2.188
    b = 0.727
    c = 0.870
    
    return k * (D**a) * (rho**b) * (H**c)