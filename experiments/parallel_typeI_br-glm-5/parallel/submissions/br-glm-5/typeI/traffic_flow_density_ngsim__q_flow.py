"""Greenberg traffic flow model: q = k * c * ln(k_jam/k)"""
import numpy as np

USED_INPUTS = ["k_veh_km_lane"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    k = X[:, 0]  # density in veh/km/lane
    c = 14.0     # characteristic speed parameter (km/h)
    k_jam = 550.0  # jam density parameter (veh/km/lane)
    # Greenberg model: flow = density * speed, where speed = c * ln(k_jam/k)
    q = k * c * np.log(k_jam / k)
    return q