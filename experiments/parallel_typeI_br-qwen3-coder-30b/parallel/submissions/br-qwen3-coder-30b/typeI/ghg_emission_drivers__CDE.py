"""Proportional relationship with GDP, TP, and AP. CDE = k * GDP * TP * AP where k ≈ 0.0046."""
import numpy as np

USED_INPUTS = ["GDP", "TP", "AP"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # k ≈ 0.004619 based on all data points
    k = 0.004619
    gdp = X[:, 0]
    tp = X[:, 1]
    ap = X[:, 2]
    return k * gdp * tp * ap