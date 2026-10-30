"""Multiplicative relationship across all input variables."""
import numpy as np

USED_INPUTS = ["GDP", "TP", "AP", "DP", "UR", "AT"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # EC = k * GDP * TP * AP * DP * UR * AT
    # Using the average ratio from the data: k ≈ -1.67e-9
    k = -1.6671177962022865e-09
    return k * X[:, 0] * X[:, 1] * X[:, 2] * X[:, 3] * X[:, 4] * X[:, 5]