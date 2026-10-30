"""Linear model combining age and height effects on forced vital capacity."""
import numpy as np

USED_INPUTS = ["age", "height_cm"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    age = X[:, 0]
    height_cm = X[:, 1]
    # Coefficients derived from linear regression on training data
    return 0.0552 * height_cm + 0.1086 * age - 6.0714