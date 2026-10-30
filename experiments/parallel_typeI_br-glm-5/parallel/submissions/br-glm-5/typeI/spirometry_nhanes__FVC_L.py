"""Spirometry FVC model: Power of height plus linear age term."""
import numpy as np

USED_INPUTS = ["age", "height_cm"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    age = X[:, 0]
    height_cm = X[:, 1]
    # FVC = a * height^b + c * age
    a = 1.1559763e-08
    b = 3.762516
    c = 0.106978
    return a * np.power(height_cm, b) + c * age