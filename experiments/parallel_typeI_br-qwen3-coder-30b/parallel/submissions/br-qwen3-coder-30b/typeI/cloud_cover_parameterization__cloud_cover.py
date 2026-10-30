"""Cloud cover as a function of cloud liquid water mixing ratio, ice mixing ratio, and relative humidity."""
import numpy as np

USED_INPUTS = ["q_c", "q_i", "RH", "T", "dz_RH"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    q_c = X[:, 0]
    q_i = X[:, 1] 
    RH = X[:, 2]
    T = X[:, 3]
    dz_RH = X[:, 4]
    
    # Compute sum of liquid and ice water mixing ratios
    q_sum = q_c + q_i
    
    # Cloud cover is modeled as a bounded linear function of (q_c + q_i) * RH
    # with a coefficient of 2200 and offset of 1000 to ensure proper bounds
    cloud_cover = np.minimum(1.0, np.maximum(0.0, q_sum * RH * 2200.0 - 1000.0))
    
    return cloud_cover