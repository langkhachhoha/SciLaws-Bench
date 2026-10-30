"""Chave et al. pantropical allometric equation for aboveground biomass.
AGB = a * (rho * D^2 * H)^b
"""
import numpy as np

USED_INPUTS = ["wood_density", "diameter_cm", "height_m"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    rho = X[:, 0]  # wood_density (g/cm^3)
    D = X[:, 1]    # diameter_cm
    H = X[:, 2]    # height_m
    
    # Chave et al. 2014 style pantropical model
    # Combined volume-density term: rho * D^2 * H
    # Fitted constants
    a = 0.07
    b = 0.96
    
    return a * (rho * D**2 * H)**b