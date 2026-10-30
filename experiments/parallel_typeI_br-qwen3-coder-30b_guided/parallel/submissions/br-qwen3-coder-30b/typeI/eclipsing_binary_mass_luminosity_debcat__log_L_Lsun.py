"""Stellar luminosity-main sequence star mass relationship."""
import numpy as np

USED_INPUTS = ["log_M_Msun"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # Best fit from experimental data: log(L/L☉) = 3.73 * log(M/M☉) + 0.40
    return 3.73 * x + 0.40