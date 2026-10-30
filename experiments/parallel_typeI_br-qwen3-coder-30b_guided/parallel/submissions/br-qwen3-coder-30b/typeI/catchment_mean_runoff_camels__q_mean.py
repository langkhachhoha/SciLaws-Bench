"""Runoff as a function of precipitation and potential evapotranspiration."""
import numpy as np

USED_INPUTS = ["p_mean", "pet_mean"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    p_mean = X[:, 0]
    pet_mean = X[:, 1]
    
    # Runoff is the excess precipitation over potential evapotranspiration, 
    # but bounded to be non-negative
    return np.maximum(0, 1.2 * (p_mean - pet_mean))