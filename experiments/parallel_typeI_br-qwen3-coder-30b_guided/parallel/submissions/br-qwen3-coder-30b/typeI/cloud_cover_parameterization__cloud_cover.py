"""Cloud cover parameterization based on liquid water mixing ratio, relative humidity, and vertical gradients."""
import numpy as np

USED_INPUTS = ["q_c", "q_i", "RH", "T", "dz_RH"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q_c = X[:, 0]
    q_i = X[:, 1]
    RH = X[:, 2]
    T = X[:, 3]
    dz_RH = X[:, 4]
    
    # Base saturation behavior with q_c
    # Cloud cover increases with q_c following a saturation curve
    base_cloud = 1.0 - np.exp(-3500.0 * q_c)
    
    # RH effect - sigmoidal threshold around 0.7
    rh_effect = 1.0 / (1.0 + np.exp(-20.0 * (RH - 0.7)))
    
    # dz_RH effect - linear dependence
    # Normalize dz_RH to [-1, 1] range for stability
    dz_normalized = np.clip(dz_RH / 0.001, -1.0, 1.0)
    dz_effect = 0.3 * dz_normalized
    
    # Combine effects with some additional considerations for ice
    # Ice reduces cloud cover slightly
    ice_effect = 0.1 * q_i / 0.000129
    
    # Final cloud cover calculation
    cloud_cover = base_cloud * rh_effect + dz_effect - ice_effect
    
    # Ensure cloud cover is bounded between 0 and 1
    return np.clip(cloud_cover, 0.0, 1.0)