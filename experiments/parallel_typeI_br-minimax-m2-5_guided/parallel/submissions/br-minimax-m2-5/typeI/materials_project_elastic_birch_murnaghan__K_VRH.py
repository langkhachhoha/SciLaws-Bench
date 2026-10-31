"""Voigt-Reuss-Hill average bulk modulus: K = a * rho^(2/3) * V^(-3/2)"""
import numpy as np

USED_INPUTS = ["density_g_cm3", "V_atomic_A3"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # X[:, 0] = density_g_cm3 (rho)
    # X[:, 1] = V_atomic_A3 (V)
    rho = X[:, 0]
    V = X[:, 1]
    # K_VRH = 2074.2 * rho^(2/3) * V^(-3/2)
    return 2074.2 * (rho ** (2.0/3.0)) * (V ** (-1.5))