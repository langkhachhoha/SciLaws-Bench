"""Wind turbine power curve: exponential saturation with cut-in speed."""
import numpy as np

USED_INPUTS = ["wind_speed_mps"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    v = X[:, 0]
    v_ci = 2.6118
    scale = 6.8741
    n = 2.5128
    P_rated = 2023.89
    
    result = np.zeros_like(v)
    mask = v > v_ci
    if np.any(mask):
        x = (v[mask] - v_ci) / scale
        result[mask] = P_rated * (1 - np.exp(-x**n))
    return result