"""Astrophysical scaling relation for nu_max based on delta_nu."""
import numpy as np

USED_INPUTS = ["delta_nu"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    delta_nu = X[:, 0]
    # Based on astrophysical theory and data fitting, nu_max scales as delta_nu^1.5
    # Using the best fit coefficient from the data: A ≈ 3.92
    return 3.9235 * (delta_nu ** 1.5)