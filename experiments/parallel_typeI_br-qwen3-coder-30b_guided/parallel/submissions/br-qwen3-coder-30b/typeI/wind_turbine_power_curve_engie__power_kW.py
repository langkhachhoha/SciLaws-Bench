"""Wind turbine power curve model with cut-in, generation, and cut-out regions."""
import numpy as np

USED_INPUTS = ["wind_speed_mps"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    v = X[:, 0]
    
    # Wind turbine power curve parameters
    cut_in_speed = 3.0      # m/s
    rated_speed = 12.0      # m/s
    cut_out_speed = 25.0    # m/s
    rated_power = 2044.50   # kW
    
    # Quadratic coefficient for power generation (P = a * v^2)
    a = 7.3445
    
    # Initialize output array
    y_pred = np.zeros_like(v)
    
    # Apply the power curve model:
    # 1. Below cut-in speed: power = 0
    # 2. Between cut-in and rated: power = a * v^2
    # 3. Above rated: power = rated_power (with some decrease beyond cut-out)
    
    mask1 = v >= cut_in_speed
    mask2 = v >= rated_speed
    mask3 = v >= cut_out_speed
    
    # Power generation region
    y_pred[mask1] = a * (v[mask1] ** 2)
    
    # Rated power region
    y_pred[mask2] = rated_power
    
    # Cut-out region - power decreases beyond cut-out speed
    # Simple model: linear decrease from rated power to 0
    y_pred[mask3] = rated_power * (1 - (v[mask3] - cut_out_speed) / (cut_out_speed - rated_speed))
    
    # Ensure no negative powers
    y_pred = np.maximum(y_pred, 0)
    
    return y_pred