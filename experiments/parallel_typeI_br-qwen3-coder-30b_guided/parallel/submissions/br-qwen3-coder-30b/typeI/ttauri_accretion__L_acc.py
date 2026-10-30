"""Accretion luminosity scales linearly with stellar luminosity."""
import numpy as np

USED_INPUTS = ["logL_star"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # Based on the strong linear correlation found in the data
    # log(L_acc/Lsun) = 1.56 * log(L_star/Lsun) - 1.33
    return 1.56 * x - 1.33