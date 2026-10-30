"""Cauchy dispersion equation with extended term and linear temperature dependence.

n = A + B/λ² + C/λ⁴ + D*T

This is the classic Cauchy formula for optical dispersion (n = A + B/λ² + C/λ⁴)
combined with a linear temperature coefficient typical for liquids.
"""
import numpy as np

USED_INPUTS = ["lambda_um", "temperature_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    lam = X[:, 0]  # wavelength in um
    T = X[:, 1]    # temperature in °C
    
    # Fitted parameters from least squares optimization
    A = 1.4261275822
    B = 0.0041448778
    C = -0.000047826065
    D = -0.000288976517
    
    return A + B/lam**2 + C/lam**4 + D*T