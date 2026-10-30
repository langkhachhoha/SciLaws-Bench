"""Linear relationship between log_Mstar and oh."""
import numpy as np

USED_INPUTS = ["log_Mstar"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    return 0.2471 * x + 6.3933