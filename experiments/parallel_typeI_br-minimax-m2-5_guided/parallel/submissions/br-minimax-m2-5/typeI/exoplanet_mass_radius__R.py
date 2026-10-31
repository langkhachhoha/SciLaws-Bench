"""Hill function (Michaelis-Menten) with high-mass decrease: R = R_sat * M^p / (M^p + K^p) - alpha * log(1+M/M0).
This models: low-M rocky planets increasing with M, approaching Jupiter-like radius at mid-high M, slight decrease at very high M (brown dwarfs)."""
import numpy as np

USED_INPUTS = ["M"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    M = X[:, 0]
    # Hill function parameters fitted to observations
    R_sat = 18.868   # Maximum radius (R_earth)
    K = 73.915       # Half-saturation mass (M_earth)
    p = 0.772        # Hill coefficient
    alpha = 1.727    # High-mass decrease coefficient
    M0 = 188.6       # Scale for high-mass decrease
    
    # Hill part: saturation curve
    hill = R_sat * np.power(M, p) / (np.power(M, p) + np.power(K, p))
    
    # High-mass decrease: slow logarithmic decrease
    dec = alpha * np.log1p(M / M0)
    
    return hill - dec