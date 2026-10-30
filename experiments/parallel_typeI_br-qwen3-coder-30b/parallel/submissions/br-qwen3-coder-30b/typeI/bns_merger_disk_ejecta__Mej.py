"""Dynamical ejecta mass from neutron star mergers. Based on power-law scaling with tidal deformability and mass ratio."""
import numpy as np

USED_INPUTS = ["q", "Lambda_tilde"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q = X[:, 0]
    Lambda_tilde = X[:, 1]
    
    # Constant derived from fitting the data
    C = 2.455e-11
    
    # Functional form: Mej = C * Lambda_tilde^3 * (1-q)^2
    return C * (Lambda_tilde ** 3) * ((1 - q) ** 2)