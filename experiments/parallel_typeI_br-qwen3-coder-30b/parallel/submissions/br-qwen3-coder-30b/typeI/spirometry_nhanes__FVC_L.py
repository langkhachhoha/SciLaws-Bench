"""Forced vital capacity model for adolescent males based on height and age."""
import numpy as np

USED_INPUTS = ["age", "height_cm"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    age = X[:, 0]
    height_cm = X[:, 1]
    # FVC = 5.40e-08 * height^3 * age
    return 5.40e-08 * (height_cm ** 3) * age