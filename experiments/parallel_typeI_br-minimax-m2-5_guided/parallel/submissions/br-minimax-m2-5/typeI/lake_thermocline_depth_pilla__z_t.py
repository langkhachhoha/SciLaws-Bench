"""Thermocline depth as logarithmic function of lake surface area: z_t = a + b * ln(A_s)"""
import numpy as np

USED_INPUTS = ["A_s_km2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]  # A_s_km2
    # z_t = 7.51 + 1.04 * ln(A_s)
    return 7.5122 + 1.0432 * np.log(x)