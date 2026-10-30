"""Xu-Randall style cloud fraction parameterization with ice weighting and dz_RH correction."""
import numpy as np

USED_INPUTS = ["q_c", "q_i", "RH", "T", "dz_RH"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q_c = X[:, 0]  # cloud liquid water mixing ratio
    q_i = X[:, 1]  # cloud ice mixing ratio
    RH = X[:, 2]   # relative humidity
    T = X[:, 3]    # temperature (K)
    dz_RH = X[:, 4]  # vertical RH gradient
    
    # Saturation specific humidity (Tetens formula for liquid water)
    es = 611.2 * np.exp(17.67 * (T - 273.15) / (T - 29.65))
    qs = 0.622 * es / 100000.0
    
    # Fitted parameters
    k = 20.0
    n = 2.5
    c = 0.6
    d = -100.0
    
    # Xu-Randall form with ice weighting
    ratio = (q_c + c * q_i) / qs
    C = 1.0 - np.exp(-k * ratio * RH**n) + d * dz_RH
    
    # Clamp to [0, 1]
    return np.clip(C, 0.0, 1.0)