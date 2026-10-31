"""Mincer human capital earnings function: log_wage = a + b*SCHL + c*exp + d*exp^2"""
import numpy as np

USED_INPUTS = ["SCHL_years", "exp"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    s = X[:, 0]  # SCHL_years
    x = X[:, 1]  # exp
    # Mincer equation coefficients
    a = 8.433721
    b = 0.117152
    c = 0.05471033
    d = -0.00074221
    return a + b * s + c * x + d * x**2