"""Nitrous oxide emissions proportional to total population times GDP per capita."""
import numpy as np

USED_INPUTS = ["GDP", "TP"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # NOE = k * TP * GDP
    # Using fitted constant k = 2.81e-05 from experimental data
    k = 2.81e-05
    gdp = X[:, 0]
    tp = X[:, 1]
    return k * tp * gdp