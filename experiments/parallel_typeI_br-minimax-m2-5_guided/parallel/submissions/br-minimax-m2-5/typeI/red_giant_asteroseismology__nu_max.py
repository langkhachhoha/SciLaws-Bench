"""Power law scaling of ν_max with Δν for red giant asteroseismology."""
import numpy as np

USED_INPUTS = ["delta_nu"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    return 7.1 * np.power(x, 1.21)