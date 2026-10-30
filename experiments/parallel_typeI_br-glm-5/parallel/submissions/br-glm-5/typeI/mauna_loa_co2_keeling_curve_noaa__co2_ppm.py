"""Mauna Loa CO2 model: quadratic trend with 3 seasonal harmonics.
c(t) = c0 + b*(t-1958) + a*(t-1958)^2 + sum of sin/cos harmonics at 1, 2, 3 cycles/year.
This captures the accelerating increase in atmospheric CO2 and seasonal vegetation cycles.
"""
import numpy as np

USED_INPUTS = ["year_decimal"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    t = X[:, 0]
    t_cent = t - 1958
    
    # Quadratic trend coefficients
    c0 = 313.820658
    b = 0.791867
    a = 0.0127908895
    
    # Seasonal harmonic coefficients
    A1, B1 = -0.204443, 0.161556  # annual cycle
    A2, B2 = 0.159426, 0.325154   # semi-annual cycle  
    A3, B3 = 0.518641, -0.146571  # tri-annual cycle
    
    # Quadratic trend
    trend = c0 + b * t_cent + a * t_cent**2
    
    # Seasonal harmonics
    seasonal = (A1 * np.sin(2*np.pi*t) + B1 * np.cos(2*np.pi*t) +
                A2 * np.sin(4*np.pi*t) + B2 * np.cos(4*np.pi*t) +
                A3 * np.sin(6*np.pi*t) + B3 * np.cos(6*np.pi*t))
    
    return trend + seasonal