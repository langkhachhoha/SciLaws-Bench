"""Stellar mass estimation using r-band absolute magnitude and (g-i) color."""
import numpy as np

USED_INPUTS = ["g", "r", "i", "DM"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    g = X[:, 0]
    r = X[:, 1]
    i = X[:, 2]
    DM = X[:, 3]
    
    # Absolute magnitude in r-band
    M_r = r - DM
    
    # Color (g-i)
    g_minus_i = g - i
    
    # log(M*) = const - 0.4*M_r + coeff*(g-i)
    # Based on Bell et al. style stellar mass-to-light relation
    log_M_star = 1.2759 - 0.4 * M_r + 0.4648 * g_minus_i
    
    return log_M_star