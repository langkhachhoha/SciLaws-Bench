"""Quadratic fit to log10_M_star_SDF00 with rounded coefficients."""
import numpy as np

USED_INPUTS = ["log10_M_star_SDF00"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # Using the best-fit quadratic model: y = 0.2996*x^2 + 1.0789*x - 1.5783
    return 0.2996 * x**2 + 1.0789 * x - 1.5783