"""Linear fit using log_P and feh inputs."""
import numpy as np

USED_INPUTS = ["log_P", "feh"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_P = X[:, 0]
    feh = X[:, 1]
    return -3.4573594 * log_P + 0.11356706 * feh - 2.67748815