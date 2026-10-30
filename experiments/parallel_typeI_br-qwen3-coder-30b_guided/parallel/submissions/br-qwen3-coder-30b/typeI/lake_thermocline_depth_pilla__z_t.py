"""Power law fit to lake surface area vs thermocline depth."""
import numpy as np

USED_INPUTS = ["A_s_km2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    return 6.93 * (x ** 0.12)