"""Linear relationship between M_W, log_P, and feh."""
import numpy as np

USED_INPUTS = ["log_P", "feh"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_P = X[:, 0]
    feh = X[:, 1]
    # Coefficients determined from the data
    return -3.268 * log_P + -0.425 * feh + -2.833