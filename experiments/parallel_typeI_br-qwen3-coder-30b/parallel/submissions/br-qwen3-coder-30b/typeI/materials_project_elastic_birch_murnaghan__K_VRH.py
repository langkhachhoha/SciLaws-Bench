"""Bulk modulus as a function of atomic volume and crystal system."""
import numpy as np

USED_INPUTS = ["V_atomic_A3", "crystal_system_id"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    V = X[:, 0]
    cs = X[:, 1]
    
    # Base relationship: K_VRH ∝ 1/V
    # Apply crystal system multipliers
    # Multipliers determined from data: CS 2=0.49, CS 3=1.22, CS 4=1.05, CS 5=1.42, CS 6=1.71, CS 7=1.76
    multiplier = np.where(cs == 2, 0.49,
                 np.where(cs == 3, 1.22,
                 np.where(cs == 4, 1.05,
                 np.where(cs == 5, 1.42,
                 np.where(cs == 6, 1.71, 1.76)))))
    
    # Return the calculated bulk modulus
    return 1000.0 / V * multiplier