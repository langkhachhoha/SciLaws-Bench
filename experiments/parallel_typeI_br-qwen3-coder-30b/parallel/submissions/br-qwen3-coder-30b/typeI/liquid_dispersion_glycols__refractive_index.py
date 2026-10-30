"""Refractive index of ethylene glycol as a function of wavelength and temperature.
Uses Cauchy dispersion relation with temperature correction."""
import numpy as np

USED_INPUTS = ["lambda_um", "temperature_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    lam = X[:, 0]  # wavelength in micrometers
    T = X[:, 1]    # temperature in Celsius
    
    # Cauchy dispersion coefficients at 23°C
    A = 2.0126
    B = 0.0127
    C = -0.0002
    
    # Temperature correction coefficient (per degree Celsius)
    temp_coeff = -0.00029
    
    # Calculate n^2 using Cauchy dispersion relation
    lam_sq = lam ** 2
    n_squared = A + B / lam_sq + C / (lam_sq ** 2)
    
    # Take square root to get refractive index
    n_23 = np.sqrt(n_squared)
    
    # Apply temperature correction
    n = n_23 + temp_coeff * (T - 23.0)
    
    return n