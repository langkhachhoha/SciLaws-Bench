"""Bulk modulus following K ~ density^(2/3) / V_atomic^(3/2) scaling law."""
import numpy as np

USED_INPUTS = ["V_atomic_A3", "density_g_cm3"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    V = X[:, 0]  # V_atomic_A3
    rho = X[:, 1]  # density_g_cm3
    return 2090.0 * rho**(2.0/3.0) / V**1.5