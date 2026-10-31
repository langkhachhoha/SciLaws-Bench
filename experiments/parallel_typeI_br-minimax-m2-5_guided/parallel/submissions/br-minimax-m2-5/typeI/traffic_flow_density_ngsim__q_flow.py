"""Traffic flow saturation model: q = A * k / (k + B), where A is max capacity and B is half-saturation density."""
import numpy as np

USED_INPUTS = ["k_veh_km_lane"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    k = X[:, 0]
    # Saturation model: q = A * k / (k + B)
    # Fitted parameters: A ≈ 3680 veh/h/lane, B ≈ 61.5 veh/km/lane
    A = 3680.13
    B = 61.53
    return A * k / (k + B)