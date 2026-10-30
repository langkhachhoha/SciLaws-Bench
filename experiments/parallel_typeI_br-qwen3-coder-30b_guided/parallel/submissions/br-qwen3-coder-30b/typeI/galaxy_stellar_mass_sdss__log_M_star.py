"""Galaxy stellar mass as a function of color (r-i)."""
import numpy as np

USED_INPUTS = ["g", "r", "i", "DM"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract the color difference r-i from the input features
    # r-i is the difference between r-band and i-band magnitudes
    r_minus_i = X[:, 1] - X[:, 2]
    
    # Apply the fitted quadratic relationship between r-i color and log stellar mass
    # Derived from experimental data: log_M_star = 0.019791 * (r-i)^2 + 0.229061 * (r-i) + 9.320623
    log_M_star = 0.019791 * (r_minus_i ** 2) + 0.229061 * r_minus_i + 9.320623
    
    return log_M_star