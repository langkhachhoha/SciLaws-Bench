"""Smooth broken power law for Mars crater size-frequency distribution.
The cumulative crater density follows a broken power law with smooth transition:
N(>=D) = N0 * D^(-b1) * (1 + (D/D_t)^alpha)^((b1-b2)/alpha)

This captures the transition from shallower slope (b1≈1.1) at small diameters
to steeper slope (b2≈2.7) at large diameters, with transition around D_t≈33 km.
"""
import numpy as np

USED_INPUTS = ["D_lower_km"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    D = X[:, 0]
    
    # Fitted parameters
    N0 = 2.0764e-03    # Normalization constant
    b1 = 1.1           # Power law exponent for D << D_t
    b2 = 2.7           # Power law exponent for D >> D_t
    D_t = 33.0         # Transition diameter (km)
    alpha = 5.0        # Transition sharpness
    
    # Smooth broken power law formula
    # The exponent of the transition term
    exponent = (b1 - b2) / alpha  # = -0.32
    
    # N = N0 * D^(-b1) * (1 + (D/D_t)^alpha)^(b1-b2)/alpha
    N = N0 * D**(-b1) * (1 + (D/D_t)**alpha)**exponent
    
    return N