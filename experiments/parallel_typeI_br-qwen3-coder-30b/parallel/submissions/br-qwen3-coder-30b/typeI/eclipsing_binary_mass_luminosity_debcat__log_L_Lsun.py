"""Stellar luminosity scaling relation for main sequence stars."""
import numpy as np

USED_INPUTS = ["log_M_Msun"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # Based on stellar physics: log(L/Lsun) = 3.5 * log(M/Msun) + 0.32
    # Using the best fit from the data: log(L/Lsun) = 3.4445 * log(M/Msun) + 0.3159
    return 3.4445 * x + 0.3159