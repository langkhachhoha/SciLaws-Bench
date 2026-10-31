"""Cauchy dispersion with linear temperature correction for ethylene glycol refractive index.
n = A + B/lambda^2 + C*(T - 23), where lambda is in micrometres and T in degrees Celsius."""
import numpy as np

USED_INPUTS = ["lambda_um", "temperature_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    lam = X[:, 0]
    T = X[:, 1]
    # Cauchy formula with temperature correction: n = 1.4196 + 0.00386/lambda^2 - 0.00028*(T-23)
    return 1.419575 + 0.003859 / (lam**2) - 0.000280 * (T - 23.0)