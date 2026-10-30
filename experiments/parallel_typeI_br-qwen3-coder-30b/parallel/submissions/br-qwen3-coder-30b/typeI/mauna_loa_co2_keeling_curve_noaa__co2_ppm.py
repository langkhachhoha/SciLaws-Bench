"""Quadratic fit modeling CO2 concentration growth."""
import numpy as np

USED_INPUTS = ["year_decimal"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    t = X[:, 0]
    # Coefficients from fitting the data
    # y = 0.01333729 * t^2 - 51.4670 * t + 49954.58
    return 0.01333729 * t**2 - 51.4670 * t + 49954.58