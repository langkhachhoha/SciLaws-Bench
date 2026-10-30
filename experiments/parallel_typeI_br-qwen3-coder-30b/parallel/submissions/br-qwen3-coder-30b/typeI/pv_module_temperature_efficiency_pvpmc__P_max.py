"""PV power model with irradiance and temperature dependence."""
import numpy as np

USED_INPUTS = ["G_W_m2", "T_module_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    G = X[:, 0]
    T = X[:, 1]
    
    # Model parameters found from experimental data
    k = 0.206009
    alpha = -0.002936
    T_ref = 25.0
    
    # P_max = k * G * (1 + alpha * (T - T_ref))
    return k * G * (1 + alpha * (T - T_ref))