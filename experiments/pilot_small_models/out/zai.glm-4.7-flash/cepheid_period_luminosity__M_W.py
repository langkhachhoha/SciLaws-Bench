"""Cepheid Period-Luminosity relation with metallicity dependence."""
import numpy as np

USED_INPUTS = ["log_P", "feh"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Inputs
    log_P = X[:, 0]  # Base-10 log of period in days
    feh = X[:, 1]    # [Fe/H] in dex
    
    # Physical constants (standard PL relation)
    # M_W = -2.76 * log_P - 4.05 (Gaia Wesenheit zero point)
    # Metallicity term: delta_M ~ -0.23 * [Fe/H] (typical Gaia dependence)
    M_W = -2.76 * log_P - 4.05 - 0.23 * feh
    return M_W