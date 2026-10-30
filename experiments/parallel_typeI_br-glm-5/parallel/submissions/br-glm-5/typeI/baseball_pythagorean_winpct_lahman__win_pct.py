"""Pythagorean expectation: win_pct = R^2 / (R^2 + RA^2)

Classical baseball formula relating runs scored (R) and runs allowed (RA)
to winning percentage. The simulator adds binomial noise around this expectation.
"""
import numpy as np

USED_INPUTS = ["R", "RA", "G"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    R = X[:, 0]
    RA = X[:, 1]
    # G is X[:, 2] but not used in the Pythagorean expectation (only affects variance)
    return R**2 / (R**2 + RA**2)