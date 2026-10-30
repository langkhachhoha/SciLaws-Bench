"""Proportional relationship between B_phi and B_r/v_sw."""
import numpy as np

USED_INPUTS = ["B_r_nT", "v_sw_km_s"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    B_r = X[:, 0]
    v_sw = X[:, 1]
    # Using the fitted constant k ≈ -270.19
    return -270.19 * B_r / v_sw