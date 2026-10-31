"""Parker spiral approximation: B_phi ≈ C * B_r / v_sw"""
import numpy as np

USED_INPUTS = ["B_r_nT", "v_sw_km_s"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    B_r = X[:, 0]
    v_sw = X[:, 1]
    C = -280.88
    return C * B_r / v_sw