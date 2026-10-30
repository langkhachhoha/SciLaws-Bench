"""Linear model capturing the relationship between VEC, dHmix, and HV."""
import numpy as np

USED_INPUTS = ["VEC", "dHmix"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Based on the linear regression analysis, the relationship appears to be:
    # HV = 33.62*VEC - 5.40*dHmix + 266.75
    vec = X[:, 0]
    dhmix = X[:, 1]
    return 33.62 * vec - 5.40 * dhmix + 266.75