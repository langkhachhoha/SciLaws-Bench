"""Exponential decay of battery capacity with cycle count: Q = a*exp(-b*k) + c"""
import numpy as np

USED_INPUTS = ["cycle_index"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    k = X[:, 0]
    a = 1.270293
    b = 0.004096
    c = 0.642440
    return a * np.exp(-b * k) + c