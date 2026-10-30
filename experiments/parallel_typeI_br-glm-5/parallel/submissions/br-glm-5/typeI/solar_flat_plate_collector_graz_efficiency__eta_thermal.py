"""Temperature-dependent heat loss model for flat-plate solar collector.
Physical mechanism: heat loss coefficient UL depends linearly on T_in, 
so the thermal efficiency is η = η₀ - UL*(T_in-T_amb)/G = η₀ - c*T_in*(T_in-T_amb)/G"""
import numpy as np

USED_INPUTS = ["G_W_m2", "T_in_C", "T_amb_C"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    G = X[:, 0]
    T_in = X[:, 1]
    T_amb = X[:, 2]
    eta0 = 0.705804
    c = 0.053483
    eta = eta0 - c * T_in * (T_in - T_amb) / G
    return eta