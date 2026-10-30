"""Methane emissions scale sublinearly with population and increase with GDP per capita and urbanization rate."""
import numpy as np

USED_INPUTS = ["GDP", "TP", "UR"]
LAW_CONSTANTS = {}
OTHER_CONSTANTS = {}
LOCAL_FITTABLE = {}

def predict(X):
    GDP = X[:, 0]
    TP = X[:, 1]
    UR = X[:, 2]
    
    # ME = a * TP^alpha * GDP^beta * UR^gamma
    # Fitted constants:
    a = 38.0
    alpha = 0.87
    beta = 0.08
    gamma = 0.45
    
    ME = a * (TP ** alpha) * (GDP ** beta) * (UR ** gamma)
    return ME