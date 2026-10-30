"""ME is proportional to GDP * TP * UR"""
import numpy as np

USED_INPUTS = ["GDP", "TP", "UR"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    GDP = X[:, 0]
    TP = X[:, 1]
    UR = X[:, 2]
    # Constant derived from data: ~7.1424e-06
    return 7.1424e-06 * GDP * TP * UR