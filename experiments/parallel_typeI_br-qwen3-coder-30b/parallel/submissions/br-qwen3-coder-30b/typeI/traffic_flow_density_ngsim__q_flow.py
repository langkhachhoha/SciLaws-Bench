"""Traffic flow model based on fundamental diagram: q = a * k * (k_max - k)"""
import numpy as np

USED_INPUTS = ["k_veh_km_lane"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    k = X[:, 0]
    # Using fitted constants from analysis
    k_max = 339.0
    a = 0.107
    return a * k * (k_max - k)