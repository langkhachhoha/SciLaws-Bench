"""PGA model with magnitude, distance, and site class effects."""
import numpy as np

USED_INPUTS = ["Mw", "R_km", "ec8_B", "ec8_C", "ec8_D", "ec8_E", "sof_NF", "sof_TF"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Mw = X[:, 0]
    R_km = X[:, 1]
    ec8_B = X[:, 2]
    ec8_C = X[:, 3]
    ec8_D = X[:, 4]
    ec8_E = X[:, 5]
    sof_NF = X[:, 6]
    sof_TF = X[:, 7]
    
    # Magnitude scaling coefficient
    mag_coeff = 0.4317
    
    # Distance decay coefficient  
    dist_coeff = 0.15
    
    # Site class coefficients (relative to reference class)
    site_B = 0.10  # Stiff soil (B class)
    site_C = 0.05  # Medium soil (C class) 
    site_D = -0.10 # Soft soil (D class)
    site_E = 0.05  # Mixed soil (E class)
    
    # Base magnitude term
    base = mag_coeff * Mw
    
    # Distance attenuation term
    distance_term = dist_coeff * np.log10(R_km)
    
    # Site class effects
    site_term = site_D * ec8_D + site_B * ec8_B + site_C * ec8_C + site_E * ec8_E
    
    # Fault type effects (small contribution)
    fault_term = 0.0 * sof_NF + 0.0 * sof_TF
    
    # Constant offset
    offset = -0.3718
    
    return base - distance_term + site_term + fault_term + offset