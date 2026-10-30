"""Mincer-type earnings function with log-linear experience.

log_wage = a + b1*S + b2*log(1+exp) + b3*exp

where S is years of schooling and exp is potential experience.
"""
import numpy as np

USED_INPUTS = ["SCHL_years", "exp"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    S = X[:, 0]
    exp = X[:, 1]
    a = 8.415892
    b1 = 0.114181
    b2 = 0.321222
    b3 = -0.005083
    return a + b1 * S + b2 * np.log(1 + exp) + b3 * exp