"""Saturating exponential function matching the simulator mechanism."""
import numpy as np

USED_INPUTS = ["pet_over_p"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    pet_over_p = X[:, 0]
    # The underlying mechanism is a saturating exponential function
    # et_over_p = 1 - exp(-pet_over_p)
    return 1.0 - np.exp(-pet_over_p)