"""Linear model with log_Kow and foc inputs."""
import numpy as np

USED_INPUTS = ["log_Kow", "foc"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    log_Kow = X[:, 0]
    foc = X[:, 1]
    return 0.5435 * log_Kow + 3.0532 * foc - 2.3022