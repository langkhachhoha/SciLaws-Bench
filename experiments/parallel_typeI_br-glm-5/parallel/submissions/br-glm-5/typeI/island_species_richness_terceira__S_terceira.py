"""Power law: Arthropod species richness follows S = a / d^1.5"""
import numpy as np

USED_INPUTS = ["d"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    d = X[:, 0]
    return 532.0 / np.power(d, 1.5)