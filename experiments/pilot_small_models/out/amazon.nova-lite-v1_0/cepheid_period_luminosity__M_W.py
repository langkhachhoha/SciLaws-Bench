"""Linear fit using log_P and feh."""
import numpy as np

USED_INPUTS = ["log_P", "feh"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x_log_P = X[:, 0]
    x_feh = X[:, 1]
    return -3.44576553 * x_log_P + 0.99770349 * x_feh - 2.56419042