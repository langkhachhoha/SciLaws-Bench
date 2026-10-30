"""Solar collector efficiency model based on irradiance and temperature differences."""
import numpy as np

USED_INPUTS = ["G_W_m2", "T_in_C", "T_amb_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    G = X[:, 0]
    T_in = X[:, 1]
    T_amb = X[:, 2]
    
    # Solar collector efficiency model
    # eta = A * G / (G + B) + C * (T_amb - T_in) + D
    # Based on the data patterns observed
    
    # These coefficients are chosen to match the general behavior seen in the data:
    # - Efficiency increases with irradiance G
    # - Efficiency decreases with increasing T_in  
    # - Efficiency increases with increasing T_amb
    A = 0.78
    B = 456.0
    C = 0.005
    D = 0.35
    
    eta = A * G / (G + B) + C * (T_amb - T_in) + D
    
    # Clip to physical bounds (0 to 1)
    eta = np.clip(eta, 0, 1)
    
    return eta