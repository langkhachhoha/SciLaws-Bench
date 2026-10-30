"""Power law fit for nu_max vs delta_nu relationship."""
import numpy as np

USED_INPUTS = ["delta_nu"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Fitted parameters from experimental data
    A = 6.31091306
    alpha = 1.25755180
    delta_nu = X[:, 0]
    return A * (delta_nu ** alpha)