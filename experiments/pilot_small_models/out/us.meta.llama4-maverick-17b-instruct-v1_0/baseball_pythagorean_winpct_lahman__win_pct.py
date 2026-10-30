"""Win percentage as a function of R and RA."""
import numpy as np

USED_INPUTS = ["R", "RA"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    ratio = X[:, 0] / X[:, 1]
    return 2.3690952948866215 * ratio / (ratio + 3.6622249616413103)