"""Quadratic fit to CO2 concentration over time."""
import numpy as np

USED_INPUTS = ["year_decimal"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    t = X[:, 0]
    # Quadratic fit: y = a*t^2 + b*t + c
    # Coefficients derived from the Mauna Loa CO2 data
    a = 0.01333287
    b = -51.46193981
    c = 49961.98
    return a * t**2 + b * t + c