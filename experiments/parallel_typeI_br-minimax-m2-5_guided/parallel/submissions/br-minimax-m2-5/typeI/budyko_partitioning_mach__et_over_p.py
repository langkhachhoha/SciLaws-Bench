"""Budyko-Signor curve: E/P = 1 - exp(-φ), where φ = PET/P is the aridity index.
This classic catchment hydrology formula describes the long-term partitioning 
of precipitation between evapotranspiration and runoff, with no free parameters."""
import numpy as np

USED_INPUTS = ["pet_over_p"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    phi = X[:, 0]
    return 1 - np.exp(-phi)