"""Dynamical ejecta mass from neutron star merger based on mass ratio and tidal deformability."""
import numpy as np

USED_INPUTS = ["q", "Lambda_tilde"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q = X[:, 0]
    Lambda_tilde = X[:, 1]
    
    # Based on analysis of the simulator data, the relationship is:
    # Mej = 1.58e-05 * Lambda_tilde^1.1 * q^(-1.5)
    return 1.58e-05 * (Lambda_tilde**1.1) * (q**(-1.5))