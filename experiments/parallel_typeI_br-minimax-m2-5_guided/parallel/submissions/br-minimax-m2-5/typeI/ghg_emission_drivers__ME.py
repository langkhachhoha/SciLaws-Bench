"""Methane emissions as proportional to population times square root of urbanization."""
import numpy as np

USED_INPUTS = ["GDP", "TP", "UR"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    TP = X[:, 1]  # Total population
    UR = X[:, 2]  # Urbanization rate (percentage)
    # Formula: ME = a * TP * sqrt(UR)
    # Based on power-law fitting showing TP^1 and UR^0.5
    a = 4.67  #fitted constant
    return a * TP * np.sqrt(UR)