"""Mass-luminosity relationship for main-sequence stars: log(L/L_sun) = a * log(M/M_sun) + b."""
import numpy as np

USED_INPUTS = ["log_M_Msun"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    return 3.28 * x + 0.27