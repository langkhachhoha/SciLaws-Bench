"""Power law relationship between mass and radius for sub-stellar objects."""
import numpy as np

USED_INPUTS = ["M"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Using the overall power law fit from the data
    # R = 2.7016 * M^0.1670
    mass = X[:, 0]
    return 2.7016 * (mass ** 0.1670)