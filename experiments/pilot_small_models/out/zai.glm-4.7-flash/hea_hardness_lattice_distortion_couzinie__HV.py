"""HV = A * VEC + B * dHmix + C."""
import numpy as np

USED_INPUTS = ["VEC", "dHmix"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    vec = X[:, 0]
    dHmix = X[:, 1]
    
    # Fit coefficients from observed data
    # VEC=4.2, dHmix=-39.45 -> HV ~ 621
    # VEC=6.0, dHmix=0.0    -> HV ~ 499
    # VEC=5.5, dHmix=-5.0  -> HV ~ 531
    # Linear model: HV = a*VEC + b*dHmix + c
    
    # From VEC=4.2 vs VEC=6.0 (dHmix constant 0.0)
    # Slope a = (499 - 621) / (6.0 - 4.2) = -122 / 1.8 = -67.777...
    a = -67.77777777777777
    
    # From VEC=4.2 vs VEC=6.0 (dHmix constant 0.0)
    # Intercept c = HV - a*VEC = 499 - (-67.777 * 6.0) = 499 + 406.666 = 905.666...
    c = 905.6666666666666
    
    # From dHmix=-39.45 vs dHmix=0.0 (VEC constant 4.2)
    # Slope b = (621 - 621) / (0.0 - (-39.45)) = 0
    b = 0.0
    
    y_pred = a * vec + b * dHmix + c
    return y_pred