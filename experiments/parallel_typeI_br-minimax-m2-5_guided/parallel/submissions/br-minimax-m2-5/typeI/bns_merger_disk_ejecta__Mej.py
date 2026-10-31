"""Dynamical ejecta mass: tidal term + symmetric term with Lambda cutoff."""
import numpy as np

USED_INPUTS = ["q", "Lambda_tilde"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    q = X[:, 0]
    Lambda = X[:, 1]
    one_minus_q = 1 - q
    
    # Term 1: tidal disruption component - proportional to (1-q), scales as Lambda^2.4
    # This dominates for asymmetric binaries (low q) and high Lambda
    term1 = 3e-6 * (one_minus_q ** 0.45) * (Lambda ** 2.4)
    
    # Term 2: symmetric/equal-mass component - peaks around Lambda~500 then decreases  
    # This represents shock dynamics / remnant formation
    term2 = 3e-5 * (Lambda / 500) ** 0.5 * np.exp(-Lambda / 550)
    
    return term1 + term2