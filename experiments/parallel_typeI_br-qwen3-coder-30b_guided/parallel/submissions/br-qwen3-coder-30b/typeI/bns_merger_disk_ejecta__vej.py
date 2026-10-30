"""Neutron star merger ejecta velocity based on mass ratio and tidal deformability."""
import numpy as np

USED_INPUTS = ["q", "Lambda_tilde"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q = X[:, 0]
    Lambda_tilde = X[:, 1]
    
    # Based on the data analysis, the relationship appears to be:
    # vej = 0.6137 * q^(-0.5975) * Lambda_tilde^(-0.1449)
    # which can be written as: 
    # vej = 0.6137 / (q^(0.5975) * Lambda_tilde^(0.1449))
    
    # For simplicity and to match common astrophysical forms, we'll use:
    # vej = 0.0092 * sqrt(Lambda_tilde) / q (approximately)
    # But to be more precise and match the fitted form:
    
    # Using the fitted constants from our analysis
    return 0.6137 * (q**(-0.5975)) * (Lambda_tilde**(-0.1449))