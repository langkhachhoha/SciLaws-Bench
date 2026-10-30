"""Vickers hardness model: HV depends on VEC and the interaction between VEC and dHmix."""
import numpy as np

USED_INPUTS = ["VEC", "dHmix"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    VEC = X[:, 0]
    dHmix = X[:, 1]
    # HV = a*VEC + b*VEC*dHmix + c = VEC*(a + b*dHmix) + c
    a = 67.5
    b = -1.57
    c = 74.0
    return VEC * (a + b * dHmix) + c