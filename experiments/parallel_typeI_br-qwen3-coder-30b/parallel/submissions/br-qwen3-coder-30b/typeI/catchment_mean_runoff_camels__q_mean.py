"""Runoff as function of precipitation minus potential evapotranspiration."""
import numpy as np

USED_INPUTS = ["p_mean", "pet_mean"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    p_mean = X[:, 0]
    pet_mean = X[:, 1]
    # Runoff is proportional to excess precipitation (P - PET) when positive
    # q_mean = k * max(0, p_mean - pet_mean)
    # Based on the data, k ≈ 1.38
    k = 1.38
    return k * np.maximum(0.0, p_mean - pet_mean)