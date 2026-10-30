"""Pythagorean expectation with exponent 2."""
import numpy as np

USED_INPUTS = ["R", "RA"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    R = X[:, 0]
    RA = X[:, 1]
    return (R**2) / (R**2 + RA**2)