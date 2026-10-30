"""Schreiber's 1904 formula for evapotranspiration partitioning."""
import numpy as np

USED_INPUTS = ["pet_over_p"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    phi = X[:, 0]  # aridity index (PET/P)
    return 1 - np.exp(-phi)