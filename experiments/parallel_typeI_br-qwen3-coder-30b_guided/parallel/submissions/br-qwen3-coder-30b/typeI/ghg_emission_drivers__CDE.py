"""Proportional relationship between CO2 emissions and GDP*TP with a fitted constant."""
import numpy as np

USED_INPUTS = ["GDP", "TP"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    gdp = X[:, 0]
    tp = X[:, 1]
    # Using the median ratio from our analysis as the fitted constant
    return 0.174916 * gdp * tp