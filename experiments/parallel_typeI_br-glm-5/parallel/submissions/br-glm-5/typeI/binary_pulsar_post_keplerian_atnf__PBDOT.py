"""GR-inspired binary pulsar orbital period derivative formula."""
import numpy as np

USED_INPUTS = ["Pb", "e"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    Pb = X[:, 0]  # orbital period in days
    e = X[:, 1]   # eccentricity
    
    # GR eccentricity enhancement factor
    # f(e) = (1 + 73/24*e^2 + 37/96*e^4) / (1-e^2)^(7/2)
    e2 = e**2
    e4 = e**4
    numerator = 1 + (73/24)*e2 + (37/96)*e4
    denominator = (1 - e2)**(7/2)
    ecc_factor = numerator / denominator
    
    # Power law in Pb with fitted exponent and coefficient
    # PBDOT = -k * Pb^c * f(e)
    k = 1.6e-14
    c = -1.92
    
    PBDOT = -k * (Pb**c) * ecc_factor
    
    return PBDOT