"""Power law scaling: delta_nu = a * nu_max^b for red giant asteroseismology."""
import numpy as np

USED_INPUTS = ["nu_max"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    return 0.277071 * x**0.756018