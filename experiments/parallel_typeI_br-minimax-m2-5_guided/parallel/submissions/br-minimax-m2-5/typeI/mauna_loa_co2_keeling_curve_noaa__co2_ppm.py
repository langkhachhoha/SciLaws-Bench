"""Mauna Loa CO2 (Keeling curve): quadratic trend + sinusoidal seasonal."""
import numpy as np

USED_INPUTS = ["year_decimal"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    x = X[:, 0]
    # Quadratic trend: a*x^2 + b*x + c
    a = 0.011824868307516044
    b = -45.47078972132175
    c = 44011.357791480026
    trend = a * x**2 + b * x + c
    
    # Seasonal component: sinusoidal with 1-year period
    # Extract month from year_decimal: month = (frac(x)) * 12
    month = (x - np.floor(x)) * 12
    seas_amp = -0.9551029896419583
    seas_phase = -1.3868756626725358
    seasonal = seas_amp * np.sin(2 * np.pi * month / 12 + seas_phase)
    
    return trend + seasonal