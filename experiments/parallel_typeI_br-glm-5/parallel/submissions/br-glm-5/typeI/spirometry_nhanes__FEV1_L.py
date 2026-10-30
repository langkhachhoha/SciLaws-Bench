"""NHANES spirometry reference equation for FEV1 in adult women."""
import numpy as np

USED_INPUTS = ["height_cm", "age"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    height = X[:, 0]  # height_cm
    age = X[:, 1]     # age
    return -1.567 + 0.0342 * height - 0.0266 * age