"""HV = a + b*VEC^2 + c*VEC*dHmix (3-constant model with VEC-dHmix interaction)."""
import numpy as np

USED_INPUTS = ["VEC", "dHmix"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    VEC = X[:, 0]
    dHmix = X[:, 1]
    return 245.43 + 7.117 * VEC**2 + (-1.4703) * VEC * dHmix