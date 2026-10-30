"""Power law fit for proton-proton total cross-section."""
import numpy as np

USED_INPUTS = ["s"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    s = X[:, 0]
    # From fitting log-log data: sigma_tot = 25.6287 * s^0.0734
    A = 25.6287
    B = 0.0734
    return A * (s ** B)