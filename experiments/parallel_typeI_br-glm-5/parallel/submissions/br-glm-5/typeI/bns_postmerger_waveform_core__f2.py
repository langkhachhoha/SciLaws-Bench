"""Post-merger gravitational-wave spectral peak frequency.

The dominant frequency scales inversely with total mass and has a power-law
dependence on the combined tidal coupling constant (kap2t) and weakly on
component masses through their product.
"""
import numpy as np

USED_INPUTS = ["mass", "kap2t", "m1", "m2"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    mass = X[:, 0]      # Total gravitational mass M
    kap2t = X[:, 1]      # Combined tidal coupling constant
    m1 = X[:, 2]         # Mass of primary
    m2 = X[:, 3]         # Mass of secondary
    
    # Fitted formula: f2 = a/M * kap2t^b * (m1*m2)^c
    # with a ≈ 44.0, b ≈ -0.35, c ≈ -0.082
    a = 44.05
    b = -0.35
    c = -0.082
    
    f2 = a / mass * (kap2t ** b) * ((m1 * m2) ** c)
    
    return f2