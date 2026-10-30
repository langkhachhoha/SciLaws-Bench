"""PV power model with irradiance and temperature dependence."""
import numpy as np

USED_INPUTS = ["G_W_m2", "T_module_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    G = X[:, 0]
    T = X[:, 1]
    # Model: P_max = G * (0.221778 - 0.000700*T + 0.000002*T^2)
    return G * (0.221778 - 0.000700*T + 0.000002*T**2)