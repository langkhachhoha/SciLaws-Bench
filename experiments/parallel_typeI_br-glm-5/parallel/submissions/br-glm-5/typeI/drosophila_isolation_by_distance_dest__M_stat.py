"""Isolation by distance: genetic differentiation M scales with square root of geographic distance."""
import numpy as np

USED_INPUTS = ["distance_km"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    d = X[:, 0]
    a = 0.0014037
    return a * np.sqrt(d)