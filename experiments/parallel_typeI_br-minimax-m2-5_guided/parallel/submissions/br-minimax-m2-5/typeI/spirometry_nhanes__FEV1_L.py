"""FEV1 = height^2 * (a + b*age) - FEV1 scales with height squared and declines linearly with age."""
import numpy as np

USED_INPUTS = ["age", "height_cm"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    age = X[:, 0]
    height_cm = X[:, 1]
    a = 0.000150
    b = -0.000001005
    return height_cm**2 * (a + b * age)