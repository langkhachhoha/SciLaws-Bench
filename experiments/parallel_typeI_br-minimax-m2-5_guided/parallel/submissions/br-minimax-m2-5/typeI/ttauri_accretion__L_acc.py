"""Linear scaling of accretion luminosity with stellar luminosity: L_acc ∝ L_star^1.5"""
import numpy as np

USED_INPUTS = ["logL_star"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    return 1.5 * x - 1.5