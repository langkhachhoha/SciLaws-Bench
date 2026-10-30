"""Refractive index of ethylene glycol as a function of wavelength and temperature.
Uses Cauchy's equation for wavelength dependence and linear temperature correction."""
import numpy as np

USED_INPUTS = ["lambda_um", "temperature_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    lambda_um = X[:, 0]
    temperature_C = X[:, 1]
    
    # Model parameters determined from data analysis:
    # n = A + B/lambda^2 + C*T
    # Based on the data patterns and physical considerations:
    # A ≈ 1.422 (baseline refractive index)
    # B ≈ 0.006 (wavelength dependence coefficient)
    # C ≈ -0.0008 (temperature dependence coefficient)
    
    A = 1.422
    B = 0.006
    C = -0.0008
    
    # Calculate refractive index
    n = A + B / (lambda_um ** 2) + C * temperature_C
    
    return n