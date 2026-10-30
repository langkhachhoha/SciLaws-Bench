"""Vickers hardness as a function of valence electron concentration and mixing enthalpy with interaction term."""
import numpy as np

USED_INPUTS = ["VEC", "dHmix"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Coefficients determined from experimental data
    a = 84.55
    b = -0.93
    c = -1.43
    d = -13.44
    
    vec = X[:, 0]
    dhmix = X[:, 1]
    
    # Model: HV = a*VEC + b*dHmix + c*VEC*dHmix + d
    return a * vec + b * dhmix + c * vec * dhmix + d