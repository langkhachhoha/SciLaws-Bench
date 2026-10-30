"""Absolute Gaia Wesenheit magnitude as a function of log_P and feh."""
import numpy as np

USED_INPUTS = ["log_P", "feh"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_P = X[:, 0]
    feh = X[:, 1]
    return -3.80 * log_P + 0.70 * feh + 0.83 * log_P*feh - 2.37