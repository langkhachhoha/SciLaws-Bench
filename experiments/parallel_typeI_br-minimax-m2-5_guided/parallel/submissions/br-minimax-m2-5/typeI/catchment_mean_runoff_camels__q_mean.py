"""Runoff as water balance: Q = max(0, P - k*PET) where k ≈ 0.687.

This represents a simple water-balance model where actual evapotranspiration 
is a constant fraction (about 69%) of potential evapotranspiration, and 
runoff is the residual precipitation after ET. The max(0,...) clips negative 
values to zero (when precipitation is less than ET, no runoff occurs)."""
import numpy as np

USED_INPUTS = ["p_mean", "pet_mean"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    p_mean = X[:, 0]
    pet_mean = X[:, 1]
    # Runoff = max(0, P - k*PET) where k ~ 0.687
    # Represents: Q = P - ET, where ET = k*PET (constant fraction of PET)
    return np.maximum(0, p_mean - 0.687 * pet_mean)