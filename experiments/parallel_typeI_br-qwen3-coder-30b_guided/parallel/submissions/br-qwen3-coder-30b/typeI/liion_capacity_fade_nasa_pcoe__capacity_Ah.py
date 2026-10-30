"""Linear degradation model for battery capacity loss."""
import numpy as np

USED_INPUTS = ["cycle_index"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    k = X[:, 0]
    # Fitted parameters from data analysis
    # Q = -0.00397300 * k + 1.915311
    return -0.00397300 * k + 1.915311