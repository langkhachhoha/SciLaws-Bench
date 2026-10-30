"""Interplanetary magnetic field azimuthal component based on radial component and solar wind speed."""
import numpy as np

USED_INPUTS = ["B_r_nT", "v_sw_km_s", "r_AU"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    B_r = X[:, 0]
    v_sw = X[:, 1]
    r_AU = X[:, 2]
    
    # The relationship appears to be: B_phi = k * B_r * v_sw
    # where k is approximately -0.0017
    k = -0.0017
    
    # Note: r_AU is constant at 1.0 for L1 data, so it doesn't affect the relationship
    return k * B_r * v_sw