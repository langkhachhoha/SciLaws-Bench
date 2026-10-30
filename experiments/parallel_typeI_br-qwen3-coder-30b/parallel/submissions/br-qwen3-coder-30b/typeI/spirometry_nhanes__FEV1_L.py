"""Simple linear model with age and height effects."""
import numpy as np

USED_INPUTS = ["age", "height_cm"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    age = X[:, 0]
    height = X[:, 1]
    # Based on the correlation patterns observed, a simple linear combination
    # with negative coefficients for both age and height seems appropriate
    # The correlation with age is around -0.29 and with height around -0.22
    # We'll use a simple linear model with fitted constants
    return 3.5 - 0.02 * age - 0.01 * height