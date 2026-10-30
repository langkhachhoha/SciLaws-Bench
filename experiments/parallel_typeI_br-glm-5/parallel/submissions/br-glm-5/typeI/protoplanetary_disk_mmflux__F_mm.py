"""Quadratic relationship between stellar mass and 1.3mm flux density.
log10 F = 0.31 * log10(M)^2 + 1.10 * log10(M) - 1.57
Corresponds to a power-law index that increases with mass."""
import numpy as np

USED_INPUTS = ["log10_M_star_SDF00"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]  # log10 stellar mass
    return 0.31 * x**2 + 1.10 * x - 1.57