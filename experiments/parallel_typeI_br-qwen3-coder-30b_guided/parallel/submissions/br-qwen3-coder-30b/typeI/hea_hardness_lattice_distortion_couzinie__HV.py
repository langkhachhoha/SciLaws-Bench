"""Vickers hardness as a function of valence electron concentration and mixing enthalpy with interaction term."""
import numpy as np

USED_INPUTS = ["VEC", "dHmix"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Interaction model: HV = a*VEC + b*dHmix + c*VEC*dHmix + d
    vec = X[:, 0]
    dhmix = X[:, 1]
    return 83.924 * vec + (-1.369) * dhmix + (-1.243) * vec * dhmix + 1.284