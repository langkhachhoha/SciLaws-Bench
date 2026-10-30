"""Isolation by distance model: M_stat = A * (1 - exp(-d/B)) where A≈0.1411 and B≈3021.27"""
import numpy as np

USED_INPUTS = ["distance_km"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    d = X[:, 0]
    A = 0.141096
    B = 3021.273105
    return A * (1 - np.exp(-d/B))