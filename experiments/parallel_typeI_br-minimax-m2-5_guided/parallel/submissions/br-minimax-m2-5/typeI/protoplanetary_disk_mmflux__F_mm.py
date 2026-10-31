"""Quadratic relationship between 1.3mm flux and stellar mass in log-log space: log10(F) = A * (log10(M) - x0)^2 + B. Uses 2 fitted constants (A, B) with x0 fixed at -1.75."""
import numpy as np

USED_INPUTS = ["log10_M_star_SDF00"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # Fixed vertex at x0 = -1.75, A ≈ 0.311, B ≈ -2.52
    A = 0.3114
    B = -2.5195
    x0 = -1.75
    return A * (x - x0)**2 + B