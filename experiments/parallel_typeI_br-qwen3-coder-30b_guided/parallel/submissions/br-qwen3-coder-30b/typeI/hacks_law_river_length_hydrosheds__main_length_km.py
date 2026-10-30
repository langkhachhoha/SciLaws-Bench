"""River length scales with upstream drainage area as a power law with exponent ~0.55."""
import numpy as np

USED_INPUTS = ["upland_area_skm"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    A = X[:, 0]
    # Best fit from experimental data: L = 1.7464 * A^0.5481
    return 1.746442 * (A ** 0.548055)