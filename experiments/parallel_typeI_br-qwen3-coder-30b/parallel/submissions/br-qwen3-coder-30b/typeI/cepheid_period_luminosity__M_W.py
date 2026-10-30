"""Linear fit for classical Cepheid absolute Wesenheit magnitude."""
import numpy as np

USED_INPUTS = ["log_P", "feh"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_P = X[:, 0]
    feh = X[:, 1]
    return -3.391043 * log_P + 0.091352 * feh - 2.738238