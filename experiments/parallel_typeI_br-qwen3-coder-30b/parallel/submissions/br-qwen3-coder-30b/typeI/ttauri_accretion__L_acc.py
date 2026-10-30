"""Linear relationship between logL_acc and logL_star."""
import numpy as np

USED_INPUTS = ["logL_star"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # Based on the fitted model: logL_acc = 1.581412 * logL_star - 1.278319
    return 1.581412 * x - 1.278319