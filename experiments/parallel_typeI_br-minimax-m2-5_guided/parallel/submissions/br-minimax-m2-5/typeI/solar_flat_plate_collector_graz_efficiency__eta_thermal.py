"""Thermal efficiency of flat-plate solar collector: eta = eta_0 - UL * (T_in - T_amb) / G"""
import numpy as np

USED_INPUTS = ["G_W_m2", "T_in_C", "T_amb_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    G = X[:, 0]
    T_in = X[:, 1]
    T_amb = X[:, 2]
    eta_0 = 0.713395  # Optical efficiency term
    UL = 3.760265     # Overall heat loss coefficient (W/m²/K)
    return eta_0 - UL * (T_in - T_amb) / G