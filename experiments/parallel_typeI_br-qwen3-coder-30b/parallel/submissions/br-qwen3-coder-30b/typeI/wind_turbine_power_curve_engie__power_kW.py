"""Wind turbine power curve with cut-in, cubic, and cut-out regions."""
import numpy as np

USED_INPUTS = ["wind_speed_mps"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    v = X[:, 0]
    
    # Wind turbine power curve parameters
    cut_in_speed = 3.0
    rated_power = 2000.0
    k = 2.7435  # Coefficient for cubic relationship
    
    # Initialize output array
    y_pred = np.zeros_like(v)
    
    # Region 1: Below cut-in speed - no power generation
    mask1 = v < cut_in_speed
    y_pred[mask1] = 0.0
    
    # Region 2: Between cut-in and rated speed - cubic power curve
    mask2 = (v >= cut_in_speed) & (v <= 12.0)
    y_pred[mask2] = k * np.power(v[mask2] - cut_in_speed, 3)
    
    # Region 3: Above rated speed - maximum power output
    mask3 = v > 12.0
    y_pred[mask3] = rated_power
    
    return y_pred