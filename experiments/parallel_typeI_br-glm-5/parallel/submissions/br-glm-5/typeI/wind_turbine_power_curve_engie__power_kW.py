"""Wind turbine power curve: cubic relationship with rated power saturation."""
import numpy as np

USED_INPUTS = ["wind_speed_mps"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    v = X[:, 0]
    k = 1.5  # Power coefficient (kW per (m/s)^3)
    P_rated = 2000  # Rated power (kW)
    
    # Power is proportional to v^3, capped at rated power
    P = k * v**3
    P = np.maximum(P, 0)  # No negative power
    P = np.minimum(P, P_rated)  # Saturate at rated power
    
    return P