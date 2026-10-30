"""Energy consumption scales with GDP^0.685 * TP * AP^3.384"""
import numpy as np

USED_INPUTS = ["GDP", "TP", "AP", "DP", "UR", "AT"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    # Extract inputs
    gdp = X[:, 0]
    tp = X[:, 1] 
    ap = X[:, 2]
    
    # Model parameters from fitting
    A = 5.45e-11
    alpha = 0.6845
    beta = 1.0058
    gamma = 3.3839
    
    # Compute the predicted energy consumption
    # EC = A * GDP^alpha * TP^beta * AP^gamma
    y_pred = A * (gdp ** alpha) * (tp ** beta) * (ap ** gamma)
    
    return y_pred