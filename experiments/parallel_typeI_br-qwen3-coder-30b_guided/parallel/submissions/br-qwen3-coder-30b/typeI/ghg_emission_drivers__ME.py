"""ME ~ GDP * TP * UR^(0.5)"""
import numpy as np

USED_INPUTS = ["GDP", "TP", "UR"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    GDP = X[:, 0]
    TP = X[:, 1]
    UR = X[:, 2]
    # Based on our analysis, ME = 7.32e-03 * GDP * TP * UR^0.5
    # For simplicity in the final formula, we'll use a rounded constant
    return 7.32e-03 * GDP * TP * (UR ** 0.5)