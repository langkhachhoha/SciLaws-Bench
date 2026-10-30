"""Triangular fundamental diagram for traffic flow."""
import numpy as np

USED_INPUTS = ["k_veh_km_lane"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    k = X[:, 0]
    # k_max = 499 km/lane (estimated from data)
    # c = 0.04967 h^-1 (estimated from maximum flow at k=249.5)
    k_max = 499.0
    c = 0.049669037473745084
    return k * (k_max - k) * c