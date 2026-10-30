"""Hack's Law: Main-stem river length scales as power law of drainage area."""
import numpy as np

USED_INPUTS = ["upland_area_skm"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    A = X[:, 0]
    k = 1.94
    h = 0.535
    return k * A**h