"""Earthquake ground motion model based on magnitude, distance, and site conditions."""
import numpy as np

USED_INPUTS = ["Mw", "R_km", "ec8_B", "ec8_C", "ec8_D", "ec8_E", "sof_NF", "sof_TF"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    Mw = X[:, 0]
    R_km = X[:, 1]
    ec8_B = X[:, 2]
    ec8_C = X[:, 3]
    ec8_D = X[:, 4]
    ec8_E = X[:, 5]
    sof_NF = X[:, 6]
    sof_TF = X[:, 7]
    
    # Handle distance = 0 case to avoid log10(0)
    R_safe = np.where(R_km == 0, 1e-10, R_km)
    
    # Apply the empirical formula derived from the simulator behavior
    # log10(PGA) = 1.71 + 0.646*Mw - 2.48*log10(R) + 0.205*ec8_B + 0.367*ec8_C + 0.309*ec8_D + 0.280*ec8_E - 0.017*sof_NF - 0.074*sof_TF
    log10_pga = (1.71 + 
                 0.646 * Mw - 
                 2.48 * np.log10(R_safe) + 
                 0.205 * ec8_B + 
                 0.367 * ec8_C + 
                 0.309 * ec8_D + 
                 0.280 * ec8_E - 
                 0.017 * sof_NF - 
                 0.074 * sof_TF)
    
    return log10_pga